import streamlit as st
import random

# Title for the game setup
st.title("Liar's Dice Game")

# Get the number of players
num_players = st.number_input("Enter the number of players:", min_value=1, max_value=10, step=1)

# Input player names and display checkboxes for each player in a horizontal layout
for i in range(int(num_players)):
    name = st.text_input(f"Enter name for Player {i + 1}:", key=f"name_{i}")
    

    # Display six checkboxes in a row using st.columns
    cols = st.columns(6)
    for j in range(6):
        cols[j].checkbox(f" ", key=f"checkbox_{i}_{j}", label_visibility="collapsed")

# Display a random card table name when button is clicked
if st.button("Show Card"):
    card_table_options = ["King's Table", "Queen's Table", "Ace's Table"]
    dealt_card_table = random.choice(card_table_options)
    st.write(f"**{dealt_card_table}**")