import streamlit as st
import random

# Title for the game setup
st.title("Liar's Dice Game")

# Get the number of players
num_players = st.number_input("Enter the number of players:", min_value=1, max_value=10, step=1)

# Input player names and store them in a session state list
if 'players' not in st.session_state:
    st.session_state.players = []

# Input for player names
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


# Initialize session state variables if they don't exist
if 'current_player_index' not in st.session_state:
    st.session_state.current_player_index = 0

if 'game_active' not in st.session_state:
    st.session_state.game_active = True

# Russian Roulette functionality
if st.session_state.game_active and st.button("Pull the Trigger"):
    # Get the current player
    if st.session_state.players:
        current_player = st.session_state.players[st.session_state.current_player_index]
        
        # Simulate bullet outcome (1 in 6 chance for the bullet to fire)
        bullet_chamber = random.randint(1, 6)  # The chamber with the bullet
        trigger_pull = random.randint(1, 6)     # The chamber being pulled

        if bullet_chamber == trigger_pull:
            st.write(f"💥 **Bang! The bullet fired! {current_player} is out!**")
            
            # Option to remove the current player
            if st.button(f"Remove {current_player} from the game"):
                st.session_state.players.remove(current_player)
                st.success(f"{current_player} has been removed from the game!")
                
                # Check if the game is still active
                if len(st.session_state.players) == 0:
                    st.session_state.game_active = False
                    st.write("All players are out!")
                else:
                    # Reset index if the current player was the last one
                    if st.session_state.current_player_index >= len(st.session_state.players):
                        st.session_state.current_player_index = 0  # Loop back to the first player
        else:
            st.write("🔫 **Click! You are safe!**")
        
        # Move to the next player for the next round
        st.session_state.current_player_index += 1
        if st.session_state.current_player_index >= len(st.session_state.players):
            st.session_state.current_player_index = 0  # Loop back to the first player

# Display remaining players
if st.session_state.players:
    st.write("Remaining players:", ", ".join(st.session_state.players))
else:
    st.write("All players are out!")