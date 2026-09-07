"""
Hunza Glacial Lakes Dashboard
Spatio-temporal Change in Hunza's Glacial Lake Number and Lake Area Change (2022-2026)
Future Leadership Internship Program 2026 - Internship Final Project

Pure Python / Streamlit application. No JavaScript, no HTML files, no backend server.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# --------------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------------
st.set_page_config(
    page_title="Hunza Glacial Lakes | Spatio-temporal Change 2022-2026",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

ASSETS = Path(__file__).parent / "assets"
MAPS = ASSETS / "maps"
FIGURES = ASSETS / "figures"
IMAGES = ASSETS / "images"

# --------------------------------------------------------------------------------
# THEME / STYLING (native Streamlit theming via config.toml + light CSS polish)
# --------------------------------------------------------------------------------
GLACIER_BLUE = "#1B4F72"
ARCTIC_CYAN = "#5DADE2"
DEEP_BLUE = "#0B2545"
CHARCOAL = "#2C3E50"
GLACIER_GRAY = "#AEB6BF"
ICE_WHITE = "#F5F9FC"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {ICE_WHITE};
    }}
    h1, h2, h3 {{
        color: {DEEP_BLUE};
        font-family: 'Georgia', serif;
    }}
    .section-banner {{
        background: linear-gradient(90deg, {GLACIER_BLUE} 0%, {ARCTIC_CYAN} 100%);
        padding: 14px 22px;
        border-radius: 8px;
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 18px;
    }}
    .info-card {{
        background-color: white;
        border: 1px solid {GLACIER_GRAY};
        border-left: 5px solid {GLACIER_BLUE};
        border-radius: 6px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }}
    .finding-box {{
        background-color: #EAF4FB;
        border: 1px solid {ARCTIC_CYAN};
        border-radius: 8px;
        padding: 20px 26px;
        margin: 12px 0 20px 0;
    }}
    .caption-text {{
        color: {CHARCOAL};
        font-size: 0.85rem;
        font-style: italic;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------------
# CORE DATA (source of truth: Table 2 / Table 3 of the internship report,
# with the 2022 lake count corrected to 145 per the report's own Abstract,
# Table 2, Section 4.2, Conclusion, and the report's own Figure 2 / Figure 5)
# --------------------------------------------------------------------------------
@st.cache_data
def load_inventory():
    return pd.DataFrame(
        {
            "Year": ["2022", "2024 (PMD)", "2025", "2026"],
            "Lake Count": [145, 299, 249, 310],
            "Total Lake Area (m2)": [6751067.93, 7893007.87, 5532488.21, 5754391.49],
            "Total Lake Area (km2)": [6.751, 7.893, 5.532, 5.754],
        }
    )


@st.cache_data
def load_change_table():
    return pd.DataFrame(
        {
            "Interval": ["2022 -> 2024 (PMD)", "2024 (PMD) -> 2025", "2025 -> 2026", "2022 -> 2026 (net)"],
            "Change in Lake Number": [154, -50, 61, 165],
            "% Change in Number": [106.21, -16.72, 24.50, 113.79],
            "Change in Total Area (m2)": [1141939.94, -2360519.66, 221903.28, -996676.44],
            "% Change in Area": [16.91, -29.91, 4.01, -14.76],
        }
    )


inventory_df = load_inventory()
change_df = load_change_table()

# --------------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------------------------------------
if IMAGES.joinpath("logo.png").exists():
    st.sidebar.image(str(IMAGES / "logo.png"), width="stretch")

st.sidebar.markdown("### 🏔️ Hunza Glacial Lakes")
st.sidebar.caption("Spatio-temporal Change 2022-2026")

SECTIONS = [
    "Home",
    "Research Overview",
    "Study Area",
    "Methodology",
    "Lake Inventory",
    "Temporal Change",
    "MNDWI Maps",
    "Interpretation",
    "Limitations",
    "Conclusion",
    "References",
]

section = st.sidebar.radio("Navigate", SECTIONS, label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Author:** Faseeh Tahir
    **Geo-code:** GWL-005
    **Program:** Future Leadership Internship Program 2026
    **Submitted to:** AI Geo Navigator
    """
)

# --------------------------------------------------------------------------------
# HOME
# --------------------------------------------------------------------------------
if section == "Home":
    st.title("Spatio-temporal Change in Hunza's Glacial Lake Number and Lake Area Change (2022-2026)")
    st.markdown("#### Future Leadership Internship Program 2026 &nbsp;|&nbsp; Internship Final Project")
    st.markdown(
        "**Submitted by:** Faseeh Tahir (Geo-code GWL-005) &nbsp;&nbsp;|&nbsp;&nbsp; "
        "**Submitted to:** AI Geo Navigator &nbsp;&nbsp;|&nbsp;&nbsp; **September 2026**"
    )
    st.markdown("---")

    st.markdown(
        """
        <div class="info-card">
        This study assesses spatial and temporal change in the glacial lakes of Hunza,
        Gilgit-Baltistan, across 2022, 2024, 2025 and 2026, using Sentinel-2 multispectral
        imagery processed in Google Earth Engine, the Modified Normalized Difference Water
        Index (MNDWI), and manual GIS-based digitization in ArcMap. The 2024 inventory,
        supplied by the Pakistan Meteorological Department, served as the base reference
        dataset, while lake boundaries for 2022, 2025 and 2026 were manually digitized using
        Sentinel-2 and MNDWI as interpretation layers within a fixed Hunza boundary mask.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Lake Inventory at a Glance")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("2022", "145 lakes", "6.751 km²")
    k2.metric("2024 (PMD)", "299 lakes", "7.893 km²")
    k3.metric("2025", "249 lakes", "5.532 km²")
    k4.metric("2026", "310 lakes", "5.754 km²")

    st.markdown(
        """
        <div class="finding-box">
        <h4>Central Finding: More mapped lakes — but less total mapped lake area</h4>
        Over the full 2022-2026 period, the number of mapped lakes increased by
        <b>+113.79%</b> (net +165 lakes), while total mapped lake area decreased by
        <b>-14.76%</b> (net -0.997 km²). Lake number and lake area moved in different,
        non-linear directions, showing that the two indicators are complementary rather
        than interchangeable measures of change in a glacierized, high-mountain basin.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    c1.metric("Net Lake-Number Change (2022-2026)", "+113.79%", "+165 lakes")
    c2.metric("Net Lake-Area Change (2022-2026)", "-14.76%", "-0.997 km²", delta_color="inverse")

# --------------------------------------------------------------------------------
# RESEARCH OVERVIEW
# --------------------------------------------------------------------------------
elif section == "Research Overview":
    st.markdown('<div class="section-banner">Research Overview</div>', unsafe_allow_html=True)

    st.subheader("Abstract")
    st.write(
        """
        This report presents the spatial and temporal change of lakes in Hunza, a mountainous
        district of Gilgit-Baltistan in northern Pakistan, across 2022, 2024, 2025 and 2026,
        using Remote Sensing and GIS techniques. Sentinel-2 multispectral imagery was processed
        in Google Earth Engine to generate MNDWI products for 2022, 2025 and 2026. MNDWI served
        as a water-enhancement reference layer supporting on-screen digitization of lake water
        surfaces within a fixed Hunza boundary. The 2024 PMD dataset was adopted as the base
        reference inventory. Results show a non-linear pattern: mapped lake number rose from
        145 (2022) to 299 (2024), fell to 249 (2025), and rose again to 310 (2026) — a net
        increase of +113.79%. Total mapped lake area rose from 6.751 km² (2022) to 7.893 km²
        (2024), fell sharply to 5.532 km² (2025), and recovered slightly to 5.754 km² (2026) —
        a net decrease of -14.76%. The contrast between rising lake count and falling total
        area indicates that the two metrics track different aspects of change: the appearance
        of new, often small water bodies, and the contraction or loss of area among individual
        lakes.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Aim")
        st.write(
            "To assess the spatio-temporal change in the number and total area of lakes "
            "within the Hunza study area across 2022, 2024, 2025 and 2026, using Sentinel-2 "
            "imagery, MNDWI, and manual GIS-based digitization."
        )
        st.subheader("Objectives")
        st.markdown(
            """
            - Acquire and process Sentinel-2 imagery for 2022, 2025 and 2026 in Google Earth Engine
            - Compute MNDWI for each of these years as a water-enhancement layer
            - Manually digitize lake boundaries for 2022, 2025 and 2026
            - Incorporate the 2024 PMD inventory as the base reference dataset
            - Calculate the number of mapped lakes and total lake area per year
            - Compare lake number and area across years and interpret the change
            """
        )
    with col2:
        st.subheader("Research Questions")
        st.markdown(
            """
            1. How has the total number of mapped lakes in Hunza changed between 2022 and 2026?
            2. How has the total area covered by lakes in Hunza changed over the same period?
            3. Do the trends in lake number and lake area move together, or do they diverge —
               and what does this indicate about the underlying nature of change?
            """
        )
        st.subheader("Scope and Significance")
        st.write(
            """
            The study is limited to the Hunza boundary shapefile and four observation years
            (2022, 2024, 2025, 2026), focusing on lake count and total area rather than
            individual-lake morphometry. Because Hunza contains lakes previously flagged for
            glacial lake outburst flood (GLOF) potential, a maintained multi-year inventory
            has direct relevance for hazard awareness, water-resource management, and future
            glacial lake research in the Karakoram.
            """
        )

# --------------------------------------------------------------------------------
# STUDY AREA
# --------------------------------------------------------------------------------
elif section == "Study Area":
    st.markdown('<div class="section-banner">Study Area</div>', unsafe_allow_html=True)

    st.image(str(MAPS / "study_area_map.jpg"), width="stretch",
              caption="Figure 1. Hunza study-area boundary")

    st.subheader("Location and Physiography")
    st.write(
        """
        Hunza is a mountainous district of Gilgit-Baltistan in northern Pakistan, located
        within the Karakoram range approximately between 36°N and 37°N latitude and 74°E and
        76°E longitude, as delineated by the Hunza boundary shapefile used for the study. The
        district borders the Khunjerab National Park to the east and shares frontier terrain
        with the Xinjiang region of China along its northeastern edge. The terrain is extremely
        rugged, with elevation ranging from valley floors near Gilgit and Aliabad in the south
        to permanently snow- and ice-covered peaks exceeding 7,000 m in the north and east.

        The district is drained by the Hunza River and its tributaries, which originate from
        extensive glacier systems including the Batura, Passu, Ghulkin, and Hispar glaciers,
        among many others. The combination of steep relief, active glaciation, and abundant
        meltwater has produced a dense mosaic of glacial lakes, moraine-dammed lakes, and
        smaller periglacial water bodies distributed across the study area.
        """
    )

    st.subheader("Climate and Hydrology")
    st.write(
        """
        Hunza experiences a cold, arid, high-mountain climate strongly influenced by elevation.
        Valley floors receive limited precipitation and are effectively semi-arid, while higher
        elevations accumulate substantial winter snowfall that sustains the glaciers feeding the
        region's rivers and lakes. Meltwater discharge peaks in summer, when snow and glacier
        ice melt is greatest — a seasonal pulse that is a primary control on the extent of many
        of the lakes.
        """
    )

    st.subheader("Rationale for Selecting Hunza")
    st.write(
        """
        Hunza was selected for two main reasons. First, it is a data-scarce region where
        continuous, ground-based hydrological monitoring of individual lakes is impractical,
        making satellite-based inventory the only feasible approach for repeated, area-wide
        assessment. Second, the presence of numerous glacial and proglacial lakes in the
        Karakoram — some previously flagged in the literature for GLOF potential — gives the
        monitoring task direct relevance to hazard awareness and water-resource planning.
        """
    )

# --------------------------------------------------------------------------------
# METHODOLOGY
# --------------------------------------------------------------------------------
elif section == "Methodology":
    st.markdown('<div class="section-banner">Methodology</div>', unsafe_allow_html=True)

    st.subheader("Workflow")
    steps = [
        "Sentinel-2 MSI Imagery",
        "Google Earth Engine",
        "Cloud filtering / composite preparation",
        "MNDWI calculation",
        "Water interpretation (3-class scheme)",
        "Manual lake digitization (ArcMap)",
        "Area calculation",
        "Temporal comparison",
    ]
    cols = st.columns(len(steps))
    for i, (c, s) in enumerate(zip(cols, steps)):
        with c:
            st.markdown(
                f"""<div style="background-color:{GLACIER_BLUE};color:white;border-radius:6px;
                padding:10px 6px;text-align:center;font-size:0.78rem;min-height:70px;
                display:flex;align-items:center;justify-content:center;">{s}</div>""",
                unsafe_allow_html=True,
            )
    st.caption("Workflow reconstructed from Sections 3.1-3.5 of the internship report.")

    st.markdown("---")
    st.subheader("MNDWI Formula")
    st.latex(r"MNDWI = \frac{B3 - B11}{B3 + B11} = \frac{Green - SWIR1}{Green + SWIR1}")
    st.write(
        """
        Introduced by **Xu (2006)**, MNDWI modifies the original Normalized Difference Water
        Index (NDWI) of **McFeeters (1996)** by substituting the near-infrared band with a
        shortwave-infrared band. **B3 (Green)** retains moderate reflectance over water, while
        **B11 (SWIR1)** is strongly absorbed by water — sharpening the contrast between open
        water and surrounding land, snow, ice, and built-up surfaces. The resulting raster
        ranges from -1 to +1, with higher positive values generally corresponding to open
        water.

        Because a high-mountain environment such as Hunza also contains snow, ice, and cast
        shadow that can spectrally resemble water, final lake boundaries were established
        through **manual, MNDWI-assisted digitization** rather than treating every
        MNDWI-positive pixel as an automatically finalized lake polygon.
        """
    )

    with st.expander("MNDWI Visualization Classes"):
        st.markdown(
            """
            | MNDWI Range | Class | Color |
            |---|---|---|
            | -1 to -0.1 | Non-water | Green |
            | -0.1 to 0.4 | Mixed / transitional | Cyan |
            | 0.4 to 0.9 | High-confidence open water | Blue |
            """
        )

    st.markdown("---")
    st.subheader("Data Sources")
    sources_df = pd.DataFrame(
        {
            "Dataset": [
                "Sentinel-2 MSI (Level-1C/2A) imagery",
                "MNDWI raster (GEE-derived)",
                "Hunza administrative/hydrological boundary",
                "2024 lake inventory (PMD)",
                "Manually digitized lake polygons",
                "Lake inventory workbook (Excel)",
            ],
            "Years": ["2022, 2025, 2026", "2022, 2025, 2026", "Static", "2024", "2022, 2025, 2026", "2022-2026"],
            "Source / Platform": [
                "Google Earth Engine Data Catalog",
                "Generated in GEE using B3 (Green) & B11 (SWIR1)",
                "Prepared shapefile, fixed study-area mask",
                "Supplied directly by Pakistan Meteorological Department",
                "On-screen digitization in ArcMap",
                "Compiled from digitized layers",
            ],
            "Role in the Study": [
                "Base multispectral imagery for MNDWI computation and visual interpretation",
                "Water-enhancement layer guiding manual digitization",
                "Clips all processing and mapping to the Hunza study extent",
                "Base inventory against which other years are compared",
                "Produces count and area figures for each year",
                "Source of all quantitative results, tables and graphs",
            ],
        }
    )
    st.dataframe(sources_df, width="stretch", hide_index=True)

# --------------------------------------------------------------------------------
# LAKE INVENTORY
# --------------------------------------------------------------------------------
elif section == "Lake Inventory":
    st.markdown('<div class="section-banner">Lake Inventory by Year</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("2022", "145 lakes", "6.751 km²")
    k2.metric("2024 (PMD)", "299 lakes", "7.893 km²")
    k3.metric("2025", "249 lakes", "5.532 km²")
    k4.metric("2026", "310 lakes", "5.754 km²")

    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.subheader("Table 2. Number of mapped lakes and total lake area, 2022-2026")

    year_filter = st.selectbox("Filter by year (optional)", ["All years"] + list(inventory_df["Year"]))
    if year_filter == "All years":
        st.dataframe(
            inventory_df.style.format({"Total Lake Area (m2)": "{:,.2f}", "Total Lake Area (km2)": "{:.3f}"}),
            width="stretch",
            hide_index=True,
        )
    else:
        st.dataframe(
            inventory_df[inventory_df["Year"] == year_filter].style.format(
                {"Total Lake Area (m2)": "{:,.2f}", "Total Lake Area (km2)": "{:.3f}"}
            ),
            width="stretch",
            hide_index=True,
        )

    st.markdown(
        """
        <div class="info-card">
        The inventory shows that the number of mapped lakes was lowest in 2022 (145) and
        highest in 2026 (310), with an intermediate peak in 2024 (299) and a partial decline
        in 2025 (249). Total lake area, in contrast, was highest in 2024 (7.893 km²) and
        lowest in 2025 (5.532 km²) — lake count peaked in 2026 while lake area peaked in 2024.
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------------
# TEMPORAL CHANGE
# --------------------------------------------------------------------------------
elif section == "Temporal Change":
    st.markdown('<div class="section-banner">Temporal Change</div>', unsafe_allow_html=True)

    st.subheader("Chart 1 — Temporal Variation in Total Number of Mapped Lakes")
    tab1, tab2 = st.tabs(["Interactive (Plotly)", "Original Report Figure"])
    with tab1:
        fig1 = go.Figure(
            data=[
                go.Bar(
                    x=inventory_df["Year"],
                    y=inventory_df["Lake Count"],
                    marker_color=GLACIER_BLUE,
                    text=inventory_df["Lake Count"],
                    textposition="outside",
                    hovertemplate="Year: %{x}<br>Lake Count: %{y}<extra></extra>",
                )
            ]
        )
        fig1.update_layout(
            title="Temporal variation in total number of mapped lakes",
            xaxis_title="Year",
            yaxis_title="Number of Mapped Lakes",
            plot_bgcolor="white",
            height=450,
        )
        st.plotly_chart(fig1, width="stretch")
    with tab2:
        st.image(str(FIGURES / "lake_number_chart.png"), width="stretch",
                  caption="Figure 5. Temporal variation in the total number of mapped lakes in Hunza (2022-2026).")

    st.markdown("---")
    st.subheader("Chart 2 — Temporal Variation in Total Mapped Lake Area")
    tab3, tab4 = st.tabs(["Interactive (Plotly)", "Original Report Figure"])
    with tab3:
        fig2 = go.Figure(
            data=[
                go.Bar(
                    x=inventory_df["Year"],
                    y=inventory_df["Total Lake Area (km2)"],
                    marker_color=ARCTIC_CYAN,
                    text=[f"{v:.3f}" for v in inventory_df["Total Lake Area (km2)"]],
                    textposition="outside",
                    hovertemplate="Year: %{x}<br>Area: %{y:.3f} km²<extra></extra>",
                )
            ]
        )
        fig2.update_layout(
            title="Temporal variation in total mapped lake area",
            xaxis_title="Year",
            yaxis_title="Total Lake Area (km²)",
            plot_bgcolor="white",
            height=450,
        )
        st.plotly_chart(fig2, width="stretch")
    with tab4:
        st.image(str(FIGURES / "lake_area_chart.png"), width="stretch",
                  caption="Figure 6. Temporal variation in total mapped lake area in Hunza (2022-2026).")

# --------------------------------------------------------------------------------
# MNDWI MAPS
# --------------------------------------------------------------------------------
elif section == "MNDWI Maps":
    st.markdown('<div class="section-banner">MNDWI Maps</div>', unsafe_allow_html=True)

    st.write(
        "MNDWI outputs were generated in Google Earth Engine for the 2022, 2025 and 2026 "
        "Sentinel-2 composites. Blue tones indicate the highest-confidence open-water "
        "response; cyan indicates a mixed/transitional response; green indicates non-water "
        "land cover."
    )

    map_year = st.selectbox("Select MNDWI Map", ["2022", "2025", "2026"])

    map_files = {
        "2022": ("mndwi_2022.png", "Figure 2. MNDWI result for Hunza, 2022."),
        "2025": ("mndwi_2025.png", "Figure 3. MNDWI result for Hunza, 2025."),
        "2026": ("mndwi_2026.png", "Figure 4. MNDWI result for Hunza, 2026."),
    }
    fname, caption = map_files[map_year]
    st.image(str(MAPS / fname), width="stretch", caption=caption)

    st.markdown(
        """
        <div class="info-card">
        Across all three years, the highest-confidence water response (blue) is concentrated
        along the main Hunza River corridor and its major tributary valleys, around known
        glacier margins and proglacial basins in the northern and eastern parts of the study
        area — consistent with the expected distribution of glacial meltwater, river channels,
        and standing lakes in this terrain. The cyan, mixed-response class is more spatially
        extensive and includes narrow or partially mixed water pixels, wet sediment, and some
        snow/ice edges, which is why this class was treated as a candidate layer requiring
        visual confirmation rather than confirmed water.
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------------
# INTERPRETATION
# --------------------------------------------------------------------------------
elif section == "Interpretation":
    st.markdown('<div class="section-banner">Interpretation</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="finding-box">
        <h4>More mapped lakes — but less total mapped lake area</h4>
        Lake number and total mapped lake area are complementary indicators of change, not
        interchangeable ones. Across 2022-2026, lake count rose overall (+113.79%) while
        total mapped area fell overall (-14.76%) — a divergence explained by the appearance of
        new, often small water bodies alongside the contraction or loss of area among
        individual, previously mapped lakes.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Interval-by-Interval Interpretation")
    with st.expander("2022 → 2024: Strong increase in both indicators", expanded=True):
        st.write(
            "Lake count rose by 154 (+106.21%) and total area rose by about 1.142 km² "
            "(+16.91%), suggesting a period of net water-surface expansion."
        )
    with st.expander("2024 → 2025: Decrease in both indicators"):
        st.write(
            "Lake count dropped by 50 (-16.72%) and total area dropped sharply by about "
            "2.361 km² (-29.91%), consistent with a period of contraction — possibly seasonal "
            "or inter-annual meltwater reduction, or a more conservative digitization threshold "
            "in the 2025 dataset."
        )
    with st.expander("2025 → 2026: Lake count increase, modest area increase"):
        st.write(
            "Lake count increased by 61 (+24.50%) while total area increased by only about "
            "0.222 km² (+4.01%) — a comparatively modest area gain relative to the count "
            "increase, suggesting much of the increase in lake number reflects newly detected "
            "small water bodies rather than substantial expansion of already-mapped lakes."
        )
    with st.expander("Overall (2022 → 2026): Divergent long-term trend"):
        st.write(
            "The net effect is a marked increase in lake count (+165 lakes, +113.79%) "
            "alongside a net decrease in total mapped area (-0.997 km², -14.76%) — the "
            "central quantitative finding of this study. Lake count follows a "
            "rise-fall-rise sequence (145 → 299 → 249 → 310), while total lake area follows "
            "a rise-fall-partial-recovery sequence (6.751 → 7.893 → 5.532 → 5.754 km²), "
            "peaking one year earlier than the eventual peak in lake count."
        )

    st.markdown("---")
    st.subheader("Year-to-Year Comparison")
    interval_choice = st.selectbox("Select interval", list(change_df["Interval"]))
    row = change_df[change_df["Interval"] == interval_choice].iloc[0]

    c1, c2 = st.columns(2)
    c1.metric("Change in Lake Number", f"{int(row['Change in Lake Number']):+d}", f"{row['% Change in Number']:+.2f}%")
    c2.metric(
        "Change in Total Area",
        f"{row['Change in Total Area (m2)']:+,.2f} m²",
        f"{row['% Change in Area']:+.2f}%",
        delta_color="normal" if row["% Change in Area"] >= 0 else "inverse",
    )

    st.markdown("---")
    st.subheader("Discussion of Spatial and Environmental Factors")
    st.write(
        """
        The spatial pattern visible in the MNDWI maps is consistent with the quantitative
        trends: the blue, high-confidence water class is concentrated along the Hunza River
        corridor, its tributary valleys, and proglacial basins near glacier margins — precisely
        the settings where new small lakes are most likely to appear as meltwater pathways
        shift, and where existing lakes are most sensitive to year-to-year changes in meltwater
        supply.

        Several image-related factors should also be considered. Sentinel-2's 10 m and 20 m
        bands are well suited to regional-scale lake mapping, but very small water bodies can
        occupy only a few pixels and are more sensitive to mixed-pixel effects — a marginal
        water body might be captured in one year's imagery and missed in another simply because
        of small differences in acquisition date, sun angle, or residual cloud. Because MNDWI
        values for snow, ice, and cast shadow can partially overlap with those of open water in
        mountainous terrain, the manual quality-control step is essential, and small differences
        in how conservatively that step was applied across digitization sessions cannot be fully
        ruled out as a contributing factor to year-to-year variation.
        """
    )

# --------------------------------------------------------------------------------
# LIMITATIONS
# --------------------------------------------------------------------------------
elif section == "Limitations":
    st.markdown('<div class="section-banner">Limitations of the Study</div>', unsafe_allow_html=True)

    limitations = [
        "The 2024 inventory was used as supplied by the PMD and was not independently "
        "re-digitized, so differences in digitization criteria between the 2024 dataset and "
        "the 2022/2025/2026 datasets cannot be fully separated from genuine changes in lake "
        "number and area.",
        "Manual digitization, while more reliable than an unfiltered MNDWI threshold in this "
        "terrain, still involves a degree of interpreter judgement, particularly for small or "
        "partially mixed water bodies near the detection limit of the imagery.",
        "Sentinel-2's 10 m-20 m spatial resolution constrains the reliable detection of very "
        "small lakes and narrow shorelines, so the true number of very small water bodies "
        "present on the ground in any given year may be somewhat under- or over-represented "
        "in the digitized inventory.",
        "Differences in acquisition date, sun angle, residual cloud or haze, and seasonal "
        "meltwater stage between the 2022, 2025 and 2026 image composites may contribute to "
        "part of the observed inter-annual variation, independent of any real change in lake "
        "number or area.",
        "The study reports lake count and total area only; it does not track the identity of "
        "individual lakes between years, so it cannot fully distinguish appearance/disappearance "
        "of individual lakes from splitting, merging, or boundary redrawing of persistent lakes.",
    ]
    for lim in limitations:
        st.markdown(f"- {lim}")

# --------------------------------------------------------------------------------
# CONCLUSION
# --------------------------------------------------------------------------------
elif section == "Conclusion":
    st.markdown('<div class="section-banner">Conclusion</div>', unsafe_allow_html=True)

    st.write(
        """
        This project developed and applied a Remote Sensing and GIS-based workflow to assess
        change in the lakes of Hunza across 2022, 2024, 2025 and 2026. Sentinel-2 multispectral
        imagery was processed in Google Earth Engine, and the Modified Normalized Difference
        Water Index (MNDWI) was computed for 2022, 2025 and 2026 to enhance and support the
        visual interpretation of open-water surfaces. The 2024 lake dataset supplied by the PMD
        was used as the base reference inventory, while lake boundaries for 2022, 2025 and 2026
        were manually digitized using Sentinel-2 imagery and MNDWI as interpretation layers,
        all constrained to a fixed Hunza study-area boundary.

        Based on the lake inventory, the number of mapped lakes in Hunza increased overall from
        145 in 2022 to 310 in 2026 — a net increase of 165 lakes (+113.79%) — following a
        non-linear rise-fall-rise trajectory across the four observation years. Total mapped
        lake area, in contrast, decreased overall from 6.751 km² in 2022 to 5.754 km² in 2026 —
        a net decrease of approximately 0.997 km² (-14.76%) — peaking in 2024 and falling
        thereafter.
        """
    )
    st.markdown(
        """
        <div class="finding-box">
        The contrast between a rising lake count and a falling total lake area is the central
        finding of this study. It demonstrates that lake number and lake area are complementary
        rather than interchangeable indicators of change in a glacierized, high-mountain basin —
        a growing number of mapped lakes does not, by itself, indicate an expanding water
        surface, and both metrics should be examined together in any future assessment of this
        kind. The work also underscores the value of multi-year, remote-sensing- and GIS-based
        monitoring for hazard awareness and water-resource planning in the Karakoram.
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------------
# REFERENCES
# --------------------------------------------------------------------------------
elif section == "References":
    st.markdown('<div class="section-banner">References</div>', unsafe_allow_html=True)

    references = [
        ("European Space Agency. (2024). *Sentinel-2 User Handbook*. Copernicus Open Access Hub.",
         "https://sentinel.esa.int/web/sentinel/user-guides/sentinel-2-msi"),
        ("Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., & Moore, R. (2017). "
         "Google Earth Engine: Planetary-scale geospatial analysis for everyone. "
         "*Remote Sensing of Environment*, 202, 18-27.",
         "https://doi.org/10.1016/j.rse.2017.06.031"),
        ("McFeeters, S. K. (1996). The use of the Normalized Difference Water Index (NDWI) in "
         "the delineation of open water features. *International Journal of Remote Sensing*, "
         "17(7), 1425-1432.",
         "https://doi.org/10.1080/01431169608948714"),
        ("Pakistan Meteorological Department. (2024). *Glacial Lake Inventory of Hunza, "
         "Gilgit-Baltistan (2024 dataset)*. Pakistan Meteorological Department, Islamabad.",
         None),
        ("Wang, X., Ding, Y., Liu, S., Jiang, L., Wu, K., Jiang, Z., & Guo, W. (2013). Changes "
         "of glacial lakes and implications in Tian Shan, central Asia, based on remote sensing "
         "data from 1990 to 2010. *Environmental Research Letters*, 8(4), 044052.",
         "https://doi.org/10.1088/1748-9326/8/4/044052"),
        ("Wang, X., Guo, X., Yang, C., Liu, Q., Wei, J., Zhang, Y., Liu, S., Zhang, Y., Jiang, "
         "Z., & Tang, Z. (2020). Glacial lake inventory of high-mountain Asia in 1990 and 2018 "
         "derived from Landsat images. *Earth System Science Data*, 12(3), 2169-2182.",
         "https://doi.org/10.5194/essd-12-2169-2020"),
        ("Xu, H. (2006). Modification of normalised difference water index (NDWI) to enhance "
         "open water features in remotely sensed imagery. *International Journal of Remote "
         "Sensing*, 27(14), 3025-3033.",
         "https://doi.org/10.1080/01431160600589179"),
    ]

    for text, url in references:
        if url:
            st.markdown(f"{text}  \n🔗 [{url}]({url})")
        else:
            st.markdown(text)
        st.markdown("")

# --------------------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Hunza Glacial Lakes Dashboard · Future Leadership Internship Program 2026 · "
    "Faseeh Tahir (GWL-005) · Built with Streamlit"
)
