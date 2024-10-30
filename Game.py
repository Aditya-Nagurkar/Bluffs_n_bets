import streamlit as st
import random
from collections import Counter
import time

def init_session_state():
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'current_player' not in st.session_state:
        st.session_state.current_player = 0
    if 'dice' not in st.session_state:
        st.session_state.dice = {}
    if 'last_bid' not in st.session_state:
        st.session_state.last_bid = {'quantity': 0, 'value': 0, 'player': None}
    if 'player_count' not in st.session_state:
        st.session_state.player_count = 2
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'dice_per_player' not in st.session_state:
        st.session_state.dice_per_player = 5
    if 'eliminated_players' not in st.session_state:
        st.session_state.eliminated_players = set()
    if 'player_dice_counts' not in st.session_state:
        st.session_state.player_dice_counts = {}
    if 'ai_difficulty' not in st.session_state:
        st.session_state.ai_difficulty = 'Medium'
    if 'game_mode' not in st.session_state:
        st.session_state.game_mode = 'Player vs AI'
    if 'bid_history' not in st.session_state:
        st.session_state.bid_history = []
    if 'round_number' not in st.session_state:
        st.session_state.round_number = 1

def get_ai_move(dice_count, last_bid, difficulty):
    if last_bid['quantity'] == 0:
        # Initial bid
        return {'quantity': 1, 'value': random.randint(1, 6)}
    
    if difficulty == 'Easy':
        # Simple increment of last bid
        if last_bid['value'] < 6:
            return {'quantity': last_bid['quantity'], 'value': last_bid['value'] + 1}
        else:
            return {'quantity': last_bid['quantity'] + 1, 'value': 1}
    
    elif difficulty == 'Medium':
        # More strategic bidding based on own dice
        own_dice = st.session_state.dice[st.session_state.current_player]
        dice_counts = Counter(own_dice)
        
        # Count ones (wild) separately
        wild_count = dice_counts[1]
        
        # Find the most common non-wild value
        most_common_value = max(range(2, 7), key=lambda x: dice_counts[x])
        most_common_count = dice_counts[most_common_value] + wild_count
        
        if random.random() < 0.7:  # 70% chance to make a "safe" bid
            if most_common_count >= last_bid['quantity']:
                return {'quantity': last_bid['quantity'], 
                       'value': most_common_value}
            else:
                # Call bluff if the bid seems too high
                return None
        else:
            # Make a slightly risky bid
            return {'quantity': last_bid['quantity'] + 1, 
                   'value': random.randint(1, 6)}

def roll_dice(num_dice):
    return [random.randint(1, 6) for _ in range(num_dice)]

def check_bid(bid_quantity, bid_value):
    total_count = 0
    for player_dice in st.session_state.dice.values():
        count = Counter(player_dice)
        # Count exact matches and ones (wild)
        total_count += count[bid_value] + count[1]
    return total_count >= bid_quantity

def start_new_round():
    # Roll new dice for remaining players
    st.session_state.dice = {
        i: roll_dice(st.session_state.player_dice_counts[i])
        for i in range(st.session_state.player_count)
        if i not in st.session_state.eliminated_players
    }
    st.session_state.last_bid = {'quantity': 0, 'value': 0, 'player': None}
    st.session_state.round_number += 1

def start_new_game():
    st.session_state.game_started = True
    st.session_state.current_player = 0
    st.session_state.last_bid = {'quantity': 0, 'value': 0, 'player': None}
    st.session_state.game_over = False
    st.session_state.eliminated_players = set()
    st.session_state.round_number = 1
    st.session_state.bid_history = []
    
    # Initialize dice counts for each player
    st.session_state.player_dice_counts = {
        i: st.session_state.dice_per_player 
        for i in range(st.session_state.player_count)
    }
    
    # Initial dice roll
    st.session_state.dice = {
        i: roll_dice(st.session_state.dice_per_player)
        for i in range(st.session_state.player_count)
    }

def main():
    st.title("🎲 Liar's Dice")
    
    init_session_state()
    
    if not st.session_state.game_started:
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.game_mode = st.selectbox(
                "Game Mode",
                ['Player vs AI', 'Player vs Player']
            )
            
            if st.session_state.game_mode == 'Player vs AI':
                st.session_state.ai_difficulty = st.selectbox(
                    "AI Difficulty",
                    ['Easy', 'Medium', 'Hard']
                )
                st.session_state.player_count = 2
            else:
                st.session_state.player_count = st.number_input(
                    "Number of players",
                    min_value=2,
                    max_value=4,
                    value=2
                )
        
        with col2:
            st.session_state.dice_per_player = st.number_input(
                "Dice per player",
                min_value=1,
                max_value=5,
                value=5
            )
        
        if st.button("Start Game"):
            start_new_game()
    
    else:
        # Game interface
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"Round {st.session_state.round_number}")
            
            # Show current player's dice
            current_player = "Your" if st.session_state.current_player == 0 else f"Player {st.session_state.current_player + 1}'s"
            st.write(f"{current_player} turn")
            
            if st.session_state.current_player == 0 or st.session_state.game_mode == 'Player vs Player':
                st.write("Your dice:", st.session_state.dice[st.session_state.current_player])
                
                # Show last bid if any
                if st.session_state.last_bid['quantity'] > 0:
                    st.write(f"Last bid: {st.session_state.last_bid['quantity']} dice showing {st.session_state.last_bid['value']}")
                
                # Bid controls
                col_bid1, col_bid2, col_bid3 = st.columns(3)
                
                with col_bid1:
                    quantity = st.number_input(
                        "Quantity",
                        min_value=max(1, st.session_state.last_bid['quantity']),
                        value=max(1, st.session_state.last_bid['quantity'])
                    )
                
                with col_bid2:
                    value = st.number_input(
                        "Value",
                        min_value=1,
                        max_value=6,
                        value=max(1, st.session_state.last_bid['value'])
                    )
                
                with col_bid3:
                    if st.button("Make Bid"):
                        if quantity < st.session_state.last_bid['quantity'] or \
                           (quantity == st.session_state.last_bid['quantity'] and 
                            value <= st.session_state.last_bid['value']):
                            st.error("Invalid bid! Must be higher than the last bid.")
                        else:
                            st.session_state.last_bid = {
                                'quantity': quantity,
                                'value': value,
                                'player': st.session_state.current_player
                            }
                            st.session_state.bid_history.append(
                                f"Player {st.session_state.current_player + 1}: {quantity} {value}s"
                            )
                            st.session_state.current_player = (st.session_state.current_player + 1) % st.session_state.player_count
                
                if st.session_state.last_bid['quantity'] > 0:
                    if st.button("Call Bluff!", type="primary"):
                        is_correct = check_bid(
                            st.session_state.last_bid['quantity'],
                            st.session_state.last_bid['value']
                        )
                        
                        # Show all dice
                        st.write("All dice:")
                        for p, dice in st.session_state.dice.items():
                            st.write(f"Player {p + 1}:", dice)
                        
                        loser = st.session_state.current_player if is_correct else st.session_state.last_bid['player']
                        st.session_state.player_dice_counts[loser] -= 1
                        
                        if st.session_state.player_dice_counts[loser] == 0:
                            st.session_state.eliminated_players.add(loser)
                            if len(st.session_state.eliminated_players) == st.session_state.player_count - 1:
                                winner = next(i for i in range(st.session_state.player_count) 
                                           if i not in st.session_state.eliminated_players)
                                st.success(f"Player {winner + 1} wins!")
                                st.session_state.game_over = True
                            else:
                                start_new_round()
                        else:
                            start_new_round()
            
            else:
                # AI turn
                st.write("AI is thinking...")
                time.sleep(1)  # Simulate AI thinking
                
                ai_move = get_ai_move(
                    st.session_state.player_dice_counts[st.session_state.current_player],
                    st.session_state.last_bid,
                    st.session_state.ai_difficulty
                )
                
                if ai_move is None:
                    # AI calls bluff
                    st.write("AI calls bluff!")
                    is_correct = check_bid(
                        st.session_state.last_bid['quantity'],
                        st.session_state.last_bid['value']
                    )
                    
                    # Show all dice
                    st.write("All dice:")
                    for p, dice in st.session_state.dice.items():
                        st.write(f"Player {p + 1}:", dice)
                    
                    loser = st.session_state.current_player if is_correct else st.session_state.last_bid['player']
                    st.session_state.player_dice_counts[loser] -= 1
                    
                    if st.session_state.player_dice_counts[loser] == 0:
                        st.session_state.eliminated_players.add(loser)
                        if len(st.session_state.eliminated_players) == st.session_state.player_count - 1:
                            winner = next(i for i in range(st.session_state.player_count) 
                                       if i not in st.session_state.eliminated_players)
                            st.success(f"Player {winner + 1} wins!")
                            st.session_state.game_over = True
                        else:
                            start_new_round()
                    else:
                        start_new_round()
                
                else:
                    # AI makes bid
                    st.write(f"AI bids {ai_move['quantity']} {ai_move['value']}s")
                    st.session_state.last_bid = {
                        'quantity': ai_move['quantity'],
                        'value': ai_move['value'],
                        'player': st.session_state.current_player
                    }
                    st.session_state.bid_history.append(
                        f"AI: {ai_move['quantity']} {ai_move['value']}s"
                    )
                    st.session_state.current_player = 0
        
        with col2:
            st.subheader("Game Status")
            for player in range(st.session_state.player_count):
                if player not in st.session_state.eliminated_players:
                    name = "You" if player == 0 and st.session_state.game_mode == 'Player vs AI' else f"Player {player + 1}"
                    st.write(f"{name}: {st.session_state.player_dice_counts[player]} dice")
            
            st.subheader("Bid History")
            for bid in reversed(st.session_state.bid_history[-5:]):
                st.write(bid)
        
        if st.session_state.game_over:
            if st.button("New Game"):
                start_new_game()

if __name__ == "__main__":
    main()