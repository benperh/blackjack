import unittest
from unittest.mock import patch, MagicMock
import pygame
import sys
import random
from blackjackfinal import Card, Deck, Hand, values, ranks, suits

class TestBlackjack(unittest.TestCase):
    
    def setUp(self):
        """Initialize test objects"""
        pygame.init()  # Needed for font operations
        self.card = Card('A', 'Hearts')
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        
    def test_card_creation(self):
        """Test Card class initialization"""
        self.assertEqual(self.card.rank, 'A')
        self.assertEqual(self.card.suit, 'Hearts')
        self.assertEqual(str(self.card), 'A of Hearts')
        
    def test_deck_initialization(self):
        """Test Deck contains 52 unique cards"""
        self.assertEqual(len(self.deck.cards), 52)
        unique_cards = set((card.rank, card.suit) for card in self.deck.cards)
        self.assertEqual(len(unique_cards), 52)
        
    def test_hand_value_calculation(self):
        """Test hand value calculation with and without Aces"""
        # Test regular cards
        self.player_hand.add_card(Card('7', 'Diamonds'))
        self.player_hand.add_card(Card('K', 'Clubs'))
        self.assertEqual(self.player_hand.hand_value(), 17)
        
        # Test Ace as 11
        self.player_hand.add_card(Card('A', 'Spades'))
        self.assertEqual(self.player_hand.hand_value(), 18)  # 7 + 10 + 1 (Ace soft)
        
        # Test Ace as 1 when needed
        self.player_hand.add_card(Card('A', 'Hearts'))
        self.assertEqual(self.player_hand.hand_value(), 19)  # 7 + 10 + 1 + 1
        
    def test_card_values_dictionary(self):
        """Test the card values dictionary"""
        self.assertEqual(values['2'], 2)
        self.assertEqual(values['10'], 10)
        self.assertEqual(values['J'], 10)
        self.assertEqual(values['Q'], 10)
        self.assertEqual(values['K'], 10)
        self.assertEqual(values['A'], 11)
        
    def test_deck_shuffling(self):
        """Test that deck shuffling changes card order"""
        original_order = [(card.rank, card.suit) for card in self.deck.cards]
        self.deck.shuffle()
        new_order = [(card.rank, card.suit) for card in self.deck.cards]
        self.assertNotEqual(original_order, new_order)
        self.assertEqual(set(original_order), set(new_order))  # Same cards, different order
        
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()

if __name__ == '__main__':
    unittest.main()