import random
import sys
import pygame
import pygame.font

# Initialize Pygame
pygame.init()
pygame.font.init()

# Load and play background music
try:
    pygame.mixer.music.load("funjazz.mp3")
    pygame.mixer.music.play(-1, 0.0)
    chip_sound = pygame.mixer.Sound("chip.mp3")
    win_sound = pygame.mixer.Sound("win.mp3")
    lose_sound = pygame.mixer.Sound("lose.mp3")
except:
    print("Could not load music file")
    chip_sound = None
    print("Could not load chip sound")
    print("Could not load lose sound")
    lose_sound = None
    print("Could not load win sound")
    win_sound = None

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
CARD_WIDTH, CARD_HEIGHT = 80, 120
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
CHIP_RADIUS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TABLE_GREEN = (0, 100, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Card setup
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = {rank: min(10, int(rank)) if rank not in ['J', 'Q', 'K', 'A'] else 10 for rank in ranks}
values['A'] = 11

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.SysFont("Comic Sans MS", 72)
button_font = pygame.font.Font(None, 36)
chip_font = pygame.font.Font(None, 24)

# Load card images
card_images = {}
for suit in suits:
    for rank in ranks:
        try:
            card_name = f"cards/{rank}_of_{suit.lower()}.png"
            image = pygame.image.load(card_name)
            card_images[(rank, suit)] = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        except:
            print(f"Missing image: {card_name}")
            # Create placeholder for missing cards
            surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            surf.fill(WHITE)
            pygame.draw.rect(surf, BLACK, (0, 0, CARD_WIDTH, CARD_HEIGHT), 2)
            text = font.render(f"{rank}{suit[0]}", True, BLACK)
            surf.blit(text, (CARD_WIDTH//2 - text.get_width()//2, CARD_HEIGHT//2 - text.get_height()//2))
            card_images[(rank, suit)] = surf

# Card back image
try:
    back_image = pygame.image.load("cards/back_of_card.png")
    card_images[('back', 'back')] = pygame.transform.scale(back_image, (CARD_WIDTH, CARD_HEIGHT))
except:
    print("Missing card back image")
    surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
    surf.fill(BLUE)
    pygame.draw.rect(surf, WHITE, (0, 0, CARD_WIDTH, CARD_HEIGHT), 2)
    card_images[('back', 'back')] = surf

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def hand_value(self):
        value = sum(values[card.rank] for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == 'A')
        
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

def draw_text(text, x, y, color=WHITE, font_size=36, font_type=None):
    current_font = pygame.font.Font(font_type, font_size) if font_type else pygame.font.Font(None, font_size)
    text_surface = current_font.render(text, True, color)
    screen.blit(text_surface, (x, y))
    return text_surface.get_rect(topleft=(x, y))

def draw_cards(hand, x, y, hide_first=False):
    for i, card in enumerate(hand.cards):
        if hide_first and i == 0:
            screen.blit(card_images[('back', 'back')], (x + i * (CARD_WIDTH + 10), y))
        else:
            screen.blit(card_images[(card.rank, card.suit)], (x + i * (CARD_WIDTH + 10), y))

def draw_button(text, x, y, width, height, color, text_color=BLACK):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect)
    draw_text(text, x + width//2 - len(text)*5, y + height//2 - 10, text_color)
    return rect

def draw_chip(x, y, value, color, outline_color):
    pygame.draw.circle(screen, outline_color, (x, y), CHIP_RADIUS + 5)
    pygame.draw.circle(screen, color, (x, y), CHIP_RADIUS)
    text = f"${value}"
    draw_text(text, x - (15 if value >= 10 else 8), y - 10, BLACK, 24)
    return pygame.Rect(x - CHIP_RADIUS, y - CHIP_RADIUS, CHIP_RADIUS * 2, CHIP_RADIUS * 2)

def home_screen():
    title = title_font.render("Welcome to Blackjack", True, RED)
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
    
    buttons = [
        {"rect": pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50), "color": GREEN, "text": "Start Game"},
        {"rect": pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, 200, 50), "color": RED, "text": "Quit"}
    ]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if buttons[0]["rect"].collidepoint(pos):
                    return
                elif buttons[1]["rect"].collidepoint(pos):
                    pygame.quit()
                    sys.exit()

        screen.fill(TABLE_GREEN)
        screen.blit(title, title_rect)
        for button in buttons:
            pygame.draw.rect(screen, button["color"], button["rect"])
            draw_text(button["text"], button["rect"].x + button["rect"].width//2 - len(button["text"])*7, 
                      button["rect"].y + button["rect"].height//2 - 10)
        pygame.display.flip()



def play_blackjack():
    money = 1000
    current_bet = 0
    betting_phase = True
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    player_turn = False
    game_over = False
    message = ""
    check_broke_after_play_again = False  

    chips = [
        {"value": 50, "color": BRONZE, "x": 700, "y": 200},
        {"value": 100, "color": SILVER, "x": 800, "y": 200},
        {"value": 250, "color": BLUE, "x": 900, "y": 200},
        {"value": 500, "color": RED, "x": 750, "y": 300},
        {"value": 1000, "color": GOLD, "x": 850, "y": 300}
    ]
    
    running = True
    while running:
        screen.fill(TABLE_GREEN)

       
        if check_broke_after_play_again and money <= 0:
            text_rect = draw_text("National Problem Gambling Helpline 1-800-GAMBLER", 65, 300, RED, 48)

            quit_button = draw_button("Quit", SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 + 50, 100, 50, RED)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 'quit_button' in locals() and quit_button.collidepoint(pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            continue
        
        # Draw UI elements
        draw_text(f"Money: ${money}", 700, 20)
        draw_text(f"Current Bet: ${current_bet}", 700, 60)
        
        if message:
            draw_text(message, 50, 550)
        
        if betting_phase:
            chip_rects = [draw_chip(chip["x"], chip["y"], chip["value"], chip["color"], WHITE) for chip in chips]
            if current_bet > 0:
                deal_button = draw_button("Deal", 750, 400, BUTTON_WIDTH, BUTTON_HEIGHT, GREEN)
            clear_button = draw_button("Clear", 750, 470, BUTTON_WIDTH, BUTTON_HEIGHT, RED)
        else:
            # Draw hands
            draw_text("Your hand:", 50, 50)
            draw_cards(player_hand, 50, 100)
            draw_text(f"Value: {player_hand.hand_value()}", 50, 250)

            draw_text("Dealer's hand:", 50, 300)
            draw_cards(dealer_hand, 50, 350, hide_first=player_turn and not game_over)
            dealer_value = "?" if player_turn and not game_over else dealer_hand.hand_value()
            draw_text(f"Value: {dealer_value}", 50, 500)

            if player_turn and not game_over:
                hit_button = draw_button("Hit", 750, 400, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE)
                stand_button = draw_button("Stand", 750, 470, BUTTON_WIDTH, BUTTON_HEIGHT, RED)

            if game_over:
                play_again_button = draw_button("Play Again", 750, 540, 190, BUTTON_HEIGHT, BLUE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if betting_phase:
                    for i, chip in enumerate(chips):
                        if chip_rects[i].collidepoint(pos) and money >= chip["value"]:
                            current_bet += chip["value"]
                            money -= chip["value"]
                            if chip_sound:
                                chip_sound.play()

                    
                    if current_bet > 0 and 'deal_button' in locals() and deal_button.collidepoint(pos):
                        betting_phase = False
                        player_turn = True
                        deck = Deck()
                        player_hand = Hand()
                        dealer_hand = Hand()
                        for _ in range(2):
                            player_hand.add_card(deck.deal_card())
                            dealer_hand.add_card(deck.deal_card())
                        message = ""
                    
                    if 'clear_button' in locals() and clear_button.collidepoint(pos):
                        money += current_bet
                        current_bet = 0
                
                elif player_turn and not game_over:
                    if 'hit_button' in locals() and hit_button.collidepoint(pos):
                        player_hand.add_card(deck.deal_card())
                        if player_hand.hand_value() > 21:
                            player_turn = False
                            game_over = True
                            message = "You busted! Dealer wins."
                            if lose_sound:
                                lose_sound.play()

                    
                    elif 'stand_button' in locals() and stand_button.collidepoint(pos):
                        player_turn = False
                
                elif game_over and 'play_again_button' in locals() and play_again_button.collidepoint(pos):
                    if money <= 0:
                        check_broke_after_play_again = True
                    else:
                        betting_phase = True
                        game_over = False
                        message = ""
                        current_bet = 0
                        check_broke_after_play_again = False  # Reset it

        # Dealer's turn
        if not player_turn and not game_over and not betting_phase:
            while dealer_hand.hand_value() < 17:
                dealer_hand.add_card(deck.deal_card())
            
            game_over = True
            p_value, d_value = player_hand.hand_value(), dealer_hand.hand_value()
            
            if p_value > 21:
                message = "You busted! Dealer wins."
                if lose_sound:
                    lose_sound.play()
            elif d_value > 21:
                message = "Dealer busted! You win!"
                money += current_bet * 2
                if win_sound:
                    win_sound.play()
            elif p_value > d_value:
                message = "You win!"
                money += current_bet * 2
                if win_sound:
                    win_sound.play()
            elif d_value > p_value:
                message = "Dealer wins!"
                if lose_sound:
                    lose_sound.play()
            else:
                message = "It's a tie!"
                money += current_bet

            
            current_bet = 0

        pygame.display.flip()




if __name__ == '__main__':
    home_screen()
    play_blackjack()