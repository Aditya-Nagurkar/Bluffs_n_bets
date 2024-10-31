import streamlit as st
import random

# Title for the game setup
st.title("Liar's Dice Game")

# Initialize player management in session state
if 'players' not in st.session_state:
    st.session_state.players = []

# Get the number of players
num_players = st.number_input("Enter the number of players:", min_value=1, max_value=10, step=1)

# Update players based on the number input
if len(st.session_state.players) < num_players:
    for i in range(len(st.session_state.players), num_players):
        st.session_state.players.append("")  # Add empty name slots for new players

# Input player names and display delete buttons
for i in range(num_players):
    col1, col2 = st.columns([4, 1])  # Two columns for name input and delete button
    with col1:
        name = st.text_input(f"Enter name for Player {i + 1}:", value=st.session_state.players[i], key=f"name_{i}")
        st.session_state.players[i] = name  # Update the player's name in the session state
    with col2:
        if st.button("Delete", key=f"delete_{i}"):
            st.session_state.players.pop(i)  # Remove the player from the list
            st.experimental_rerun()  # Refresh the app to reflect changes

# Display the list of players
st.write("Current Players:")
for player in st.session_state.players:
    st.write(player)

# Display six checkboxes for dice selections
dice_selections = {}
for i, player in enumerate(st.session_state.players):
    cols = st.columns(6)
    dice_selections[i] = []
    for j in range(6):
        if cols[j].checkbox(" ", key=f"checkbox_{i}_{j}", label_visibility="collapsed"):
            dice_selections[i].append(j + 1)  # Store selected dice values

# Show selected dice
if st.button("Show Selections"):
    for idx, selections in dice_selections.items():
        if selections:
            st.write(f"{st.session_state.players[idx]} selected dice: {', '.join(map(str, selections))}")
        else:
            st.write(f"{st.session_state.players[idx]} did not select any dice.")

# Display a random card table name when button is clicked
if st.button("Show Card Table"):
    card_table_options = ["King's Table", "Queen's Table", "Ace's Table"]
    dealt_card_table = random.choice(card_table_options)
    st.write(f"**{dealt_card_table}**")

# Russian Roulette section below the existing game content
st.subheader("Russian Roulette")

# Russian Roulette functionality
if st.button("Pull the Trigger"):
    bullet_chamber = random.randint(1, 6)  # The chamber with the bullet
    trigger_pull = random.randint(1, 6)     # The chamber being pulled

    if bullet_chamber == trigger_pull:
        st.write("💥 **Bang! The bullet fired! You are out!**")
    else:
        st.write("🔫 **Click! You are safe!**")