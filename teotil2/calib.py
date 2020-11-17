import os
from collections import defaultdict

import networkx as nx
import numpy as np
import pandas as pd


def build_calib_network(data, calib_node_set):
    """Build an unattributed network for the "calibration catchments" in 'calib_node_set'.
       Designed to help when calibrating the model (e.g. after adding a new component or
       parameter).

    Args:
        data:           Dataframe or raw str to model input file. Must include a contingency table
                        with columns 'regine' and 'regine_ned' describing network links.
        calib_node_set: Set of catchment IDs for which calibration data are available.

    Returns:
        (g, nd_list). Tuple. g is a NetworkX graph object for the sub-network upstream of
        catchments in calib_node_set. nd_list is a topologically sorted list of nodes.
    """
    # Parse input
    if isinstance(data, pd.DataFrame):
        df = data

    elif isinstance(data, str):
        df = pd.read_csv(data)

    else:
        raise ValueError('"data" must be either a "raw" string or a Pandas dataframe.')

    # Check required cols are present
    req_cols = ["regine", "regine_ned"]
    for col in req_cols:
        assert col in df.columns, f"'data' must contain a column named '{col}'."

    # Build graph
    g = nx.DiGraph()

    # Add nodes
    for idx, row in df.iterrows():
        nd = row["regine"]
        g.add_node(nd, local={}, accum={})

    # Add edges
    for idx, row in df.iterrows():
        fr_nd = row["regine"]
        to_nd = row["regine_ned"]
        g.add_edge(fr_nd, to_nd)

    # Check directed tree
    assert nx.is_tree(g), "g is not a valid tree."
    assert nx.is_directed_acyclic_graph(g), "g is not a valid DAG."

    # Get nodes upstream of each site with data
    nd_set = set()
    for nd in calib_node_set:
        nds = nx.dfs_tree(g.reverse(), nd).nodes()
        nd_set.update(nds)

    # Get subgraph
    g = g.subgraph(nd_set).copy()

    # Get topo node list
    nd_list = list(nx.topological_sort(g))

    return (g, nd_list)


def update_and_accumulate(g, nd_list, year, data_dict, cal_pars, par_list, reg_set):
    """Update network with properties for 'year' and accumulate downstream.

    Args
        g:         Pre-built NetworkX graph. Must be a directed tree/forest
                   and each node must have properties 'local' (internal load)
                   and 'accum' (empty dict).
        nd_list:   List. Topologically sorted list of nodes of g
        year:      Int. Year of interest
        data_dict: Dict. data_dict['node', year]['quantity]
        cal_pars:  Dict. Calibration parameters
        par_list:  List of parameters in the input file
        reg_set:  List of regine ID of interest

    Returns
        Dict containing accumulated loads for IDs in reg_set.
    """
    # Container for results
    out_dict = {"regine": [], "q_m3/s": []}
    for par in par_list:
        out_dict["%s_tonnes" % par] = []

    # Process nodes in topo order from headwaters down
    for nd in nd_list:
        # Update local properties
        # 1. Flow
        g.nodes[nd]["local"]["q_reg_m3/s"] = data_dict[(nd, year)]["q_reg_m3/s"]

        # 2. Water chem and transmission
        for par in par_list:
            g.nodes[nd]["local"]["trans_%s" % par] = (
                data_dict[(nd, year)]["trans_%s" % par] * cal_pars["b_r_%s" % par]
            )

            g.nodes[nd]["local"]["%s_tonnes" % par] = (
                data_dict[(nd, year)]["all_point_%s_tonnes" % par]
                * cal_pars["b_p_%s" % par]
            ) + (
                data_dict[(nd, year)]["all_diff_%s_tonnes" % par]
                * cal_pars["b_d_%s" % par]
            )

        # Accumulate
        # Get catchments directly upstream
        preds = list(g.predecessors(nd))

        if len(preds) > 0:
            # Accumulate total input from upstream
            # Counters default to 0
            q_up = 0
            tot_dict = defaultdict(int)

            # Loop over upstream catchments
            for pred in preds:
                q_up += g.nodes[pred]["accum"]["q_m3/s"]

                # Loop over quantities of interest
                for par in par_list:
                    tot_dict["%s_tonnes" % par] += g.nodes[pred]["accum"][
                        "%s_tonnes" % par
                    ]

            # Assign outputs
            # Flow
            g.nodes[nd]["accum"]["q_m3/s"] = q_up + g.nodes[nd]["local"]["q_reg_m3/s"]

            # Calculate output. Oi = ti(Li + Ii)
            for par in par_list:
                g.nodes[nd]["accum"]["%s_tonnes" % par] = (
                    g.nodes[nd]["local"]["%s_tonnes" % par]
                    + tot_dict["%s_tonnes" % par]
                ) * g.nodes[nd]["local"]["trans_%s" % par]

        else:
            # Flow
            g.nodes[nd]["accum"]["q_m3/s"] = g.nodes[nd]["local"]["q_reg_m3/s"]

            # No upstream inputs. Oi = ti * Li
            for par in par_list:
                g.nodes[nd]["accum"]["%s_tonnes" % par] = (
                    g.nodes[nd]["local"]["%s_tonnes" % par]
                    * g.nodes[nd]["local"]["trans_%s" % par]
                )

    # Add results to dict
    for nd in reg_set:
        out_dict["regine"].append(nd)
        out_dict["q_m3/s"].append(g.nodes[nd]["accum"]["q_m3/s"])
        for par in par_list:
            out_dict["%s_tonnes" % par].append(g.nodes[nd]["accum"]["%s_tonnes" % par])

    # Build df
    df = pd.DataFrame(out_dict)

    # Add year
    df["year"] = year

    return df


def read_obs_data(cal_prop, seed=1):
    """Reads observed data file for 155 RID sites from 1990 to 2016. Joins in basic station
       properties and splits into calibration and validation datasets.

    Args:
        cal_prop: Float. Between 0 and 1. Fraction of dataset to use for
                  calibration. The rest is for validation.
        seed:     Int. For repeatability

    Returns:
        Tuple (obs_df, cal_df, val_df). obs_df is the entire dataset
    """

    # Read obs data
    in_csv = (
        r"C:\Data\James_Work\Staff\Oeyvind_K\Elveovervakingsprogrammet"
        r"\NOPE\NOPE_RID_Calibration_Data\rid_all_obs_loads_flows_1990_2016.csv"
    )
    obs_df = pd.read_csv(in_csv)

    # Drop NaN
    obs_df.dropna(how="any", inplace=True)

    # Read station data
    in_xlsx = (
        r"C:\Data\James_Work\Staff\Oeyvind_K\Elveovervakingsprogrammet"
        r"\Data\RID_Sites_List.xlsx"
    )
    stn_df = pd.read_excel(in_xlsx, sheet_name="RID_All")
    stn_df = stn_df[["station_id", "nve_vassdrag_nr", "rid_group"]]

    # Join vassdrag nrs
    obs_df = pd.merge(obs_df, stn_df, how="left", on="station_id")

    # Split cal and val
    # NB: obs_df.sample randomises the rows, then np.split()
    # divides data into chunks at the desired split points
    cal_df, val_df = np.split(
        obs_df.sample(frac=1, random_state=seed),
        [
            int(cal_prop * len(obs_df)),
        ],
    )

    return (obs_df, cal_df, val_df)


def build_input_dict(st_yr, end_yr, par_list):
    """Build a dictionary of input data for running TEOTIL2 in calibration mode. Designed
       to improve performance compared to looping over dataframes.

    Args:
        st_yr:    Int. Start year of interest
        end_yr:   Int. Start year of interest
        par_list: List. Parameters of interest

    Returns:
        Dict with keys ('regine', year) => {'variable':value}
    """

    # Annual input folder
    core_fold = (
        r"C:\Data\James_Work\Staff\Oeyvind_K\Elveovervakingsprogrammet"
        r"\NOPE\NOPE_Annual_Inputs"
    )

    # Container for output
    df_list = []

    # Loop over CSV
    for year in range(st_yr, end_yr + 1):
        # Read data
        in_csv = os.path.join(core_fold, "nope_input_data_%s.csv" % year)
        df = pd.read_csv(in_csv)

        # Add year
        df["year"] = year

        # Add to output
        df_list.append(df)

    # Combine
    df = pd.concat(df_list, axis=0)

    # Add diffuse
    for par in par_list:
        df["all_diff_%s_tonnes" % par] = (
            df["nat_diff_%s_tonnes" % par] + df["anth_diff_%s_tonnes" % par]
        )

    # Get cols of interest
    par_cols = ["trans_%s", "all_point_%s_tonnes", "all_diff_%s_tonnes"]
    cols = [
        "regine",
        "year",
        "q_reg_m3/s",
    ] + [i % j for i in par_cols for j in par_list]
    df = df[cols]

    # Convert to dict for speed later
    in_data = df.set_index(["regine", "year"]).T.to_dict()

    return in_data


def run_model_multi_year(
    g, nd_list, st_yr, end_yr, in_data, par_list, reg_set, cal_pars=None
):
    """Run model for specified years.

    Args
        g:         Pre-built NetworkX graph. Must be a directed tree/forest
                   and each node must have properties 'local' (internal load)
                   and 'output' (empty dict).
        nd_list:   List. Topologically sorted list of nodes of g
        st_yr:     Int. Start year of interest
        end_yr:    Int. End year of interest
        in_data    Dict. All data required to run model
        par_list:  List of parameters in the input file
        reg_set:   List of regine IDs of interest
        cal_pars:  Dict. Calibration parameters

    Returns
        Dataframe of annual accumulated loads for IDs in reg_set.
    """
    # Build cal_par dict if necessary
    if cal_pars is None:
        cal_pars = {}
        for par in par_list:
            for coef in ["b_r", "b_p", "b_d"]:
                # Set defaults to 1
                cal_pars["%s_%s" % (coef, par)] = 1

    # Container for output
    df_list = []

    # Loop over years
    for year in range(st_yr, end_yr + 1):
        df = update_and_accumulate(
            g, nd_list, year, in_data, cal_pars, par_list, reg_set
        )

        df_list.append(df)

    # Combine
    df = pd.concat(df_list, axis=0)

    # Reorder
    cols = ["regine", "year", "q_m3/s"] + ["%s_tonnes" % i for i in par_list]
    df = df[cols]

    return df
