# Welcome to Blackjack!

A simple Blackjack game built using Python and Pygame. The goal of Blackjack is to have a hand value as close to 21 as possible, without exceeding 21. 
The player competes against the dealer, and the player wins if their hand value is higher than the dealer's, or if the dealer busts (goes over 21). The player can place a bet before each turn.

## Instructions
1. Clone the repository.
2. Run the `blackjackfinal.py` script using Python.
3. Ensure you have Pygame installed, have the card deck, and the 4 mp3 files included in the repo.
4. Enjoy the game!

## Tests
Run blackjackfinaltest.py to perform multiple tests.
The tests ensure the following:
1. The Card class is correctly initialized
2. The Deck class creates a 52-card deck
3. The Hand class properly calculates card values, including when an ace is counted as an 11 or 1
4. The values dictionary assigns each card with the correct numerical value
5. The Deck.shuffle() method randomizes card order
