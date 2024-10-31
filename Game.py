Import streamlit as st
import random
import time

# Title for the game setup
st.title("Liar's Dice Game")

# Initialize session state variables
if 'players' not in st.session_state:
    st.session_state.players = []
if 'deleted_players' not in st.session_state:
    st.session_state.deleted_players = set()

# Get the number of players
num_players = st.number_input("Enter the number of players:", min_value=1, max_value=10, step=1)

# Adjust the player list size based on num_players input
if len(st.session_state.players) < num_players:
    st.session_state.players.extend([""] * (num_players - len(st.session_state.players)))
elif len(st.session_state.players) > num_players:
    st.session_state.players = st.session_state.players[:num_players]

# Enhanced player management
players_to_delete = []

# Create two columns for the main layout
main_col1, main_col2 = st.columns([2, 1])

with main_col1:
    # Player management section
    for i in range(num_players):
        if i not in st.session_state.deleted_players:
            # Player name and delete button in the same container
            name_row = st.container()
            
            # Use columns for name input and delete button
            name_col, delete_col = name_row.columns([4, 1])
            with name_col:
                st.session_state.players[i] = st.text_input(
                    f"Enter name for Player {i + 1}:",
                    value=st.session_state.players[i],
                    key=f"name_{i}",
                    label_visibility="visible"
                )
            with delete_col:
                # Add some vertical padding to align with the text input
                st.write("")  # This creates a small vertical space
                if st.button("Delete", key=f"delete_{i}", use_container_width=True):
                    st.session_state.deleted_players.add(i)
            
            # Enhanced checkbox layout
            checkbox_container = st.container()
            dice_cols = checkbox_container.columns(6)
            
            # Create checkboxes
            for j in range(6):
                dice_cols[j].checkbox(
                    f"Dice {j+1}",
                    key=f"checkbox_{i}_{j}",
                    label_visibility="collapsed"
                )

with main_col2:
    # Card table section with original options
    
    card_table_options = ["King's Table", "Queen's Table", "Ace's Table"]
    
    if 'current_table' not in st.session_state:
        st.session_state.current_table = None
    
    if st.button("Show"):
        st.session_state.current_table = random.choice(card_table_options)
    
    if st.session_state.current_table:
        st.write(f"**{st.session_state.current_table}**")

# Russian Roulette section below the existing game content


# Enhanced Russian Roulette functionality with explosion animation
if st.button("Pull the Trigger"):
    bullet_chamber = random.randint(1, 6)
    trigger_pull = random.randint(1, 6)
    
    # Create suspense with a progress bar
    progress_text = st.empty()
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)
    
    # Result container
    result_container = st.empty()
    
    if bullet_chamber == trigger_pull:
        # Explosion animation sequence
        explosion_frames = [
            "💥 *BANG!*",
            "✨ *BANG!* ✨",
            "💥 *BANG!* 💥",
            "✨ *BANG!* ✨",
            "⚡️ *BANG!* ⚡️",
            "💥 *BANG!* 💥",
            "🔥 **BANG! The bullet fired! You are out!** 🔥",
            "💥 **BANG! The bullet fired! You are out!** 💥",
            "⚡️ **BANG! The bullet fired! You are out!** ⚡️"
        ]
        
        for frame in explosion_frames:
            result_container.markdown(frame)
            time.sleep(0.1)
    else:
        result_container.markdown("🔫 **Click! You are safe!**")

This is my streamlit code