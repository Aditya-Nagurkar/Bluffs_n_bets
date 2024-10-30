import streamlit as st
import random

# Title for the game setup
st.title("Liar's Dice Game Setup")

# Get number of players
num_players = st.number_input("Enter the number of players:", min_value=1, max_value=10, step=1, key="num_players")

# Input names and set checkboxes for each player
players = []  # List to store player names
for i in range(int(num_players)):
    name = st.text_input(f"Enter name for Player {i + 1}:", key=f"name_{i}")
    if name:
        players.append(name)
        # Display 6 checkboxes for each player
        for j in range(6):
            st.checkbox(f"{name}'s Dice {j + 1}", key=f"checkbox_{i}_{j}")

# Step 2: Deal a random card and show result
if st.button("Show Card"):
    card_options = ["King", "Queen", "Ace"]
    dealt_card = random.choice(card_options)
    st.write(f"The card is: **{dealt_card}**")