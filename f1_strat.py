import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Constants
PIT_STOP_LOSS = 20  # seconds (time lost during a pit stop)
TYRE_PERFORMANCE = {
    "Soft": {"pace": 1.25, "lifespan": 20},
    "Medium": {"pace": 1.30, "lifespan": 30},
    "Hard": {"pace": 1.35, "lifespan": 40},
}

def calculate_race_time(strategy, total_laps):
    total_time = 0
    current_tyre = strategy[0][0]
    laps_on_tyre = 0
    pit_stops = 0

    for lap in range(1, total_laps + 1):
        if laps_on_tyre >= TYRE_PERFORMANCE[current_tyre]["lifespan"]:
            pit_stops += 1
            total_time += PIT_STOP_LOSS
            current_tyre = strategy[pit_stops][0]
            laps_on_tyre = 0

        total_time += TYRE_PERFORMANCE[current_tyre]["pace"]
        laps_on_tyre += 1

    return total_time, pit_stops

# Streamlit UI
st.title("F1 Tyre and Race Strategy Analyzer")

# User inputs
lap_distance = st.number_input("Lap Distance (km)", min_value=3.0, max_value=7.0, value=5.303, step=0.1)
total_laps = st.number_input("Total Laps", min_value=40, max_value=80, value=58, step=1)

st.subheader("Enter Race Strategies")
num_stints = st.number_input("Number of Stints", min_value=1, max_value=5, value=2, step=1)

strategy = []
for i in range(num_stints):
    tyre_choice = st.selectbox(f"Tyre for Stint {i+1}", options=["Soft", "Medium", "Hard"], key=f"tyre_{i}")
    stint_laps = st.number_input(f"Laps on {tyre_choice}", min_value=1, max_value=total_laps, value=20, step=1, key=f"laps_{i}")
    strategy.append((tyre_choice, stint_laps))

if st.button("Analyze Strategy"):
    total_time, pit_stops = calculate_race_time(strategy, total_laps)
    st.write(f"### Strategy Results")
    st.write(f"Total Race Time: {total_time:.2f} seconds")
    st.write(f"Number of Pit Stops: {pit_stops}")

    # Visualization
    labels = [f"Stint {i+1}\n({tyre}, {laps} laps)" for i, (tyre, laps) in enumerate(strategy)]
    times = [TYRE_PERFORMANCE[tyre]["pace"] * laps for tyre, laps in strategy]
    
    fig, ax = plt.subplots()
    ax.bar(labels, times, color=["red", "yellow", "blue"][:len(labels)])
    ax.set_ylabel("Total Time (seconds)")
    ax.set_title("Race Strategy Breakdown")
    st.pyplot(fig)
