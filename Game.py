import streamlit as st
import random

# Title for the game setup
st.title("Liar's Dice Game")

# Get the number of players
num_players = st.number_input("Enter the number of players:", min_value=1, max_value=10, step=1)

# Input player names and store them in a session state list
if 'players' not in st.session_state:
    st.session_state.players = []

for i in range(int(num_players)):
    name = st.text_input(f"Enter name for Player {i + 1}:", key=f"name_{i}")
    if name and name not in st.session_state.players:
        st.session_state.players.append(name)

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

    if bullet_chamber == trigger_pull and st.session_state.players:
        st.write("💥 **Bang! The bullet fired!**")

        # Show option to delete a player
        player_to_remove = st.selectbox("Select a player to remove:", st.session_state.players)
        if st.button("Remove Player"):
            st.session_state.players.remove(player_to_remove)
            st.success(f"{player_to_remove} has been removed from the game!")
    else:
        st.write("🔫 **Click! You are safe!**")

# Display remaining players
if st.session_state.players:
    st.write("Remaining players:", ", ".join(st.session_state.players))
else:
    st.write("All players are out!")