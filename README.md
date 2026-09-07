# Hunza Glacial Lakes Dashboard

An interactive research dashboard for the internship project:

**Spatio-temporal Change in Hunza's Glacial Lake Number and Lake Area Change (2022-2026)**
Future Leadership Internship Program 2026 · Faseeh Tahir (GWL-005)

Built entirely in **Python** using **Streamlit** — no JavaScript, no HTML files, no
backend server, no database, and no API keys required.

## 1. What this project is

This dashboard presents the results of a Remote Sensing / GIS study tracking glacial
lake number and total lake area in Hunza, Gilgit-Baltistan, across 2022, 2024, 2025 and
2026, using Sentinel-2 imagery, MNDWI, and manual digitization in ArcMap. It includes:

- KPI cards and interactive tables of the lake inventory
- Interactive Plotly charts alongside the original report figures
- The original MNDWI maps for 2022, 2025 and 2026, selectable by year
- Full methodology, interpretation, limitations, conclusion, and references

## 2. How to run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## 3. How to deploy for free (Streamlit Community Cloud)

1. Push this project folder to a **GitHub** repository (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"New app"**, select your repository and branch.
4. Set the main file path to `app.py`.
5. Click **Deploy**.

That's it — no server setup, no build configuration, and no cost.

## Project structure

```
hunza-glacial-lakes/
├── app.py                  # the entire application
├── requirements.txt
├── README.md
└── assets/
    ├── maps/                # study area map + MNDWI maps (2022, 2025, 2026)
    ├── figures/              # original report charts
    └── images/               # logo
```

## Editing the data

All inventory figures (lake counts, areas, and % changes) live near the top of
`app.py` in the `load_inventory()` and `load_change_table()` functions. Update the
numbers there if the source report is revised.
