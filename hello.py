from preswald import text, plotly, connect, get_df, table, query
import pandas as pd
import plotly.express as px

text("# Building a Greener NYC: Analyzing Where and Why Green Infrastructure Is Happening")

text("""
This dashboard explores how and where New York City is deploying Green Infrastructure (GI) to manage stormwater and create greener streets.Using open data from the NYC Department of Environmental Protection, I have analyzed borough-level trends in GI installations, tree coverage, sewer system types, and feature diversity. The results reveal that Queens and Brooklyn are leading the GI rollout — not just in quantity, but in greener, more flood-resilient design — largely driven by their high proportion of combined sewer systems.
""")

# Load the CSV
connect()
df = get_df('demo_csv')

text("Which Boroughs Are Leading in Green Infrastructure?")

sql = """
SELECT
  Borough,
  COALESCE(Status_Gro, 'Proposed') AS Status_Gro,
  COUNT(*) AS Number_of_buildings
FROM demo_csv
WHERE COALESCE(Status_Gro, 'Proposed') IN ('Constructed', 'In Construction', 'Proposed')
GROUP BY Borough, Status_Gro
ORDER BY Number_of_buildings DESC
"""

# Run query on in-memory df
result_df = query(sql, "demo_csv")
#table(result_df)

fig = px.bar(
    result_df,
    x="Borough",
    y="Number_of_buildings",
    color="Status_Gro",
    barmode="group",
    color_discrete_map={"Constructed": "green", "In Construction":"yellow","Proposed": "red"},
    title="GI Installations by Borough",
    text_auto=True
)
plotly(fig)

text("What kind of GI features used by Borough?")

#df["GI_Feature"] = df["GI_Feature"].fillna("Unknown")

fig = px.histogram(
    df,
    x="Borough",
    color="GI_Feature",
    barmode="stack",  # You can change to "group" if you prefer
    title="Distribution of GI Features by Borough",
    labels={"GI_Feature": "GI Feature Type", "Borough": "NYC Borough"},
    text_auto=True
)

plotly(fig)

text("Looks like GI initiatives are mostly around Queens and Brooklyn, let's find out why")

# Query to calculate average tree presence per borough
sql = """
SELECT
  Borough,
  AVG(
    CASE
      WHEN Tree_Commo IS NULL OR Tree_Commo = 'N/A' THEN 0
      ELSE 1
    END
  ) AS Tree_Coverage_Rate
FROM "demo_csv"
GROUP BY Borough
ORDER BY Tree_Coverage_Rate DESC
"""

tree_stats = query(sql, "demo_csv")
#table(tree_stats, title="Percent of GI Installations with Trees per Borough")

fig = px.bar(
    tree_stats,
    x="Tree_Coverage_Rate",
    y="Borough",
    orientation='h',
    text_auto=True,
    title="Tree Coverage Rate in GI Installations by Borough",
    labels={"Tree_Coverage_Rate": "Share of GI Sites with Trees"}
)
plotly(fig)

text("Why are these boroughs prioritized?")
sql = """
SELECT
  Borough,
  Sewer_Type,
  COUNT(*) AS Count
FROM "demo_csv"
GROUP BY Borough, Sewer_Type
ORDER BY Count DESC
"""

ex = query(sql, "demo_csv")
#table(ex)

fig = px.bar(
    ex,
    x="Borough",
    y="Count",
    color="Sewer_Type",
    barmode="stack",
    text_auto=True,
    title="Sewer Type Distribution by Borough",
    labels={"Count": "Number of GI Installations", "Sewer_Type": "Sewer Type"}
)

plotly(fig)

text("GI projects in these boroughs aren't just about beautification — they’re a targeted flood mitigation strategy. NYC DEP is likely prioritizing vulnerable infrastructure zones (combined sewer areas) for GI deployment")





















