import streamlit as st
import random

# Title for the game setup
st.title("Liar's Dice Game")

# Initialize player names in session state if not already initialized
if 'players' not in st.session_state:
    st.session_state.players = []

# Get the number of players
num_players = st.number_input("Enter the number of players:", min_value=1, max_value=10, step=1)

# Adjust the player list size based on num_players input
if len(st.session_state.players) < num_players:
    st.session_state.players.extend([""] * (num_players - len(st.session_state.players)))
elif len(st.session_state.players) > num_players:
    st.session_state.players = st.session_state.players[:num_players]

# Input player names and display checkboxes for each player in a horizontal layout
for i in range(num_players):
    # Display player name input and delete button in a row
    col1, col2 = st.columns([4, 1])
    with col1:
        st.session_state.players[i] = st.text_input(f"Enter name for Player {i + 1}:", value=st.session_state.players[i], key=f"name_{i}")
    with col2:
        if st.button("Delete", key=f"delete_{i}"):
            st.session_state.players.pop(i)
            st.experimental_rerun()  # Refresh the app to reflect changes

    # Display six checkboxes in a row using st.columns
    cols = st.columns(6)
    for j in range(6):
        cols[j].checkbox(" ", key=f"checkbox_{i}_{j}", label_visibility="collapsed")

# Display a random card table name when button is clicked
if st.button("Show"):
    card_table_options = ["King's Table", "Queen's Table", "Ace's Table"]
    dealt_card_table = random.choice(card_table_options)
    st.write(f"**{dealt_card_table}**")

# Russian Roulette section below the existing game content


# Russian Roulette functionality
if st.button("Pull the Trigger"):
    # Simulate bullet outcome (1 in 6 chance for the bullet to fire)
    bullet_chamber = random.randint(1, 6)  # The chamber with the bullet
    trigger_pull = random.randint(1, 6)     # The chamber being pulled

    if bullet_chamber == trigger_pull:
        st.write("💥 **Bang! The bullet fired! You are out!**")
    else:
        st.write("🔫 **Click! You are safe!**")