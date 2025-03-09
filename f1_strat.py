import streamlit as st
import matplotlib.pyplot as plt

# Constants
LAP_DISTANCE = 5.303  # km
TOTAL_LAPS = 58
PIT_STOP_LOSS = 20  # seconds (time lost during a pit stop)
TYRE_PERFORMANCE = {
    "Soft": {"pace": 1.25, "lifespan": 20},  # pace in seconds per lap, lifespan in laps
    "Medium": {"pace": 1.30, "lifespan": 30},
    "Hard": {"pace": 1.35, "lifespan": 40},
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
                st.error("Strategy ran out of tyres! Cannot complete the race.")
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

# Display strategy options
st.write("### Select a Strategy")
strategy_names = [
    "One-Stop: Soft -> Medium",
    "Two-Stop: Soft -> Soft -> Medium",
    "One-Stop: Medium -> Hard",
]
selected_strategy = st.selectbox("Choose a strategy:", strategy_names)

# Map selected strategy to the corresponding strategy list
strategy_index = strategy_names.index(selected_strategy)
strategy = strategies[strategy_index]

# Calculate race time for the selected strategy
total_time, pit_stops = calculate_race_time(strategy)

if total_time is not None:
    # Display results
    st.write("### Results")
    st.write(f"**Selected Strategy:** {selected_strategy}")
    st.write(f"**Total Race Time:** {total_time:.2f} seconds")
    st.write(f"**Number of Pit Stops:** {pit_stops}")

    # Visualize tyre usage
    st.write("### Tyre Usage Over Laps")
    tyre_usage = []
    current_tyre = strategy[0][0]
    laps_on_tyre = 0
    pit_stop_laps = []

    for lap in range(1, TOTAL_LAPS + 1):
        if laps_on_tyre >= TYRE_PERFORMANCE[current_tyre]["lifespan"]:
            pit_stop_laps.append(lap)
            if len(pit_stop_laps) >= len(strategy):
                break  # Stop if we run out of tyres
            current_tyre = strategy[len(pit_stop_laps)][0]
            laps_on_tyre = 0
        tyre_usage.append(current_tyre)
        laps_on_tyre += 1

    # Plot tyre usage

    fig, ax = plt.subplots()
    ax.plot(range(1, len(tyre_usage) + 1), [TYRE_PERFORMANCE[tyre]["pace"] for tyre in tyre_usage], label="Tyre Pace")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Pace (seconds per lap)")
    ax.set_title("Tyre Performance Over Race Distance")
    for pit_lap in pit_stop_laps:
        ax.axvline(x=pit_lap, color="red", linestyle="--", label="Pit Stop" if pit_lap == pit_stop_laps[0] else "")
    ax.legend()
    st.pyplot(fig)
