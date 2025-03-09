import streamlit as st
import pandas as pd
import plotly.express as px

# Constants
LAP_DISTANCE = 5.303  # km
TOTAL_LAPS = 58
PIT_STOP_LOSS = 20  # seconds (time lost during a pit stop)
TYRE_PERFORMANCE = {
    "Soft": {"pace": 1.25, "lifespan": 20, "color": "#f95738"},  # Soft: #f95738
    "Medium": {"pace": 1.30, "lifespan": 30, "color": "#f4d35e"},  # Medium: #f4d35e
    "Hard": {"pace": 1.35, "lifespan": 40, "color": "#ebebd3"},  # Hard: #ebebd3
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
                # If strategy runs out of tyres, continue with the last tyre
                current_tyre = strategy[-1][0]
                laps_on_tyre = 0
            else:
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
    # Convert tyre segments to a string representation
    tyre_segments_str = " -> ".join([f"{tyre} ({laps} laps)" for tyre, laps in strategy])
    results.append({
        "Strategy": strategy_names[i],
        "Total Race Time (s)": total_time,
        "Pit Stops": pit_stops,
        "Tyre Segments": tyre_segments_str,  # Store as a string
    })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Display results in a table
st.write("### Race Strategy Results")
st.dataframe(results_df)

# Prepare data for the stacked bar chart
st.write("### Tyre Usage Visualization (Horizontal Stacked Bar Chart)")

# Create a DataFrame for Plotly
plotly_data = []
for i, row in results_df.iterrows():
    strategy_name = row["Strategy"]
    tyre_segments = strategies[i]  # Use the original strategy list
    for segment in tyre_segments:
        tyre_type = segment[0]
        lap_count = segment[1]
        plotly_data.append({
            "Strategy": strategy_name,
            "Tyre Type": tyre_type,
            "Laps": lap_count,
            "Color": TYRE_PERFORMANCE[tyre_type]["color"],  # Use the updated color codes
        })

plotly_df = pd.DataFrame(plotly_data)

# Create the horizontal stacked bar chart using Plotly
fig = px.bar(
    plotly_df,
    y="Strategy",  # Strategies on the y-axis
    x="Laps",      # Laps on the x-axis
    color="Tyre Type",
    color_discrete_map={  # Map tyre types to their respective colors
        "Soft": "#f95738",  # Soft: #f95738
        "Medium": "#f4d35e",  # Medium: #f4d35e
        "Hard": "#ebebd3",  # Hard: #ebebd3
    },
    title="Tyre Usage by Strategy",
    labels={"Laps": "Laps", "Strategy": "Strategy"},
    text="Laps",  # Display lap counts on the bars
    orientation="h",  # Horizontal bar chart
)

# Update layout for better readability
fig.update_layout(
    barmode="stack",
    yaxis_title="Strategy",
    xaxis_title="Laps",
    legend_title="Tyre Type",
    # Remove gridlines
    xaxis_showgrid=False,
    yaxis_showgrid=False,
)

# Add gray borders to the bars
fig.update_traces(
    marker_line_color="gray",  # Gray border
    marker_line_width=1.5,     # Border width
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)
