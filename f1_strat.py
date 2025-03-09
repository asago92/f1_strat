import streamlit as st
import pandas as pd
import plotly.express as px

# Constants
LAP_DISTANCE = 5.303  # km
TOTAL_LAPS = 58
PIT_STOP_LOSS = 20  # seconds (time lost during a pit stop)
TYRE_PERFORMANCE = {
    "Soft": {"pace": 1.25, "lifespan": 20, "color": "red"},  # pace in seconds per lap, lifespan in laps
    "Medium": {"pace": 1.30, "lifespan": 30, "color": "yellow"},
    "Hard": {"pace": 1.35, "lifespan": 40, "color": "white"},
}

# Function to calculate total race time for a given strategy
def calculate_race_time(strategy):
    total_time = 0
    current_tyre = strategy[0][0]
    laps_on_tyre = 0
    pit_stops = 0

    for lap in range(1, TOTAL_LAPS + 1):
        if laps_on_tyre >= TYRE_PERFORMANCE[current_tyre]["lifespan"]:
            # Pit stop required
            pit_stops += 1
            if pit_stops >= len(strategy):
                st.error(f"Strategy {strategy} ran out of tyres! Cannot complete the race.")
                return None, None
            total_time += PIT_STOP_LOSS
            current_tyre = strategy[pit_stops][0]
            laps_on_tyre = 0

        total_time += TYRE_PERFORMANCE[current_tyre]["pace"]
        laps_on_tyre += 1

    return total_time, pit_stops

# Streamlit App
st.title("F1 Race Strategy Simulator")
st.subheader("Melbourne Grand Prix Circuit")

# Define possible strategies
strategies = [
    [("Soft", 25), ("Medium", 33)],  # One-stop strategy
    [("Soft", 15), ("Soft", 20), ("Medium", 23)],  # Two-stop strategy
    [("Medium", 30), ("Hard", 28)],  # Alternative one-stop strategy
]

# Strategy names for display
strategy_names = [
    "One-Stop: Soft -> Medium",
    "Two-Stop: Soft -> Soft -> Medium",
    "One-Stop: Medium -> Hard",
]

# Calculate race time for all strategies
results = []
for i, strategy in enumerate(strategies):
    total_time, pit_stops = calculate_race_time(strategy)
    if total_time is not None:
        results.append({
            "Strategy": strategy_names[i],
            "Total Race Time (s)": total_time,
            "Pit Stops": pit_stops,
            "Tyre Segments": strategy,  # Store the tyre segments for visualization
        })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Display results in a table
st.write("### Race Strategy Results")
st.dataframe(results_df)

# Prepare data for the stacked bar chart
st.write("### Tyre Usage Visualization (Stacked Bar Chart)")

# Create a DataFrame for Plotly
plotly_data = []
for i, row in results_df.iterrows():
    strategy_name = row["Strategy"]
    tyre_segments = row["Tyre Segments"]
    for segment in tyre_segments:
        tyre_type = segment[0]
        lap_count = segment[1]
        plotly_data.append({
            "Strategy": strategy_name,
            "Tyre Type": tyre_type,
            "Laps": lap_count,
            "Color": TYRE_PERFORMANCE[tyre_type]["color"],
        })

plotly_df = pd.DataFrame(plotly_data)

# Create the stacked bar chart using Plotly
fig = px.bar(
    plotly_df,
    x="Strategy",
    y="Laps",
    color="Tyre Type",
    color_discrete_map={  # Map tyre types to their respective colors
        "Soft": "red",
        "Medium": "yellow",
        "Hard": "white",
    },
    title="Tyre Usage by Strategy",
    labels={"Laps": "Laps", "Strategy": "Strategy"},
    text="Laps",  # Display lap counts on the bars
)

# Update layout for better readability
fig.update_layout(
    barmode="stack",
    xaxis_title="Strategy",
    yaxis_title="Laps",
    legend_title="Tyre Type",
    xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)
