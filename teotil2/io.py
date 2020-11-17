import calendar
import os

import numpy as np
import pandas as pd


def get_annual_spredt_data(year, engine, par_list=["Tot-N", "Tot-P"]):
    """Get annual spredt data from RESA2.

    Args:
        year:     Int. Year of interest
        par_list: List. Parameters defined in
                  RESA2.RID_PUNKTKILDER_OUTPAR_DEF
        engine:   SQL-Alchemy 'engine' object already connected
                  to RESA2

    Returns:
        Dataframe
    """

    # Get data, converting units to tonnes
    sql = (
        "SELECT a.komm_no as komnr, "
        "       c.name, "
        "       (a.value*b.factor) AS value "
        "FROM resa2.rid_kilder_spredt_values a, "
        "resa2.rid_punktkilder_inp_outp b, "
        "resa2.rid_punktkilder_outpar_def c "
        "WHERE a.inp_par_id = b.in_pid "
        "AND b.out_pid = c.out_pid "
        "AND ar = %s" % year
    )

    spr_df = pd.read_sql(sql, engine)

    # Only continue if data
    if len(spr_df) == 0:
        print("    No spredt data for %s." % year)

        return None

    else:
        # Pivot
        spr_df = spr_df.pivot(index="komnr", columns="name", values="value").copy()

        # Tidy
        spr_df = spr_df[par_list]
        cols = ["spr_%s_tonnes" % i.lower() for i in spr_df.columns]
        spr_df.columns = cols
        spr_df.columns.name = ""
        spr_df.reset_index(inplace=True)
        spr_df.dropna(
            subset=[
                "komnr",
            ],
            inplace=True,
        )
        spr_df.dropna(subset=cols, how="all", inplace=True)
        spr_df["komnr"] = spr_df["komnr"].astype(int)

        return spr_df


def get_annual_aquaculture_data(year, engine, par_list=["Tot-N", "Tot-P"]):
    """Get annual aquaculture data from RESA2.

    Args:
        year:     Int. Year of interest
        par_list: List. Parameters defined in
                  RESA2.RID_PUNKTKILDER_OUTPAR_DEF
        engine:   SQL-Alchemy 'engine' object already connected
                  to RESA2

    Returns:
        Dataframe
    """

    # Get data, converting units to tonnes
    sql = (
        "SELECT regine, name, SUM(value) AS value FROM ( "
        "  SELECT b.regine, "
        "         c.name, "
        "         (a.value*d.factor) AS value "
        "  FROM resa2.rid_kilder_aqkult_values a, "
        "  resa2.rid_kilder_aquakultur b, "
        "  resa2.rid_punktkilder_outpar_def c, "
        "  resa2.rid_punktkilder_inp_outp d "
        "  WHERE a.anlegg_nr = b.nr "
        "  AND a.inp_par_id = d.in_pid "
        "  AND c.out_pid = d.out_pid "
        "  AND ar = %s) "
        "GROUP BY regine, name" % year
    )

    aqu_df = pd.read_sql(sql, engine)

    # Only continue if data
    if len(aqu_df) == 0:
        print("    No aquaculture data for %s." % year)

        return None

    else:
        # Pivot
        aqu_df = aqu_df.pivot(index="regine", columns="name", values="value").copy()

        # Tidy
        aqu_df = aqu_df[par_list]
        cols = ["aqu_%s_tonnes" % i.lower() for i in aqu_df.columns]
        aqu_df.columns = cols
        aqu_df.columns.name = ""
        aqu_df.reset_index(inplace=True)
        aqu_df.dropna(
            subset=[
                "regine",
            ],
            inplace=True,
        )
        aqu_df.dropna(subset=cols, how="all", inplace=True)

        return aqu_df


def get_annual_renseanlegg_data(year, engine, par_list=["Tot-N", "Tot-P"]):
    """Get annual renseanlegg data from RESA2.

    Args:
        year:     Int. Year of interest
        par_list: List. Parameters defined in
                  RESA2.RID_PUNKTKILDER_OUTPAR_DEF
        engine:   SQL-Alchemy 'engine' object already connected
                  to RESA2

    Returns:
        Dataframe
    """

    sql = (
        "SELECT regine, name, SUM(value) AS value FROM ( "
        "  SELECT b.regine, "
        "         b.type, "
        "         c.name, "
        "         (a.value*d.factor) AS value "
        "  FROM resa2.rid_punktkilder_inpar_values a, "
        "  resa2.rid_punktkilder b, "
        "  resa2.rid_punktkilder_outpar_def c, "
        "  resa2.rid_punktkilder_inp_outp d "
        "  WHERE a.anlegg_nr = b.anlegg_nr "
        "  AND a.inp_par_id = d.in_pid "
        "  AND c.out_pid = d.out_pid "
        "  AND year = %s) "
        "WHERE type = 'RENSEANLEGG' "
        "GROUP BY regine, type, name" % year
    )

    ren_df = pd.read_sql(sql, engine)

    # Only continue if data
    if len(ren_df) == 0:
        print("    No renseanlegg data for %s." % year)

        return None

    else:
        # Pivot
        ren_df = ren_df.pivot(index="regine", columns="name", values="value").copy()

        # If no data for pars, add cols of 0
        for par in par_list:
            if par not in ren_df.columns:
                print(f"    No renseanlegg data for {par} in {year}.")
                ren_df[par] = 0

        # Tidy
        ren_df = ren_df[par_list]
        cols = ["ren_%s_tonnes" % i.lower() for i in ren_df.columns]
        ren_df.columns = cols
        ren_df.columns.name = ""
        ren_df.reset_index(inplace=True)
        ren_df.dropna(
            subset=[
                "regine",
            ],
            inplace=True,
        )
        ren_df.dropna(subset=cols, how="all", inplace=True)

        return ren_df


def get_annual_industry_data(year, engine, par_list=["Tot-N", "Tot-P"]):
    """Get annual industry data from RESA2.

    Args:
        year:     Int. Year of interest
        par_list: List. Parameters defined in
                  RESA2.RID_PUNKTKILDER_OUTPAR_DEF
        engine:   SQL-Alchemy 'engine' object already connected
                  to RESA2

    Returns:
        Dataframe
    """

    sql = (
        "SELECT regine, name, SUM(value) AS value FROM ( "
        "  SELECT b.regine, "
        "         b.type, "
        "         c.name, "
        "         (a.value*d.factor) AS value "
        "  FROM resa2.rid_punktkilder_inpar_values a, "
        "  resa2.rid_punktkilder b, "
        "  resa2.rid_punktkilder_outpar_def c, "
        "  resa2.rid_punktkilder_inp_outp d "
        "  WHERE a.anlegg_nr = b.anlegg_nr "
        "  AND a.inp_par_id = d.in_pid "
        "  AND c.out_pid = d.out_pid "
        "  AND year = %s) "
        "WHERE type = 'INDUSTRI' "
        "GROUP BY regine, type, name" % year
    )

    ind_df = pd.read_sql(sql, engine)

    # Only continue if data
    if len(ind_df) == 0:
        print("    No industry data for %s." % year)

        return None

    else:
        # Pivot
        ind_df = ind_df.pivot(index="regine", columns="name", values="value").copy()

        # Tidy
        ind_df = ind_df[par_list]
        cols = ["ind_%s_tonnes" % i.lower() for i in ind_df.columns]
        ind_df.columns = cols
        ind_df.columns.name = ""
        ind_df.reset_index(inplace=True)
        ind_df.dropna(
            subset=[
                "regine",
            ],
            inplace=True,
        )
        ind_df.dropna(subset=cols, how="all", inplace=True)

        return ind_df


def get_annual_vassdrag_mean_flows(year, engine):
    """Get annual flow data for main NVE vassdrags based on
        RESA2.DISCHARGE_VALUES.

    Args:
        year:     Int. Year of interest
        engine:   SQL-Alchemy 'engine' object already connected to
                  RESA2

    Returns:
        Dataframe
    """

    # Get NVE stn IDs
    sql = (
        "SELECT dis_station_id, TO_NUMBER(nve_serienummer) as Vassdrag "
        "FROM resa2.discharge_stations "
        "WHERE dis_station_name LIKE 'NVE Modellert%'"
    )

    nve_stn_df = pd.read_sql_query(sql, engine)
    nve_stn_df.index = nve_stn_df["dis_station_id"]
    del nve_stn_df["dis_station_id"]

    # Get avg. annual values for NVE stns
    sql = (
        "SELECT dis_station_id, AVG(xvalue) AS q_yr "
        "FROM resa2.discharge_values "
        "WHERE dis_station_id in ( "
        "  SELECT dis_station_id "
        "  FROM resa2.discharge_stations "
        "  WHERE dis_station_name LIKE 'NVE Modellert%%') "
        "AND TO_CHAR(xdate, 'YYYY') = %s "
        "GROUP BY dis_station_id "
        "ORDER BY dis_station_id" % year
    )

    an_avg_df = pd.read_sql_query(sql, engine)
    an_avg_df.index = an_avg_df["dis_station_id"]
    del an_avg_df["dis_station_id"]

    # Combine
    q_df = pd.concat([nve_stn_df, an_avg_df], axis=1)

    # Tidy
    q_df.reset_index(inplace=True, drop=True)
    q_df.sort_values(by="vassdrag", ascending=True, inplace=True)
    q_df.columns = ["vassom", "q_yr_m3/s"]

    return q_df


def get_annual_agricultural_coefficients(year, engine):
    """Get annual agricultural inputs from Bioforsk and
        convert to land use coefficients.

    Args:
        year:     Int. Year of interest
        engine:   SQL-Alchemy 'engine' object already connected to
                  RESA2

    Returns:
        Dataframe
    """
    # Read LU areas (same values used every year)
    in_csv = r"../data/core_input_data/fysone_land_areas.csv"
    lu_areas = pd.read_csv(in_csv, sep=";", encoding="windows-1252")

    # Read Bioforsk data
    sql = "SELECT * FROM RESA2.RID_AGRI_INPUTS " "WHERE year = %s" % year
    lu_lds = pd.read_sql(sql, engine)
    del lu_lds["year"]

    # Check have data
    if len(lu_lds) == 0:
        print("    No agricultural land use coefficients for %s." % year)

    # Join
    lu_df = pd.merge(lu_lds, lu_areas, how="outer", on="omrade")

    # Calculate required columns
    # N
    lu_df["agri_diff_tot-n_kg/km2"] = lu_df["n_diff_kg"] / lu_df["a_fy_agri_km2"]
    lu_df["agri_point_tot-n_kg/km2"] = (
        lu_df["n_point_kg"] / lu_df["a_fy_agri_km2"]
    )  # Orig a_fy_eng_km2??
    lu_df["agri_back_tot-n_kg/km2"] = lu_df["n_back_kg"] / lu_df["a_fy_agri_km2"]

    # P
    lu_df["agri_diff_tot-p_kg/km2"] = lu_df["p_diff_kg"] / lu_df["a_fy_agri_km2"]
    lu_df["agri_point_tot-p_kg/km2"] = (
        lu_df["p_point_kg"] / lu_df["a_fy_agri_km2"]
    )  # Orig a_fy_eng_km2??
    lu_df["agri_back_tot-p_kg/km2"] = lu_df["p_back_kg"] / lu_df["a_fy_agri_km2"]

    # Get cols of interest
    cols = [
        "fylke_sone",
        "fysone_name",
        "agri_diff_tot-n_kg/km2",
        "agri_point_tot-n_kg/km2",
        "agri_back_tot-n_kg/km2",
        "agri_diff_tot-p_kg/km2",
        "agri_point_tot-p_kg/km2",
        "agri_back_tot-p_kg/km2",
        "a_fy_agri_km2",
        "a_fy_eng_km2",
    ]

    lu_df = lu_df[cols]

    return lu_df


def make_rid_input_file(year, engine, core_fold, out_csv, par_list=["Tot-N", "Tot-P"]):
    """Builds a TEOTIL2 input file for the RID programme for the specified year. All the
       required data must be complete in RESA2.

    Args:
        year:      Int. Year of interest
        par_list:  List. Parameters defined in
                   RESA2.RID_PUNKTKILDER_OUTPAR_DEF
        out_csv:   Path for output CSV file
        core_fold: Path to folder containing core TEOTIL2 data files
        engine:    SQL-Alchemy 'engine' object already connected
                   to RESA2

    Returns:
        Dataframe. The CSV is written to the specified path.
    """

    # Read data from RESA2
    spr_df = get_annual_spredt_data(year, engine, par_list=par_list)
    aqu_df = get_annual_aquaculture_data(year, engine, par_list=par_list)
    ren_df = get_annual_renseanlegg_data(year, engine, par_list=par_list)
    ind_df = get_annual_industry_data(year, engine, par_list=par_list)
    agri_df = get_annual_agricultural_coefficients(year, engine)
    q_df = get_annual_vassdrag_mean_flows(year, engine)

    # Read core TEOTIL2 inputs
    # 1. Regine network
    # Changes to kommuner boundaries in 2017 require different files for
    # different years
    if year < 2017:
        csv_path = os.path.join(core_fold, "regine_pre_2017.csv")
        reg_df = pd.read_csv(csv_path, index_col=0, sep=";")
    elif year == 2017:
        csv_path = os.path.join(core_fold, "regine_2017.csv")
        reg_df = pd.read_csv(csv_path, index_col=0, sep=";")
    else:
        csv_path = os.path.join(core_fold, "regine_2018_onwards.csv")
        reg_df = pd.read_csv(csv_path, index_col=0, sep=";")

    # 2. Retention factors
    csv_path = os.path.join(core_fold, "retention_nutrients.csv")
    ret_df = pd.read_csv(csv_path, sep=";")

    # 3. Land cover
    csv_path = os.path.join(core_fold, "land_cover.csv")
    lc_df = pd.read_csv(csv_path, index_col=0, sep=";")

    # 4. Lake areas
    csv_path = os.path.join(core_fold, "lake_areas.csv")
    la_df = pd.read_csv(csv_path, index_col=0, sep=";")

    # 5. Background coefficients
    csv_path = os.path.join(core_fold, "back_coeffs.csv")
    back_df = pd.read_csv(csv_path, sep=";")

    # 7. Fylke-Sone
    csv_path = os.path.join(core_fold, "regine_fysone.csv")
    fy_df = pd.read_csv(csv_path, sep=";")

    # Convert par_list to lower case
    par_list = [i.lower() for i in par_list]

    # Process data
    # 1. Land use
    # 1.1 Land areas
    # Join lu datasets
    area_df = pd.concat([reg_df, lc_df, la_df], axis=1, sort=True)
    area_df.index.name = "regine"
    area_df.reset_index(inplace=True)

    # Fill NaN
    area_df.fillna(value=0, inplace=True)

    # Get total area of categories
    area_df["a_sum"] = (
        area_df["a_wood_km2"]
        + area_df["a_agri_km2"]
        + area_df["a_upland_km2"]
        + area_df["a_glacier_km2"]
        + area_df["a_urban_km2"]
        + area_df["a_sea_km2"]
        + area_df["a_lake_km2"]
    )

    # If total exceeds overall area, calc correction factor
    area_df["a_cor_fac"] = np.where(
        area_df["a_sum"] > area_df["a_reg_km2"],
        area_df["a_reg_km2"] / area_df["a_sum"],
        1,
    )

    # Apply correction factor
    area_cols = [
        "a_wood_km2",
        "a_agri_km2",
        "a_upland_km2",
        "a_glacier_km2",
        "a_urban_km2",
        "a_sea_km2",
        "a_lake_km2",
        "a_sum",
    ]

    for col in area_cols:
        area_df[col] = area_df[col] * area_df["a_cor_fac"]

    # Calc 'other' column
    area_df["a_other_km2"] = area_df["a_reg_km2"] - area_df["a_sum"]

    # Combine 'glacier' and 'upland' as 'upland'
    area_df["a_upland_km2"] = area_df["a_upland_km2"] + area_df["a_glacier_km2"]

    # Add 'land area' column
    area_df["a_land_km2"] = area_df["a_reg_km2"] - area_df["a_sea_km2"]

    # Tidy
    del area_df["a_glacier_km2"], area_df["a_sum"], area_df["a_cor_fac"]

    # 1.2. Join background coeffs
    area_df = pd.merge(area_df, back_df, how="left", on="regine")

    # 1.3. Join agri coeffs
    area_df = pd.merge(area_df, fy_df, how="left", on="regine")
    area_df = pd.merge(area_df, agri_df, how="left", on="fylke_sone")

    # 2. Discharge
    # Sum LTA to vassom level
    lta_df = area_df[["vassom", "q_reg_m3/s"]].groupby("vassom").sum().reset_index()
    lta_df.columns = ["vassom", "q_lta_m3/s"]

    # Join
    q_df = pd.merge(lta_df, q_df, how="left", on="vassom")

    # Calculate corr fac
    q_df["q_fac"] = q_df["q_yr_m3/s"] / q_df["q_lta_m3/s"]

    # Join and reset index
    df = pd.merge(area_df, q_df, how="left", on="vassom")
    df.index = df["regine"]
    del df["regine"]

    # Calculate regine-specific flow for this year
    for col in ["q_sp_m3/s/km2", "runoff_mm/yr", "q_reg_m3/s"]:
        df[col] = df[col] * df["q_fac"]

        # Fill NaN
        df[col].fillna(value=0, inplace=True)

    # Tidy
    del df["q_fac"], df["q_yr_m3/s"], df["q_lta_m3/s"]

    # 3. Point sources
    # 3.1. Aqu, ren, ind
    # List of data to concat later
    df_list = [
        df,
    ]

    # Set indices
    for pt_df in [aqu_df, ren_df, ind_df]:
        if pt_df is not None:
            pt_df.index = pt_df["regine"]
            del pt_df["regine"]
            df_list.append(pt_df)

    # Join
    df = pd.concat(df_list, axis=1, sort=True)
    df.index.name = "regine"
    df.reset_index(inplace=True)

    # Fill NaN
    for typ in ["aqu", "ren", "ind"]:
        for par in par_list:
            col = "%s_%s_tonnes" % (typ, par)
            if col in df.columns:
                df[col].fillna(value=0, inplace=True)
            else:  # Create cols of zeros
                df[col] = 0

    # 3.2. Spr
    # Get total land area and area of cultivated land in each kommune
    kom_df = df[["komnr", "a_land_km2", "a_agri_km2"]]
    kom_df = kom_df.groupby("komnr").sum()
    kom_df.reset_index(inplace=True)
    kom_df.columns = ["komnr", "a_kom_km2", "a_agri_kom_km2"]

    if spr_df is not None:
        # Join 'spredt' to kommune areas
        kom_df = pd.merge(kom_df, spr_df, how="left", on="komnr")

    else:  # Create cols of zeros
        for par in par_list:
            kom_df["spr_%s_tonnes" % par.lower()] = 0

    # Join back to main df
    df = pd.merge(df, kom_df, how="left", on="komnr")

    # Distribute loads
    for par in par_list:
        # Over agri
        df["spr_agri"] = (
            df["spr_%s_tonnes" % par] * df["a_agri_km2"] / df["a_agri_kom_km2"]
        )

        # Over all area
        df["spr_all"] = df["spr_%s_tonnes" % par] * df["a_land_km2"] / df["a_kom_km2"]

        # Use agri if > 0, else all
        df["spr_%s_tonnes" % par] = np.where(
            df["a_agri_kom_km2"] > 0, df["spr_agri"], df["spr_all"]
        )

    # Delete intermediate cols
    del df["spr_agri"], df["spr_all"]

    # Fill NaN
    df["a_kom_km2"].fillna(value=0, inplace=True)
    df["a_agri_kom_km2"].fillna(value=0, inplace=True)

    for par in par_list:
        # Fill
        df["spr_%s_tonnes" % par].fillna(value=0, inplace=True)

    # 4. Diffuse
    # Loop over pars
    for par in par_list:
        # Background inputs
        # Woodland
        df["wood_%s_tonnes" % par] = (
            df["a_wood_km2"]
            * df["q_sp_m3/s/km2"]
            * df["c_wood_mg/l_%s" % par]
            * 0.0864
            * 365
        )

        # Upland
        df["upland_%s_tonnes" % par] = (
            df["a_upland_km2"]
            * df["q_sp_m3/s/km2"]
            * df["c_upland_mg/l_%s" % par]
            * 0.0864
            * 365
        )

        # Lake
        df["lake_%s_tonnes" % par] = (
            df["a_lake_km2"] * df["c_lake_kg/km2_%s" % par] / 1000
        )

        # Urban
        df["urban_%s_tonnes" % par] = (
            df["a_urban_km2"] * df["c_urban_kg/km2_%s" % par] / 1000
        )

        # Agri from Bioforsk
        # Background
        df["agri_back_%s_tonnes" % par] = (
            df["a_agri_km2"] * df["agri_back_%s_kg/km2" % par] / 1000
        )

        # Point
        df["agri_pt_%s_tonnes" % par] = (
            df["a_agri_km2"] * df["agri_point_%s_kg/km2" % par] / 1000
        )

        # Diffuse
        df["agri_diff_%s_tonnes" % par] = (
            df["a_agri_km2"] * df["agri_diff_%s_kg/km2" % par] / 1000
        )

    # 5. Retention and transmission
    # Join
    df = pd.merge(df, ret_df, how="left", on="regine")

    # Fill NaN
    for par in par_list:
        # Fill NaN
        df["ret_%s" % par].fillna(value=0, inplace=True)

        # Calculate transmission
        df["trans_%s" % par] = 1 - df["ret_%s" % par]

    # 6. Aggregate values
    # Loop over pars
    for par in par_list:
        # All point sources
        df["all_point_%s_tonnes" % par] = (
            df["spr_%s_tonnes" % par]
            + df["aqu_%s_tonnes" % par]
            + df["ren_%s_tonnes" % par]
            + df["ind_%s_tonnes" % par]
            + df["agri_pt_%s_tonnes" % par]
        )

        # Natural diffuse sources
        df["nat_diff_%s_tonnes" % par] = (
            df["wood_%s_tonnes" % par]
            + df["upland_%s_tonnes" % par]
            + df["lake_%s_tonnes" % par]
            + df["agri_back_%s_tonnes" % par]
        )

        # Anthropogenic diffuse sources
        df["anth_diff_%s_tonnes" % par] = (
            df["urban_%s_tonnes" % par] + df["agri_diff_%s_tonnes" % par]
        )

        # All sources
        df["all_sources_%s_tonnes" % par] = (
            df["all_point_%s_tonnes" % par]
            + df["nat_diff_%s_tonnes" % par]
            + df["anth_diff_%s_tonnes" % par]
        )

    # 7. Lake volume
    # Estimate volume using poor relation from TEOTIL1
    df["mean_lake_depth_m"] = 1.8 * df["a_lake_km2"] + 13
    df["vol_lake_m3"] = df["mean_lake_depth_m"] * df["a_lake_km2"] * 1e6

    # Get cols of interest
    # Basic_cols
    col_list = [
        "regine",
        "regine_ned",
        "a_reg_km2",
        "runoff_mm/yr",
        "q_reg_m3/s",
        "vol_lake_m3",
    ]

    # Param specific cols
    #    par_cols = ['trans_%s', 'aqu_%s_tonnes', 'ind_%s_tonnes', 'ren_%s_tonnes',
    #                'spr_%s_tonnes', 'all_point_%s_tonnes', 'nat_diff_%s_tonnes',
    #                'anth_diff_%s_tonnes', 'all_sources_%s_tonnes']

    # Changed 21/11/2018. See e-mail from John Rune received 20/11/2018 at 16.15
    # Now include 'urban' and 'agri_diff' as separate categories
    par_cols = [
        "trans_%s",
        "aqu_%s_tonnes",
        "ind_%s_tonnes",
        "ren_%s_tonnes",
        "spr_%s_tonnes",
        "agri_pt_%s_tonnes",
        "all_point_%s_tonnes",
        "urban_%s_tonnes",
        "agri_diff_%s_tonnes",
        "nat_diff_%s_tonnes",
        "anth_diff_%s_tonnes",
        "all_sources_%s_tonnes",
    ]

    # Build col list
    for name in par_cols:
        for par in par_list:
            # Get col
            col_list.append(name % par)

    # Get cols
    df = df[col_list]

    # Remove rows where regine_ned is null
    df = df.query("regine_ned == regine_ned")

    # Fill Nan
    df.fillna(value=0, inplace=True)

    # 7. Write output
    df.to_csv(out_csv, encoding="utf-8", index=False)

    return df


def make_metals_input_file(
    year,
    engine,
    core_fold,
    out_csv,
    par_list=["As", "Cd", "Cr", "Cu", "Hg", "Ni", "Pb", "Zn"],
):
    """Builds an input file for the selected metals for the specified year. All the required
       data must be complete in RESA2.

    Args:
        year:      Int. Year of interest
        par_list:  List. Metal parameters defined in RESA2.RID_PUNKTKILDER_OUTPAR_DEF
        out_csv:   Path for output CSV file
        core_fold: Path to folder containing core TEOTIL2 data files
        engine:    SQL-Alchemy 'engine' object already connected to RESA2

    Returns:
        Dataframe. The CSV is written to the specified path.
    """
    # Validate input
    valid_metals = ["As", "Cd", "Cr", "Cu", "Hg", "Ni", "Pb", "Zn"]
    for par in par_list:
        assert (
            par in valid_metals
        ), f"{par} is not valid. Must be one of ['As', 'Cd', 'Cr', 'Cu', 'Hg', 'Ni', 'Pb', 'Zn']."

    # Read data from RESA2
    ren_df = get_annual_renseanlegg_data(year, engine, par_list=par_list)
    ind_df = get_annual_industry_data(year, engine, par_list=par_list)
    q_df = get_annual_vassdrag_mean_flows(year, engine)

    # Read core TEOTIL2 inputs
    # 1. Regine network
    # Changes to kommuner boundaries in 2017 require different files for
    # different years
    if year < 2017:
        csv_path = os.path.join(core_fold, "regine_pre_2017.csv")
        reg_df = pd.read_csv(csv_path, index_col=0, sep=";")
    elif year == 2017:
        csv_path = os.path.join(core_fold, "regine_2017.csv")
        reg_df = pd.read_csv(csv_path, index_col=0, sep=";")
    else:
        csv_path = os.path.join(core_fold, "regine_2018_onwards.csv")
        reg_df = pd.read_csv(csv_path, index_col=0, sep=";")

    # 2. Retention factors
    csv_path = os.path.join(core_fold, "retention_metals.csv")
    ret_df = pd.read_csv(csv_path, sep=";")

    # 3. Land cover
    csv_path = os.path.join(core_fold, "land_cover.csv")
    lc_df = pd.read_csv(csv_path, index_col=0, sep=";")

    # 4. Lake areas
    csv_path = os.path.join(core_fold, "lake_areas.csv")
    la_df = pd.read_csv(csv_path, index_col=0, sep=";")

    # 5. Background coefficients
    csv_path = os.path.join(core_fold, "back_coeffs.csv")
    back_df = pd.read_csv(csv_path, sep=";")

    # 7. Fylke-Sone
    csv_path = os.path.join(core_fold, "regine_fysone.csv")
    fy_df = pd.read_csv(csv_path, sep=";")

    # 8. Diffuse concs from 1000 Lakes data
    csv_path = os.path.join(core_fold, "mean_metal_concs_2019.csv")
    wc_df = pd.read_csv(csv_path)
    cols = ["regine"] + [i for i in wc_df.columns if i.split("_")[0] in par_list]
    wc_df = wc_df[cols]
    wc_df.columns = [f"diff_{i.lower()}" for i in wc_df.columns]
    wc_df.rename({"diff_regine": "regine"}, inplace=True, axis="columns")

    # 9. Change factors for water chemistry
    csv_path = os.path.join(core_fold, "ospar_region_mean_metals_div_2019_smooth.csv")
    fac_df = pd.read_csv(csv_path)
    fac_df = fac_df.query("year == @year")

    # Convert par_list to lower case
    par_list = [i.lower() for i in par_list]

    # Process data
    # 1. Land use
    # 1.1 Land areas
    # Join lu datasets
    area_df = pd.concat([reg_df, lc_df, la_df], axis=1, sort=True)
    area_df.index.name = "regine"
    area_df.reset_index(inplace=True)

    # Fill NaN
    area_df.fillna(value=0, inplace=True)

    # Get total area of categories
    area_df["a_sum"] = (
        area_df["a_wood_km2"]
        + area_df["a_agri_km2"]
        + area_df["a_upland_km2"]
        + area_df["a_glacier_km2"]
        + area_df["a_urban_km2"]
        + area_df["a_sea_km2"]
        + area_df["a_lake_km2"]
    )

    # If total exceeds overall area, calc correction factor
    area_df["a_cor_fac"] = np.where(
        area_df["a_sum"] > area_df["a_reg_km2"],
        area_df["a_reg_km2"] / area_df["a_sum"],
        1,
    )

    # Apply correction factor
    area_cols = [
        "a_wood_km2",
        "a_agri_km2",
        "a_upland_km2",
        "a_glacier_km2",
        "a_urban_km2",
        "a_sea_km2",
        "a_lake_km2",
        "a_sum",
    ]

    for col in area_cols:
        area_df[col] = area_df[col] * area_df["a_cor_fac"]

    # Calc 'other' column
    area_df["a_other_km2"] = area_df["a_reg_km2"] - area_df["a_sum"]

    # Combine 'glacier' and 'upland' as 'upland'
    area_df["a_upland_km2"] = area_df["a_upland_km2"] + area_df["a_glacier_km2"]

    # Add 'land area' column
    area_df["a_land_km2"] = area_df["a_reg_km2"] - area_df["a_sea_km2"]

    # Tidy
    del area_df["a_glacier_km2"], area_df["a_sum"], area_df["a_cor_fac"]

    # 1.2. Join background coeffs
    area_df = pd.merge(area_df, back_df, how="left", on="regine")

    # 2. Discharge
    # Sum LTA to vassom level
    lta_df = area_df[["vassom", "q_reg_m3/s"]].groupby("vassom").sum().reset_index()
    lta_df.columns = ["vassom", "q_lta_m3/s"]

    # Join
    q_df = pd.merge(lta_df, q_df, how="left", on="vassom")

    # Calculate corr fac
    q_df["q_fac"] = q_df["q_yr_m3/s"] / q_df["q_lta_m3/s"]

    # Join and reset index
    df = pd.merge(area_df, q_df, how="left", on="vassom")
    df.index = df["regine"]
    del df["regine"]

    # Calculate regine-specific flow for this year
    for col in ["q_sp_m3/s/km2", "runoff_mm/yr", "q_reg_m3/s"]:
        df[col] = df[col] * df["q_fac"]

        # Fill NaN
        df[col].fillna(value=0, inplace=True)

    # Tidy
    del df["q_fac"], df["q_yr_m3/s"], df["q_lta_m3/s"]

    # Point sources
    # List of data to concat later
    df_list = [
        df,
    ]

    # Set indices
    for pt_df in [ren_df, ind_df]:
        if pt_df is not None:
            pt_df.index = pt_df["regine"]
            del pt_df["regine"]
            df_list.append(pt_df)

    # Join
    df = pd.concat(df_list, axis=1, sort=True)
    df.index.name = "regine"
    df.reset_index(inplace=True)

    # Fill NaN
    for typ in ["ren", "ind"]:
        for par in par_list:
            col = "%s_%s_tonnes" % (typ, par)
            if col in df.columns:
                df[col].fillna(value=0, inplace=True)
            else:  # Create cols of zeros
                df[col] = 0

    # Estimate volume using poor relation from TEOTIL1
    df["mean_lake_depth_m"] = 1.8 * df["a_lake_km2"] + 13
    df["vol_lake_m3"] = df["mean_lake_depth_m"] * df["a_lake_km2"] * 1e6

    # Join 1000 Lakes concs
    df = pd.merge(df, wc_df, on="regine", how="left")

    # Join change factors for water chem
    df = pd.merge(df, fac_df, on="ospar_region", how="left")

    # Diffuse fluxes (without retention)
    days_in_yr = 366 if calendar.isleap(year) else 365
    for col in df.columns:
        if col.split("_")[0] == "diff":
            par, unit = col.split("_")[1:]
            if unit == "mgpl":
                unit_fac = 1e9  # mg => tonnes
            elif unit == "µgpl":
                unit_fac = 1e12  # ug => tonnes
            elif unit == "ngpl":
                unit_fac = 1e15  # ug => tonnes
            else:
                raise ValueError("Parameter unit not recognised.")

            df[f"diff_{par}_tonnes"] = (
                1000
                * df["q_reg_m3/s"]
                * df[col]
                * df[f"{par}_div_2019"]
                * days_in_yr
                * 24
                * 60
                * 60
                * 1.2  # Bias-correction factor based on OLS regressions. See end of notebook 05
                / unit_fac
            )
            del df[col]

    # Retention and transmission
    df = pd.merge(df, ret_df, how="left", on="regine")
    for par in par_list:
        df["ret_%s" % par].fillna(value=0, inplace=True)
        df["trans_%s" % par] = 1 - df["ret_%s" % par]

    # Calculate aggregate columns
    for par in par_list:
        df[f"all_point_{par}_tonnes"] = (
            df[f"ind_{par}_tonnes"] + df[f"ren_{par}_tonnes"]
        )
        df[f"all_sources_{par}_tonnes"] = (
            df[f"all_point_{par}_tonnes"] + df[f"diff_{par}_tonnes"]
        )

    # Get cols of interest
    # Basic_cols
    col_list = [
        "regine",
        "regine_ned",
        "a_reg_km2",
        "runoff_mm/yr",
        "q_reg_m3/s",
        "vol_lake_m3",
    ]

    # Source cols
    par_cols = [
        "ind_%s_tonnes",
        "ren_%s_tonnes",
        "diff_%s_tonnes",
        "all_point_%s_tonnes",
        "all_sources_%s_tonnes",
    ]

    # Build col list
    for name in par_cols:
        for par in par_list:
            # Get col
            col_list.append(name % par)

    for par in par_list:
        col_list.append(f"trans_{par}")

    # Get cols
    df = df[col_list]

    # Remove rows where regine_ned is null
    df = df.query("regine_ned == regine_ned")

    # Fill Nan
    df.fillna(value=0, inplace=True)

    # Write output
    df.to_csv(out_csv, encoding="utf-8", index=False)

    return df


def make_input_file(
    year, engine, core_fold, out_csv, mode="nutrients", par_list=["Tot-N", "Tot-P"]
):
    """Make an input file for TEOTIL2 for either 'nutrients' (N and P) or 'metals' (As, Cd, Cr,
        Cu, Hg, Ni, Pb, Zn).

    Args:
        year:      Int. Year of interest
        engine:    SQL-Alchemy 'engine' object already connected to RESA2
        core_fold: Path to folder containing core TEOTIL2 data files
        out_csv:   Path for output CSV file
        mode:      Str. One of ['nutrients', 'metals']. Use 'nutrients' to simulate total N and
                   total P; 'metals' simulates As, Cd, Cr, Cu, Hg, Ni, Pb and Zn.
        par_list:  List. Parameters defined in RESA2.RID_PUNKTKILDER_OUTPAR_DEF

    Returns:
        Dataframe. The CSV is written to the specified path.
    """
    if mode == "nutrients":
        valid_pars = ["Tot-N", "Tot-P"]
        for par in par_list:
            assert (
                par in valid_pars
            ), f"Parameter '{par}' is not recognised for mode = '{mode}'."
        df = make_rid_input_file(year, engine, core_fold, out_csv, par_list=par_list)

    elif mode == "metals":
        valid_pars = ["As", "Cd", "Cr", "Cu", "Hg", "Ni", "Pb", "Zn"]
        for par in par_list:
            assert (
                par in valid_pars
            ), f"Parameter '{par}' is not recognised for mode = '{mode}'."
        df = make_metals_input_file(year, engine, core_fold, out_csv, par_list=par_list)

    else:
        raise ValueError("'mode' must be one of ['nutrients', 'metals'].")

    return df


def estimate_metal_change_factors_over_time(
    st_yr,
    end_yr,
    eng,
    par_list=["As", "Cd", "Cr", "Cu", "Hg", "Ni", "Pb", "Zn"],
    agg_stat="mean",
    smooth=True,
    omit_stns=None,
    out_csv=None,
):
    """Extracts all measured concentrations for the 155 stations within Elveovervåkingsprogrammet
        for the parameters and time period of interest. Groups stations according to OSPAR regions
        (slightly modified to include catchments draining to Sweden) and calculates an aggregated
        average (mean or median) time series for each region (with smoothing to remove big outliers
        if desired). Values are expressed relative to 2019, in order to give "change factors" that
        can be applied to the spatially interpolated 1000 Lakes dataset. For use with the main
        TEOTIL2 model, 'out_csv' should be set to:

            r"../data/core_input_data/ospar_region_mean_metals_div_2019_smooth.csv"

        NOTE: Requires module nivapy3.

    Args:
        st_yr:     Int. Start of period of interest
        end_yr:    Int. End of period of interest
        eng:       Obj. Active database engine object connected to the NIVABASE
        par_list:  List of str. One or more of ['As', 'Cd', 'Cr', 'Cu', 'Hg', 'Ni', 'Pb', 'Zn']
        agg_stat:  Str. Either 'mean' or 'median'
        smooth:    Bool. Whether to apply moving window median smoothing with a window width of 3
                   years. Removes large (artificial?) spikes from the historic data for regions
        omit_stns: List of ints. RESA2 station IDs for stations within Elveovervåkingsprogrammet
                   that should be omitted when calculating regional averages. Useful for cross-
                   validation (e.g. creating leave-one-out datasets)
        out_csv:   Raw str. Path for output CSV

    Returns:
        Dataframe containing annual concentration time series for each metal in 'par_list' for each
        OSPAR region, expressed relative to values in 2019. Optionally, the dataframe is saved as a
        CSV.
    """
    import nivapy3 as nivapy

    # Validate input
    years = range(st_yr, end_yr + 1)
    assert (
        2019 in years
    ), "This function computes values relative to 2019. 2019 must therefore be within the range of years i.e. 'st_yr' <= 2019 <= 'end_yr'."

    valid_metals = ["As", "Cd", "Cr", "Cu", "Hg", "Ni", "Pb", "Zn"]
    for par in par_list:
        assert (
            par in valid_metals
        ), f"{par} is not valid. Must be one of ['As', 'Cd', 'Cr', 'Cu', 'Hg', 'Ni', 'Pb', 'Zn']."

    assert agg_stat in [
        "mean",
        "median",
    ], "'agg_stat' must be one of ['mean', 'median']."

    # Read station details
    stn_xlsx = r"../data/metals/rid20_obs_loads/RID_Sites_List_2017-2020.xlsx"
    stn_df = pd.read_excel(stn_xlsx, sheet_name="RID_All")

    if omit_stns:
        stn_df = stn_df.query("station_id not in @omit_stns")

    # Tidy names for OSPAR regions
    stn_df["ospar_region"].replace(
        {
            "SKAGERAK": "Skagerrak",
            "NORTH SEA": "North Sea",
            "NORWEGIAN SEA2": "Norwegian Sea (2)",
            "LOFOTEN-BARENTS SEA": "Lofoten-Barents Sea",
        },
        inplace=True,
    )

    # Get parameter IDs
    par_df = nivapy.da.select_resa_station_parameters(
        stn_df, f"{st_yr}-01-01", f"{end_yr}-12-31", eng
    )
    par_df = par_df.query("parameter_name in @par_list")

    # Get water chemistry
    wc_df, dup_df = nivapy.da.select_resa_water_chemistry(
        stn_df, par_df, f"{st_yr}-01-01", f"{end_yr}-12-31", eng, drop_dups=True
    )

    # Annual agg for stations
    wc_df["year"] = wc_df["sample_date"].dt.year
    if agg_stat == "mean":
        ann_df = (
            wc_df.groupby(["station_id", "station_code", "station_name", "year"])
            .mean()
            .reset_index()
        )
    else:
        ann_df = (
            wc_df.groupby(["station_id", "station_code", "station_name", "year"])
            .median()
            .reset_index()
        )

    # Join region names
    ann_df = pd.merge(
        ann_df, stn_df[["station_id", "ospar_region"]], on="station_id", how="left"
    )

    ann_df.drop(
        ["station_id", "station_code", "station_name", "depth1", "depth2"],
        axis="columns",
        inplace=True,
    )

    # Annual agg for regions
    if agg_stat == "mean":
        ann_df = ann_df.groupby(["ospar_region", "year"]).mean().reset_index()
    else:
        ann_df = ann_df.groupby(["ospar_region", "year"]).median().reset_index()

    # Fill NaNs with linear interpolation and back-filling where necessary
    df_list = []
    for reg in ann_df["ospar_region"].unique():
        reg_df = ann_df.query("ospar_region == @reg").copy()

        assert len(reg_df) == len(years)

        # Fill NaN
        reg_df.sort_values("year", inplace=True)
        reg_df.interpolate(method="linear", inplace=True)
        reg_df.fillna(method="backfill", inplace=True)

        assert pd.isna(reg_df).all().all() == False

        reg_df.set_index(["ospar_region", "year"], inplace=True)

        # Calculate ratios to 2019
        for col in reg_df.columns:
            if smooth:
                # Apply rolling median smooth with window width of 3 years to remove huge spikes
                reg_df[col] = (
                    reg_df[col]
                    .rolling(window=3, center=True, win_type=None, min_periods=1)
                    .median()
                )
            df_2019 = reg_df.query("year == 2019")
            reg_df[col] = reg_df[col] / df_2019[col].iloc[0]

            reg_df.rename(
                {col: f"{col.split('_')[0].lower()}_div_2019"},
                inplace=True,
                axis="columns",
            )

        reg_df.reset_index(inplace=True)

        df_list.append(reg_df)

    ann_df = pd.concat(df_list, axis=0)
    ann_df = ann_df.round(2)

    if out_csv:
        ann_df.to_csv(out_csv, index=False)

    return ann_df
