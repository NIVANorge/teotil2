from collections import defaultdict

import geopandas as gpd
import graphviz
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def run_model(data):
    """Run the TEOTIL2 model with the specified inputs. 'data' must either be a dataframe or a
       file path to a CSV in the correct format e.g. the dataframe or CSV returned by
       make_input_file(). See below for format details.

       Quantities specified in 'data' are assigned to the regine catchment network and
       accumulated downstream, allowing for retention.

    Args:
        data: Raw str or dataframe e.g. as returned by make_input_file(). The following
              columns are mandatory:

                   ["regine", "regine_ned", "a_reg_km2",
                    "runoff_mm/yr", "q_reg_m3/s", "vol_lake_m3"]

              Additional columns to be accumulated must be named '{source}_{par}_{unit}',
              all in lowercase e.g. 'ind_cd_tonnes' for industrial point inputs of cadmium
              in tonnes. In addition, theremust be a corresponding column named
              'trans_{par}' containing transmission factors (floats between 0 and 1)

    Returns:
        NetworkX graph object with results added as node attributes.
    """
    # Parse input
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, str):
        df = pd.read_csv(data)
    else:
        raise ValueError('"data" must be either a "raw" string or a Pandas dataframe.')

    # Check required cols are present
    req_cols = [
        "regine",
        "regine_ned",
        "a_reg_km2",
        "runoff_mm/yr",
        "q_reg_m3/s",
        "vol_lake_m3",
    ]
    for col in req_cols:
        assert col in df.columns, f"'data' must contain a column named '{col}'."

    # Identify cols to accumulate
    acc_cols = [
        i for i in df.columns if (i not in req_cols) and (i.split("_")[0] != "trans")
    ]

    # Check 'trans' cols are present
    par_list = list(set([i.split("_")[-2] for i in acc_cols]))
    for par in par_list:
        assert (
            f"trans_{par}" in df.columns
        ), f"Column 'trans_{par}' not present in input.'"
        assert (
            df[f"trans_{par}"].between(0, 1, inclusive=True).all()
        ), f"Column 'trans_{par}' contains values outside of range [0, 1]"

    # Build graph
    g = nx.DiGraph()

    # Add nodes
    for idx, row in df.iterrows():
        nd = row["regine"]
        g.add_node(nd, local=row.to_dict(), accum={})

    # Add edges
    for idx, row in df.iterrows():
        fr_nd = row["regine"]
        to_nd = row["regine_ned"]
        g.add_edge(fr_nd, to_nd)

    # Accumulate
    g = accumulate_loads(g, acc_cols)

    return g


def accumulate_loads(g, acc_cols):
    """Perform accumulation over a TEOTIL2 hydrological network. Usually called by run_model().
       Local inputs for the sources and parameters specified by 'acc_cols' are accumulated
       downstream, allowing for parameter-specific retention.

    Args
        g          Pre-built NetworkX graph. Must be a directed tree/forest and each node must
                   have properties 'local' (internal load) and 'accum' (empty dict).
        acc_cols:  List of str. Columns to accumulate (in addition to the standard/required ones).
                   Must be named '{source}_{par}_{unit}' - see docstring for run_model() for
                   further details

    Returns
        NetworkX graph object. g is modifed by adding the property 'accum_XXX' to each node.
        This is the total amount of substance flowing out of the node.
    """
    assert nx.is_tree(g), "g is not a valid tree."
    assert nx.is_directed_acyclic_graph(g), "g is not a valid DAG."

    # Process nodes in topo order from headwaters down
    for nd in list(nx.topological_sort(g))[:-1]:
        # Get catchments directly upstream
        preds = list(g.predecessors(nd))

        if len(preds) > 0:
            # Accumulate total input from upstream
            # Counters default to 0
            a_up = 0
            q_up = 0
            tot_dict = defaultdict(int)

            # Loop over upstream catchments
            for pred in preds:
                a_up += g.nodes[pred]["accum"]["upstr_area_km2"]
                q_up += g.nodes[pred]["accum"]["q_m3/s"]

                # Loop over quantities of interest
                for col in acc_cols:
                    tot_dict[col] += g.nodes[pred]["accum"][col]

            # Assign outputs
            # Area and flow
            g.nodes[nd]["accum"]["upstr_area_km2"] = (
                a_up + g.nodes[nd]["local"]["a_reg_km2"]
            )
            g.nodes[nd]["accum"]["q_m3/s"] = q_up + g.nodes[nd]["local"]["q_reg_m3/s"]

            # Calculate output. Oi = ti(Li + Ii)
            for col in acc_cols:
                par = col.split("_")[-2]
                g.nodes[nd]["accum"][col] = (
                    g.nodes[nd]["local"][col] + tot_dict[col]
                ) * g.nodes[nd]["local"]["trans_%s" % par]

        else:
            # Area and flow
            g.nodes[nd]["accum"]["upstr_area_km2"] = g.nodes[nd]["local"]["a_reg_km2"]
            g.nodes[nd]["accum"]["q_m3/s"] = g.nodes[nd]["local"]["q_reg_m3/s"]

            # No upstream inputs. Oi = ti * Li
            for col in acc_cols:
                par = col.split("_")[-2]
                g.nodes[nd]["accum"][col] = (
                    g.nodes[nd]["local"][col] * g.nodes[nd]["local"]["trans_%s" % par]
                )

    return g


def plot_network(g, catch_id, direct="down", stat="accum", quant="upstr_area_km2"):
    """Create schematic diagram upstream or downstream of specified node.

    Args:
        g         NetworkX graph object returned by teo.run_model()
        catch_id: Str. Regine ID of interest
        direct:   Str. 'up' or 'down'. Direction to trace network
        stat:     Str. 'local' or 'accum'. Type of results to display
        quant:    Str. Any of the returned result types

    Returns:
        NetworkX graph. Can be displayed using draw(g2, show='ipynb')
    """
    # Parse direction
    if direct == "down":
        # Get sub-tree
        g2 = nx.dfs_tree(g, catch_id)

        # Update labels with 'quant'
        for nd in list(nx.topological_sort(g2))[:-1]:
            g2.nodes[nd]["label"] = "%s\n(%.2f)" % (nd, g.nodes[nd][stat][quant])

    elif direct == "up":
        # Get sub-tree
        g2 = nx.dfs_tree(g.reverse(), catch_id).reverse()

        # Update labels with 'quant'
        for nd in list(nx.topological_sort(g2)):
            g2.nodes[nd]["label"] = "%s\n(%.2f)" % (nd, g.nodes[nd][stat][quant])

    else:
        raise ValueError('"direct" must be "up" or "down".')

    # Draw
    res = nx.nx_agraph.to_agraph(g2)
    res.layout("dot")

    return graphviz.Source(res.to_string())


def make_map(
    g,
    stat="accum",
    quant="q_m3/s",
    trans="none",
    cmap="viridis",
    scheme="quantiles",
    n_classes=10,
    figsize=(8, 12),
    plot_path=None,
):
    """Display a map of the regine catchments, coloured according
    to the quantity specified.

    Args:
        g          NetworkX graph object returned by teo.run_model()
        stat:      Str. 'local' or 'accum'. Type of results to display
        quant:     Str. Any of the returned result types
        trans:     Str. One of ['none', 'log', 'sqrt']. Whether to transform 'quant'
                   before plotting
        cmap:      Str. Valid matplotlib colourmap
        scheme:    Str. Valid map classify scheme name. See here for details:
                       https://github.com/pysal/mapclassify
        n_classes: Int. Number of classes in 'scheme'. Corresponds to parameter 'k' here:
                       https://github.com/pysal/mapclassify
        figsize:   Tuple. Figure (width, height) in inches
        plot_path: Raw Str. Optional. Path to which plot will be saved

    Returns:
        None
    """
    # Extract data of interest from graph
    reg_list = []
    par_list = []

    for nd in list(nx.topological_sort(g))[:-1]:
        reg_list.append(g.nodes[nd]["local"]["regine"])
        par_list.append(g.nodes[nd][stat][quant])

    # Build df
    df = pd.DataFrame(data={quant: par_list, "VASSDRAGNR": reg_list})

    # Map title
    tit = quant.split("_")
    name = " ".join(tit[:-1]).capitalize()
    unit = tit[-1]

    # Transform if necessary
    if trans == "none":
        tit = f"{name} ({unit})"
    elif trans == "log":
        tit = f"log[{name} ({unit})]"
        df[quant] = np.log10(df[quant])
    elif trans == "sqrt":
        tit = f"sqrt[{name} ({unit})]"
        df[quant] = df[quant] ** 0.5
    else:
        raise ValueError("'trans' must be one of ['none', 'log', 'sqrt'].")

    # Read regine catchments and join
    reg_shp = r"../data/gis/reg_minste_f_wgs84.shp"
    reg_gdf = gpd.read_file(reg_shp).to_crs(epsg=32633)
    reg_gdf = reg_gdf.merge(df, on="VASSDRAGNR")

    # Plot
    ax = reg_gdf.plot(
        column=quant,
        legend=True,
        scheme=scheme,
        edgecolor="none",
        figsize=figsize,
        cmap=cmap,
        legend_kwds={"loc": "upper left"},
        classification_kwds={"k": n_classes},
    )
    ax.set_title(tit, fontsize=20)
    plt.axis("off")

    # Save
    if plot_path:
        plt.savefig(plot_path, dpi=300)


def model_to_dataframe(g, out_path=None):
    """Convert a TEOTIL2 graph to a Pandas dataframe. If a path is supplied, the dataframe
       will be written to CSV format.

    Args:
        g          NetworkX graph object returned by teo.run_model()
        plot_path: Raw Str. Optional. CSV path to which df will
                   be saved

    Returns:
        Dataframe
    """

    # Container for data
    out_dict = defaultdict(list)

    # Loop over data
    for nd in list(nx.topological_sort(g))[:-1]:
        for stat in ["local", "accum"]:
            for key in g.nodes[nd][stat]:
                out_dict["%s_%s" % (stat, key)].append(g.nodes[nd][stat][key])

    # Convert to df
    df = pd.DataFrame(out_dict)

    # Reorder cols
    key_cols = ["local_regine", "local_regine_ned"]
    cols = [i for i in df.columns if not i in key_cols]
    cols.sort()
    df = df[key_cols + cols]
    cols = list(df.columns)
    cols[:2] = ["regine", "regine_ned"]
    df.columns = cols

    # Write output
    if out_path:
        df.to_csv(out_path, index=False, encoding="utf-8")

    return df
