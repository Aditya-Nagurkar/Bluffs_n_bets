import streamlit as st
import random

# Title for the game setup
st.title("Liar's Dice Game")

# Initialize session state variables
if 'players' not in st.session_state:
    st.session_state.players = []
if 'dice_values' not in st.session_state:
    st.session_state.dice_values = {}
if 'deleted_players' not in st.session_state:
    st.session_state.deleted_players = set()

# Get the number of players
num_players = st.number_input("Enter the number of players:", min_value=1, max_value=10, step=1)

# Adjust the player list size based on num_players input
if len(st.session_state.players) < num_players:
    st.session_state.players.extend([""] * (num_players - len(st.session_state.players)))
elif len(st.session_state.players) > num_players:
    st.session_state.players = st.session_state.players[:num_players]

# Enhanced player management with dice values
players_to_delete = []

# Create two columns for the main layout
main_col1, main_col2 = st.columns([2, 1])

with main_col1:
    # Player management section
    for i in range(num_players):
        if i not in st.session_state.deleted_players:
            # Create a container for each player's section
            player_container = st.container()
            
            # Player name and delete button row
            col1, col2 = player_container.columns([4, 1])
            with col1:
                st.session_state.players[i] = st.text_input(
                    f"Enter name for Player {i + 1}:",
                    value=st.session_state.players[i],
                    key=f"name_{i}"
                )
            with col2:
                if st.button("Delete", key=f"delete_{i}"):
                    st.session_state.deleted_players.add(i)
                    if i in st.session_state.dice_values:
                        del st.session_state.dice_values[i]

            # Enhanced checkbox layout with dice values
            checkbox_container = player_container.container()
            dice_cols = checkbox_container.columns(6)
            
            # Initialize dice values if not present
            if i not in st.session_state.dice_values:
                st.session_state.dice_values[i] = [False] * 6
            
            # Create checkboxes with dice values
            for j in range(6):
                dice_value = dice_cols[j].checkbox(
                    f"Dice {j+1}",
                    value=st.session_state.dice_values[i][j],
                    key=f"checkbox_{i}_{j}",
                    label_visibility="collapsed"
                )
                st.session_state.dice_values[i][j] = dice_value

            # Add dice roll button for each player
            if st.button("Roll Dice", key=f"roll_{i}"):
                st.session_state.dice_values[i] = [random.choice([True, False]) for _ in range(6)]

with main_col2:
    # Card table section with original options
    st.subheader("Card Table")
    card_table_options = ["King's Table", "Queen's Table", "Ace's Table"]
    
    if 'current_table' not in st.session_state:
        st.session_state.current_table = None
    
    if st.button("Show Card Table"):
        st.session_state.current_table = random.choice(card_table_options)
    
    if st.session_state.current_table:
        st.write(f"**{st.session_state.current_table}**")

# Russian Roulette section below the existing game content
st.subheader("Russian Roulette")

# Enhanced Russian Roulette functionality
if st.button("Pull the Trigger"):
    bullet_chamber = random.randint(1, 6)
    trigger_pull = random.randint(1, 6)
    
    # Create suspense with a progress bar
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)
    
    if bullet_chamber == trigger_pull:
        st.markdown("💥 **Bang! The bullet fired! You are out!**")
        st.balloons()
    else:
        st.markdown("🔫 **Click! You are safe!**")

# Add a reset button for the entire game
if st.button("Reset Game"):
    st.session_state.players = []
    st.session_state.dice_values = {}
    st.session_state.deleted_players = set()
    st.session_state.current_table = None
    st.rerun()