# Imports.
from optparse import Values
import random
import os
import sys
import time
from tkinter import Y

# Variables containing the deck
deck_dict = {'♥A':11, '♦A':11, '♣A':11, '♠A':11,'♥K':10, '♦K':10, '♣K':10, '♠K':10, '♥Q':10, '♦Q':10, '♣Q':10, '♠Q':10, '♥J':10, '♦J':10, '♣J':10, '♠J':10, '♥10':10, '♦10':10, '♣10':10, '♠10':10, '♥9':9, '♦9':9, '♣9':9, '♠9':9, '♥8':8, '♦8':8, '♣8':8, '♠8':8, '♥7':7, '♦7':7, '♣7':7, '♠7':7, '♥6':6, '♦6':6, '♣6':6, '♠6':6, '♥5':5, '♦5':5, '♣5':5, '♠5':5, '♥4':4, '♦4':4, '♣4':4, '♠4':4, '♥3':3, '♦3':3, '♣3':3, '♠3':3, '♥2':2, '♦2':2, '♣2':2, '♠2':2}
deck_cards = list(deck_dict.keys())

# Init variables for the player's wallet and pot value
player_funds = 0.00
pot_value = 0.00

# FUNCTIONS

# Shuffles the deck.  Returns a list of the keys from deck_dict in a shuffled order.
def shuffle_deck(cards):
    shuffled_deck = cards
    random.shuffle(shuffled_deck)
    return shuffled_deck

# Clears the terminal and print the game logo.
def game_logo():

    os.system('cls' if os.name == 'nt' else 'clear')
    print("===========================================")
    print("= ♥ ♦ ♣ ♠   B L A C K J A C K !   ♥ ♦ ♣ ♠ =")
    print("===========================================")
    print("")

# Prompts user for playing a new game.  Returns a boolean.
def new_game():
    loop_active = True
    while loop_active:
        print("")
        user_input = input("Would you like to start a new game? (Y/N):  ")
        # If yes
        if (user_input == 'Y') or (user_input == 'y') or (user_input == 'Yes') or (user_input == 'yes'):
            return True
            loop_active = False
            break
        # If no
        elif (user_input == 'N') or (user_input == 'n') or (user_input == 'No') or (user_input == 'no'):
            return False
            loop_active = False
            break
        else:
            print("Invalid input received, please try again...")
            print("")

# Executes first deal of the game.  Returns the active deck for the game, player hand, and dealer hand as a tuple.
def deal_me_in(cards):
    active_deck = cards
    player_hand = []
    dealer_hand = []
    card_count = 0
    while (card_count < 4):
        player_hand.append(active_deck[0])
        del active_deck[0]
        card_count = card_count + 1
        dealer_hand.append(active_deck[0])
        del active_deck[0]
        card_count = card_count + 1
    return (active_deck, player_hand, dealer_hand)

# Check a hand's value, automatically calculates if an ace is worth 1 or 11.  Returns value as an int.
def calculate_hand(hand, deck_dictionary):
    current_hand = hand
    card_values = deck_dictionary
    hand_value = 0
    
    # Iterate through each card in current_hand, retrieve their values from card_values.
    for card in current_hand:
        hand_value = hand_value + card_values.get(card)
    
    # Logic for decreasing ace value to 1 if hand value is over 21
    if (hand_value > 21) and ("♥A" in current_hand):
        hand_value = hand_value - 10
    elif (hand_value > 21) and ("♦A" in current_hand):
        hand_value = hand_value - 10
    elif (hand_value > 21) and ("♣A" in current_hand):
        hand_value = hand_value - 10
    elif (hand_value > 21) and ("♠A" in current_hand):
        hand_value = hand_value - 10
    else:
        pass

    return hand_value

# Functionality that takes cards from the remaining deck and applies them to a hand.
def hit_logic(hand, deck):
    current_hand = hand
    remaining_cards = deck
    current_hand.append(remaining_cards[0])
    del remaining_cards[0]
    return current_hand, remaining_cards
        
# Collects bets.
def place_bets(player_funds):
    loop_active = True

    while loop_active == True:
        print(f"You have ${player_funds} available.")
        player_bet = input("How much would you like to bet on this round?  ")

        # Convert input to float.
        player_bet = float(player_bet)

        # Make sure the player isn't betting more than they have.
        if (player_bet > player_funds):
            print("You do not have enough funds for that bet, please try again.")

        else:
            print(f"Really bet ${player_bet}?")
            confirm_bet = input("(Y/N):  ")

            if (confirm_bet == 'Y') or (confirm_bet == 'y') or (confirm_bet == 'Yes') or (confirm_bet == 'yes'):
                loop_active = False
                print("Bet placed.")
                pot = (player_bet * 2)
                return pot

            elif (confirm_bet == 'N') or (confirm_bet == 'n') or (confirm_bet == 'No') or (confirm_bet == 'no'):
                player_bet = 0.00
    
            else:
                print("Invalid input received, please try again.")

# Dealer turn Logic function
def dealer_turn(dealer_hand, dealer_score, deck):
    current_hand = dealer_hand
    current_score = dealer_score
    remaining_cards = deck
    turn_active = True

    while turn_active == True:
        if (dealer_score < 17):
            turn_variables = hit_logic(current_hand, remaining_cards)
            # Update hand and score
            current_hand = turn_variables[0]
            remaining_cards = turn_variables[1]
            time.sleep(0.5)

                # Calculate and update score
            current_score = calculate_hand(current_hand, deck_dict)

            # Print each cycle's results
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Dealer's turn...")
            print(f"Dealer's hand:  {current_hand}")
            print(f"Dealer's score:  {current_score}")

            if (current_score >= 17) and (current_score <= 20):
                print(f"Dealer stays at {current_score}.")
                turn_active = False
                time.sleep(1)
                return current_score, remaining_cards
    
            elif (current_score == 21):
                print("Dealer scores 21.")
                turn_active = False
                time.sleep(1)
                return current_score, remaining_cards
    
            elif (current_score > 21):
                print(f"{current_score}, Dealer busts.")
                turn_active = False
                time.sleep(1)
                return current_score, remaining_cards
        
            else:
                pass

        elif (current_score == 21):
            print("Dealer scores 21.")
            turn_active = False
            time.sleep(1)
            return current_score, remaining_cards

        else:
            print("Dealer's turn...")
            print(f"Dealer's hand:  {current_hand}")
            print(f"Dealer stays at {current_score}")
            turn_active = False
            time.sleep(1)
            return current_score, remaining_cards

# Player turn logic function
def player_turn(player_hand, player_score, dealer_hand, dealer_score, deck):
    current_hand = player_hand
    current_score = player_score
    remaining_cards = deck
    turn_active = True 
    while turn_active == True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Player's turn...")
        print(f"Player's hand:  {current_hand}")
        print(f"Hand's value is:  {current_score}")
        print("")
        print(f"Dealer's hand:  {dealer_hand}")
        print(f"Dealer's hand's's value is:  {dealer_score}")

        print("")
        
        # If player scores 21 print Blackjack message, end turn, return score.
        if (current_score == 21):
            print("Player scores 21.  Blackjack!!")
            turn_active = False
            time.sleep(1)
            return current_score, remaining_cards

        # If player scores over 21 print Bust message, end turn, return score.
        elif (current_score > 21):
            print(f"Player scores {current_score}.  Player busts.")
            turn_active = False
            time.sleep(1)
            return current_score, remaining_cards

        # If player scores less than 21 allow them to hit then update hand, score, and remaining cards in deck.
        elif (current_score < 21):
            player_hits = input("Would you like to hit?(Y/N):  ")

            # If player wants to hit
            if (player_hits == 'Y') or (player_hits == 'y') or (player_hits == 'Yes') or (player_hits == 'yes'):
                turn_variables = hit_logic(current_hand, remaining_cards)
                # Update hand and score
                current_hand = turn_variables[0]
                remaining_cards = turn_variables[1]
                time.sleep(1)

                # Calculate and update score
                current_score = calculate_hand(current_hand, deck_dict)
            
            # If player wants to stay
            elif (player_hits == 'N') or (player_hits == 'n') or (player_hits == 'No') or (player_hits == 'no'):
                print(f"Player stands at {current_score}.")
                time.sleep(1)
                turn_active = False
                return current_score, remaining_cards

            # If player inputs something other than yes or no
            else:
                print("Invalid input received, please try again.")
                time.sleep(0.5)


        else:
            pass

# Round result calculation, returns True if player wins, False if player loses.
def round_result(player_score, dealer_score):
    
    # If player busts - return False
    if (player_score > 21):
        print("Player loses.")
        time.sleep(1)
        return False
    
    # If dealer busts but player doesn't - return True
    elif (player_score <= 21) and (dealer_score > 21):
        print('Player wins.')
        time.sleep(1)
        return True
    
    # If nobody busts and dealer scores higher than player - return False
    elif (player_score <= 20) and (dealer_score <= 21) and (player_score < dealer_score):
        print("Player loses.")
        time.sleep(1)
        return False
    
    # If nobody busts and player scores higher than or equal to dealer - return True
    elif (player_score <= 21) and (dealer_score <= 21) and (player_score >= dealer_score):
        print('Player wins.')
        time.sleep(1)
        return True
    
    else:
        pass

# End of round balance calculaton - returns balance and game over status
def calculate_balance(round_result, player_funds, pot_value):

    # If player wins add half of the pot value to player's funds
    if (round_result == True):
        current_funds = (player_funds + (pot_value / 2))
        print(f"Player's new balance is ${current_funds}.")
        gameover = False
        time.sleep(1)
        return current_funds, gameover
    # If player loses subtract half the pot value to the player's funds.
    else:
        current_funds = (player_funds - (pot_value / 2))
        print(f"Player's new balance is ${current_funds}.")
        if (current_funds < 0.01):
            gameover = True
        else:
            gameover = False
        
        return current_funds, gameover


# Game Over screen function
def gameover(gameover_status):
    if (gameover_status == True):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Player has run out of funds.")
        print("")
        print("")
        print("GAME OVER.")
        time.sleep(1)
    
    else:
        pass

# Play again prompt
def play_again():
    play = input("Would you like to play again?(Y/N):  ")
    if (play == 'Y') or (play == 'y') or (play == 'Yes') or (play == 'yes'):
        return True
    
    elif (play == 'N') or (play == 'n') or (play == 'No') or (play == 'no'):
        return False
    
    else:
        print("Invalid input received, please try again.")


# Gameplay  Function
def play_blackjack():
    
    # Print logo, ask if they want to start a new game
    game_logo()
    game_active = new_game()
    
    # Initialize gameplay variables upon new game launch
    if (game_active == True):
        player_funds = 100.00
        player_score = 0
        dealer_score = 0
        pot_value = 0
        quit_game = False
    else:
        pass

    # While game is active run gameplay loop.
    while (game_active == True):
        if(quit_game == True):
            sys.exit()
        else:
                # 1.  Shuffle the deck at the beginning of every loop.
                active_deck = shuffle_deck(deck_cards)

                #2.  Prompt user to place their bets
                os.system('cls' if os.name == 'nt' else 'clear')
                pot_value = place_bets(player_funds)

                #3.  Deal
                os.system('cls' if os.name == 'nt' else 'clear')
                game_start = deal_me_in(active_deck)
                deck_after_deal = game_start[0]
                player_hand = game_start[1]
                dealer_hand = game_start[2]

                #4.  Calculate scores from first hands dealt
                player_score = calculate_hand(player_hand, deck_dict)
                dealer_score = calculate_hand(dealer_hand, deck_dict)

                #5.  Player's turn
                os.system('cls' if os.name == 'nt' else 'clear')
                players_turn = player_turn(player_hand, player_score, dealer_hand, dealer_score, deck_after_deal)
                player_score = players_turn[0]
                deck_after_player = players_turn[1]

                #6.  Dealer's turn occurs if the player has not busted or scored blackjack.
                if(player_score >= 21):
                    dealer_score = 1
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    dealers_turn = dealer_turn(dealer_hand, dealer_score, deck_after_player)
                    dealer_score = dealers_turn[0]
                    time.sleep(1)
                    # deck_after_dealer = dealer_turn[1]

                #7 Determine if the player won or lost
                os.system('cls' if os.name == 'nt' else 'clear')
                player_won = round_result(player_score, dealer_score)

                #8 Update player balance, determine game over status
                round_calculation = calculate_balance(player_won, player_funds, pot_value)
                gameover = round_calculation[1]
                player_funds = round_calculation[0]
                if (player_funds < 0.01):
                    print("Player has run out of funds.")
                    print("")
                    print("")
                    print("GAME OVER.")
                    time.sleep(3)
                    os.system('cls' if os.name == 'nt' else 'clear')
            

                # Check for game over, if true end game.  If false prompt to continue
                if (gameover == True):
                    sys.exit()
        
                else:
                    cont_prompt = play_again()
                    if (cont_prompt == False):
                        sys.exit()
                    else:
                        pass
    

        



















play_blackjack()