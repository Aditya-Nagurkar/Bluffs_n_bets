import streamlit as st
import random
from collections import Counter
import time
import json
from pathlib import Path
import base64

def local_css():
    st.markdown("""
    <style>
        .dice-container {
            display: flex;
            gap: 10px;
            margin: 10px 0;
            flex-wrap: wrap;
        }
        .dice {
            width: 50px;
            height: 50px;
            background: white;
            border-radius: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 24px;
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border: 2px solid #333;
        }
        .player-card {
            background: #2c3e50;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            color: white;
        }
        .active-player {
            border: 3px solid #e74c3c;
        }
        .bid-history {
            max-height: 200px;
            overflow-y: auto;
            background: #34495e;
            padding: 10px;
            border-radius: 5px;
        }
        .game-controls {
            background: #34495e;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .eliminated {
            opacity: 0.5;
        }
        .stButton button {
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }
        .call-bluff button {
            background-color: #e74c3c !important;
        }
        .dice-shake {
            animation: shake 0.5s ease-in-out;
        }
        @keyframes shake {
            0% { transform: rotate(0deg); }
            25% { transform: rotate(-10deg); }
            50% { transform: rotate(10deg); }
            75% { transform: rotate(-5deg); }
            100% { transform: rotate(0deg); }
        }
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    defaults = {
        'game_started': False,
        'current_player': 0,
        'dice': {},
        'last_bid': {'quantity': 0, 'value': 0},
        'player_count': 2,
        'game_over': False,
        'dice_per_player': 5,
        'eliminated_players': set(),
        'bid_history': [],
        'player_names': {},
        'shake_dice': False,
        'animations_complete': False,
        'round_number': 1,
        'player_stats': {},
        'game_mode': 'normal',  # normal or tournament
        'tournament_scores': {},
        'sound_enabled': True
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_player_avatar(player_index):
    # Generate consistent colorful avatars based on player index
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f1c40f', '#9b59b6', '#e67e22']
    return f"""
    <div style="
        width: 40px;
        height: 40px;
        background-color: {colors[player_index % len(colors)]};
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-weight: bold;
        font-size: 20px;
    ">
        {player_index + 1}
    </div>
    """

def display_dice(dice_values, shake=False):
    dice_html = '<div class="dice-container">'
    for value in dice_values:
        shake_class = "dice-shake" if shake else ""
        dice_html += f'<div class="dice {shake_class}">{value}</div>'
    dice_html += '</div>'
    return dice_html

def roll_dice(num_dice):
    return [random.randint(1, 6) for _ in range(num_dice)]

def check_bid(bid_quantity, bid_value):
    total_count = 0
    for player_dice in st.session_state.dice.values():
        count = Counter(player_dice)
        if st.session_state.game_mode == 'normal':
            # In normal mode, 1s are wild
            total_count += count[bid_value] + count[1]
        else:
            total_count += count[bid_value]
    return total_count >= bid_quantity

def start_new_game():
    st.session_state.game_started = True
    st.session_state.current_player = 0
    st.session_state.last_bid = {'quantity': 0, 'value': 0}
    st.session_state.game_over = False
    st.session_state.eliminated_players = set()
    st.session_state.bid_history = []
    st.session_state.round_number = 1
    st.session_state.shake_dice = True
    st.session_state.animations_complete = False
    
    # Initialize player stats
    st.session_state.player_stats = {
        i: {
            'successful_bluff_calls': 0,
            'failed_bluff_calls': 0,
            'times_caught_bluffing': 0
        } for i in range(st.session_state.player_count)
    }
    
    # Roll dice for each player
    st.session_state.dice = {
        i: roll_dice(st.session_state.dice_per_player) 
        for i in range(st.session_state.player_count)
    }

def display_game_stats():
    st.sidebar.header("Game Statistics")
    st.sidebar.write(f"Round: {st.session_state.round_number}")
    
    for player in range(st.session_state.player_count):
        if player not in st.session_state.eliminated_players:
            stats = st.session_state.player_stats[player]
            st.sidebar.markdown(f"""
            **Player {player + 1}**
            - Successful bluff calls: {stats['successful_bluff_calls']}
            - Failed bluff calls: {stats['failed_bluff_calls']}
            - Times caught bluffing: {stats['times_caught_bluffing']}
            """)

def next_player():
    next_player = (st.session_state.current_player + 1) % st.session_state.player_count
    while next_player in st.session_state.eliminated_players:
        next_player = (next_player + 1) % st.session_state.player_count
    st.session_state.current_player = next_player

def main():
    st.set_page_config(page_title="Liar's Dice", page_icon="🎲", layout="wide")
    local_css()
    init_session_state()
    
    col1, col2, col3 = st.columns([2,6,2])
    
    with col1:
        st.image("https://via.placeholder.com/150", caption="Liar's Dice")
        if not st.session_state.game_started:
            st.session_state.game_mode = st.radio(
                "Game Mode",
                ['normal', 'tournament'],
                format_func=lambda x: x.capitalize()
            )
    
    with col2:
        st.title("🎲 Liar's Dice")
        
        if not st.session_state.game_started:
            st.write("Welcome to Liar's Dice! Set up your game below.")
            
            col_setup1, col_setup2 = st.columns(2)
            with col_setup1:
                st.session_state.player_count = st.number_input(
                    "Number of players:", min_value=2, max_value=6, value=2
                )
            with col_setup2:
                st.session_state.dice_per_player = st.number_input(
                    "Dice per player:", min_value=1, max_value=5, value=5
                )
            
            # Player name inputs
            st.write("Enter player names (optional):")
            for i in range(st.session_state.player_count):
                st.session_state.player_names[i] = st.text_input(
                    f"Player {i+1} name:",
                    value=f"Player {i+1}",
                    key=f"player_name_{i}"
                )
            
            if st.button("Start Game", key="start_game"):
                start_new_game()
        
        else:
            # Game interface
            if not st.session_state.game_over:
                # Current player info
                current_player_name = st.session_state.player_names[st.session_state.current_player]
                st.markdown(f"### Current Turn: {current_player_name}")
                
                # Display dice for current player
                st.markdown("### Your Dice:")
                st.markdown(
                    display_dice(
                        st.session_state.dice[st.session_state.current_player],
                        st.session_state.shake_dice
                    ),
                    unsafe_allow_html=True
                )
                
                # Game controls
                st.markdown("### Make Your Move")
                with st.container():
                    col_bid1, col_bid2, col_bid3 = st.columns([2,2,3])
                    
                    with col_bid1:
                        new_quantity = st.number_input(
                            "Bid quantity:",
                            min_value=max(1, st.session_state.last_bid['quantity']),
                            value=max(1, st.session_state.last_bid['quantity'])
                        )
                    
                    with col_bid2:
                        new_value = st.number_input(
                            "Bid value (1-6):",
                            min_value=1,
                            max_value=6,
                            value=max(1, st.session_state.last_bid['value'])
                        )
                    
                    with col_bid3:
                        col_action1, col_action2 = st.columns(2)
                        with col_action1:
                            if st.button("Make Bid", key="make_bid"):
                                if new_quantity < st.session_state.last_bid['quantity'] or \
                                   (new_quantity == st.session_state.last_bid['quantity'] and 
                                    new_value <= st.session_state.last_bid['value']):
                                    st.error("Invalid bid! Must be higher than the last bid.")
                                else:
                                    st.session_state.last_bid = {
                                        'quantity': new_quantity,
                                        'value': new_value
                                    }
                                    st.session_state.bid_history.append({
                                        'player': current_player_name,
                                        'bid': f"{new_quantity} dice showing {new_value}"
                                    })
                                    next_player()
                        
                        with col_action2:
                            if st.session_state.last_bid['quantity'] > 0:
                                if st.button("Call Bluff!", key="call_bluff", type="primary"):
                                    is_correct = check_bid(
                                        st.session_state.last_bid['quantity'],
                                        st.session_state.last_bid['value']
                                    )
                                    
                                    # Show all dice
                                    st.markdown("### All Dice on the Table:")
                                    for player, dice in st.session_state.dice.items():
                                        player_name = st.session_state.player_names[player]
                                        st.markdown(
                                            f"**{player_name}:** " + 
                                            display_dice(dice, True),
                                            unsafe_allow_html=True
                                        )
                                    
                                    if is_correct:
                                        st.error("Wrong call! The bid was correct!")
                                        st.session_state.player_stats[st.session_state.current_player]['failed_bluff_calls'] += 1
                                        st.session_state.eliminated_players.add(st.session_state.current_player)
                                    else:
                                        st.success("Good call! The bid was a bluff!")
                                        prev_player = (st.session_state.current_player - 1) % st.session_state.player_count
                                        st.session_state.player_stats[st.session_state.current_player]['successful_bluff_calls'] += 1
                                        st.session_state.player_stats[prev_player]['times_caught_bluffing'] += 1
                                        st.session_state.eliminated_players.add(prev_player)
                                    
                                    # Check if game is over
                                    if len(st.session_state.eliminated_players) >= st.session_state.player_count - 1:
                                        st.session_state.game_over = True
                                        winner = next(i for i in range(st.session_state.player_count) 
                                                    if i not in st.session_state.eliminated_players)
                                        winner_name = st.session_state.player_names[winner]
                                        st.balloons()
                                        st.success(f"Game Over! {winner_name} wins! 🏆")
                                        
                                        if st.session_state.game_mode == 'tournament':
                                            if winner not in st.session_state.tournament_scores:
                                                st.session_state.tournament_scores[winner] = 0
                                            st.session_state.tournament_scores[winner] += 1
                                    else:
                                        # Start new round
                                        st.session_state.round_number += 1
                                        st.session_state.last_bid = {'quantity': 0, 'value': 0}
                                        st.session_state.dice = {
                                            i: roll_dice(st.session_state.dice_per_player)
                                            for i in range(st.session_state.player_count)
                                            if i not in st.session_state.eliminated_players
                                        }
                
                # Bid history
                st.markdown("### Bid History")
                for bid in reversed(st.session_state.bid_history[-5:]):
                    st.write(f"{bid['player']}: {bid['bid']}")
            
            if st.session_state.game_over:
                if st.button("Start New Game", key="new_game"):
                    start_new_game()
    
    with col3:
        display_game_stats()
        
        if st.session_state.game_mode == 'tournament':
            st.sidebar.markdown("### Tournament Scores")
            for player, score in st.session_state.tournament_scores.items():
                player_name = st.session_state.player_names[player]
                st.sidebar.write(f"{player_name}: {score} wins")

if __name__ == "__main__":
    main()</antArtifact>