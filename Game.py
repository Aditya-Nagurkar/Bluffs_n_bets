import streamlit as st
import random

# Initialize or reset game state
if "player_dice" not in st.session_state:
    st.session_state.player_dice = [random.randint(1, 6) for _ in range(5)]
    st.session_state.computer_dice = [random.randint(1, 6) for _ in range(5)]
    st.session_state.turn = "Player"
    st.session_state.player_guess = None
    st.session_state.message = "Game Start! Make your first guess."

# Helper function to get total dice count
def get_total_dice_count(guess_number):
    return st.session_state.player_dice.count(guess_number) + st.session_state.computer_dice.count(guess_number)

# Display game instructions
st.title("Liar's Dice - Simplified Version")
st.write("This is a simplified, single-player version of Liar's Dice where you play against the computer.")
st.write("**Instructions**:")
st.write("1. Guess the total number of a specific face (1-6) among both your and the computer's dice.")
st.write("2. The computer will either raise your guess or call you a liar.")
st.write("3. If the computer calls you a liar, the dice are revealed and the winner is determined.")

# Show player's dice
st.write(f"Your dice: {st.session_state.player_dice}")

# Input for player's guess
guess_face = st.selectbox("Choose a dice face (1-6):", [1, 2, 3, 4, 5, 6])
guess_count = st.number_input("Guess the total count of this face:", min_value=1, max_value=10, step=1)

# Submit player's guess
if st.button("Submit Guess"):
    st.session_state.player_guess = (guess_face, guess_count)
    st.session_state.turn = "Computer"
    st.session_state.message = f"You guessed {guess_count} dice showing {guess_face}. The computer's turn."

# Display game message
st.write(st.session_state.message)

# Computer's turn logic
if st.session_state.turn == "Computer" and st.session_state.player_guess:
    player_face, player_count = st.session_state.player_guess
    actual_count = get_total_dice_count(player_face)
    
    # Computer decides whether to raise or call
    if player_count < actual_count + random.randint(0, 2):
        st.session_state.message = f"Computer raises your bet to {player_count + 1} dice showing {player_face}."
        st.session_state.turn = "Player"
    else:
        st.session_state.message = f"Computer calls you a liar!"
        
        # Reveal dice and determine the outcome
        st.write(f"Actual dice count for {player_face}: {actual_count}")
        if actual_count >= player_count:
            st.write("You were right! The computer loses a die.")
            if len(st.session_state.computer_dice) > 1:
                st.session_state.computer_dice.pop()
            else:
                st.write("You win! The computer has no more dice.")
                st.session_state.turn = None
        else:
            st.write("The computer was right! You lose a die.")
            if len(st.session_state.player_dice) > 1:
                st.session_state.player_dice.pop()
            else:
                st.write("Game over. The computer wins!")
                st.session_state.turn = None
        
        # Reset for the next round
        st.session_state.player_guess = None
        st.session_state.turn = "Player"
        st.session_state.player_dice = [random.randint(1, 6) for _ in range(len(st.session_state.player_dice))]
        st.session_state.computer_dice = [random.randint(1, 6) for _ in range(len(st.session_state.computer_dice))]

# Restart button
if st.button("Restart Game"):
    st.session_state.player_dice = [random.randint(1, 6) for _ in range(5)]
    st.session_state.computer_dice = [random.randint(1, 6) for _ in range(5)]
    st.session_state.turn = "Player"
    st.session_state.player_guess = None
    st.session_state.message = "Game Start! Make your first guess."
