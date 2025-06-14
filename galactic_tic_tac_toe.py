import pygame
import sys
import random
import os
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Tic-Tac-Toe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_BLUE = (100, 100, 255)
DARK_BLUE = (50, 50, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
TRANSPARENT = (0, 0, 0, 128)

# Fonts
title_font = pygame.font.SysFont('arial', 64, bold=True)
button_font = pygame.font.SysFont('arial', 32)
score_font = pygame.font.SysFont('arial', 24)
game_over_font = pygame.font.SysFont('arial', 72, bold=True)

# Game variables
board = [' ' for _ in range(9)]
player_score = 0
computer_score = 0
current_screen = "main_menu"  # main_menu, game, victory, defeat
game_active = False
winner = None
winning_line = None
hover_button = None
match_point = 3  # Number of wins needed for match victory

# Create directories if they don't exist
os.makedirs('assets/images', exist_ok=True)
os.makedirs('assets/sounds', exist_ok=True)

# Placeholder for assets (in a real game, you'd have actual image files)
def create_placeholder_assets():
    # Create placeholder background
    bg = pygame.Surface((WIDTH, HEIGHT))
    for i in range(1000):
        x = random.randint(0, WIDTH-1)
        y = random.randint(0, HEIGHT-1)
        radius = random.randint(1, 3)
        color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))
        pygame.draw.circle(bg, color, (x, y), radius)
    
    # Save background
    pygame.image.save(bg, "assets/images/background.png")
    
    # Create X icon (player)
    x_icon = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.line(x_icon, (0, 200, 255), (20, 20), (80, 80), 10)
    pygame.draw.line(x_icon, (0, 200, 255), (80, 20), (20, 80), 10)
    pygame.image.save(x_icon, "assets/images/x_icon.png")
    
    # Create O icon (computer)
    o_icon = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(o_icon, (255, 100, 100), (50, 50), 40, 10)
    pygame.image.save(o_icon, "assets/images/o_icon.png")
    
    # Create sound placeholders (empty files)
    for sound in ["click.wav", "hover.wav", "win.wav", "lose.wav"]:
        with open(f"assets/sounds/{sound}", "wb") as f:
            f.write(b"")

# Check if assets exist, if not create placeholders
if not os.path.exists("assets/images/background.png"):
    create_placeholder_assets()

# Load assets
try:
    background = pygame.image.load("assets/images/background.png").convert()
    x_icon = pygame.image.load("assets/images/x_icon.png").convert_alpha()
    o_icon = pygame.image.load("assets/images/o_icon.png").convert_alpha()
    
    # Load sounds
    click_sound = mixer.Sound("assets/sounds/click.wav")
    hover_sound = mixer.Sound("assets/sounds/hover.wav")
    win_sound = mixer.Sound("assets/sounds/win.wav")
    lose_sound = mixer.Sound("assets/sounds/lose.wav")
except pygame.error:
    print("Warning: Some assets couldn't be loaded. Using fallback graphics.")
    # Create fallback graphics
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((20, 20, 50))
    
    x_icon = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.line(x_icon, (0, 200, 255), (20, 20), (80, 80), 10)
    pygame.draw.line(x_icon, (0, 200, 255), (80, 20), (20, 80), 10)
    
    o_icon = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(o_icon, (255, 100, 100), (50, 50), 40, 10)
    
    # Create dummy sounds
    click_sound = mixer.Sound(buffer=bytes([0]))
    hover_sound = mixer.Sound(buffer=bytes([0]))
    win_sound = mixer.Sound(buffer=bytes([0]))
    lose_sound = mixer.Sound(buffer=bytes([0]))

# Resize icons
x_icon = pygame.transform.scale(x_icon, (100, 100))
o_icon = pygame.transform.scale(o_icon, (100, 100))

def play_sound(sound):
    """Play a sound effect"""
    try:
        sound.play()
    except:
        pass  # Silently fail if sound can't be played

def reset_board():
    """Reset the game board"""
    global board, game_active, winner, winning_line
    board = [' ' for _ in range(9)]
    game_active = True
    winner = None
    winning_line = None

def check_win(board, player):
    """Check if a player has won"""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return condition
    return None

def check_draw(board):
    """Check if the game is a draw"""
    return ' ' not in board

def computer_move():
    """Make a move for the computer"""
    # Check if computer can win
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if check_win(board, 'O'):
                return
            board[i] = ' '
    
    # Check if player can win and block
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if check_win(board, 'X'):
                board[i] = 'O'
                return
            board[i] = ' '
    
    # Take center if available
    if board[4] == ' ':
        board[4] = 'O'
        return
    
    # Take corners if available
    corners = [0, 2, 6, 8]
    random.shuffle(corners)
    for corner in corners:
        if board[corner] == ' ':
            board[corner] = 'O'
            return
    
    # Take any available space
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            return

def draw_board():
    """Draw the game board"""
    # Draw grid lines
    pygame.draw.line(screen, WHITE, (300, 150), (300, 450), 5)
    pygame.draw.line(screen, WHITE, (400, 150), (400, 450), 5)
    pygame.draw.line(screen, WHITE, (200, 250), (500, 250), 5)
    pygame.draw.line(screen, WHITE, (200, 350), (500, 350), 5)
    
    # Draw X's and O's
    for i in range(9):
        row, col = i // 3, i % 3
        x = 200 + col * 100 + 50
        y = 150 + row * 100 + 50
        
        if board[i] == 'X':
            screen.blit(x_icon, (x - 50, y - 50))
        elif board[i] == 'O':
            screen.blit(o_icon, (x - 50, y - 50))
    
    # Highlight winning line if there is one
    if winning_line:
        start_idx = winning_line[0]
        end_idx = winning_line[2]
        start_row, start_col = start_idx // 3, start_idx % 3
        end_row, end_col = end_idx // 3, end_idx % 3
        
        start_x = 200 + start_col * 100 + 50
        start_y = 150 + start_row * 100 + 50
        end_x = 200 + end_col * 100 + 50
        end_y = 150 + end_row * 100 + 50
        
        pygame.draw.line(screen, GREEN, (start_x, start_y), (end_x, end_y), 10)

def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    """Draw a button and handle hover effects"""
    global hover_button
    
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]
    
    # Check if mouse is over button
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        
        # Play hover sound if this is a new hover
        if hover_button != text:
            play_sound(hover_sound)
            hover_button = text
        
        # Handle click
        if clicked and action:
            play_sound(click_sound)
            pygame.time.delay(200)  # Small delay to prevent double clicks
            action()
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
        if hover_button == text:
            hover_button = None
    
    # Draw button text
    text_surf = button_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surf, text_rect)
    
    return False

def draw_main_menu():
    """Draw the main menu screen"""
    # Draw title
    title = title_font.render("Galactic Tic-Tac-Toe", True, WHITE)
    screen.blit(title, (WIDTH/2 - title.get_width()/2, 100))
    
    # Draw buttons
    if draw_button("Start Game", WIDTH/2 - 100, 250, 200, 60, DARK_BLUE, LIGHT_BLUE, start_game):
        return
    
    if draw_button("Quit", WIDTH/2 - 100, 350, 200, 60, DARK_BLUE, LIGHT_BLUE, quit_game):
        return

def draw_game_screen():
    """Draw the game screen"""
    # Draw score
    score_text = score_font.render(f"Player: {player_score}   Computer: {computer_score}", True, WHITE)
    screen.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 50))
    
    # Draw board
    draw_board()
    
    # Draw buttons
    if draw_button("Main Menu", 50, 500, 150, 50, DARK_BLUE, LIGHT_BLUE, go_to_main_menu):
        return
    
    if not game_active:
        if draw_button("Play Again", WIDTH - 200, 500, 150, 50, DARK_BLUE, LIGHT_BLUE, reset_board):
            return

def draw_victory_screen():
    """Draw the victory screen"""
    # Create semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    # Draw victory message
    victory_text = game_over_font.render("VICTORY!", True, GREEN)
    screen.blit(victory_text, (WIDTH/2 - victory_text.get_width()/2, 150))
    
    # Draw score
    score_text = score_font.render(f"Final Score - Player: {player_score}   Computer: {computer_score}", True, WHITE)
    screen.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 250))
    
    # Draw buttons
    if draw_button("Next Match", WIDTH/2 - 200, 350, 180, 60, DARK_BLUE, LIGHT_BLUE, new_match):
        return
    
    if draw_button("Main Menu", WIDTH/2 + 20, 350, 180, 60, DARK_BLUE, LIGHT_BLUE, go_to_main_menu):
        return

def draw_defeat_screen():
    """Draw the defeat screen"""
    # Create semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    # Draw defeat message
    defeat_text = game_over_font.render("DEFEAT!", True, RED)
    screen.blit(defeat_text, (WIDTH/2 - defeat_text.get_width()/2, 150))
    
    # Draw score
    score_text = score_font.render(f"Final Score - Player: {player_score}   Computer: {computer_score}", True, WHITE)
    screen.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 250))
    
    # Draw buttons
    if draw_button("Try Again", WIDTH/2 - 200, 350, 180, 60, DARK_BLUE, LIGHT_BLUE, new_match):
        return
    
    if draw_button("Main Menu", WIDTH/2 + 20, 350, 180, 60, DARK_BLUE, LIGHT_BLUE, go_to_main_menu):
        return

def start_game():
    """Start a new game"""
    global current_screen, game_active
    reset_board()
    current_screen = "game"
    game_active = True

def go_to_main_menu():
    """Go to the main menu"""
    global current_screen
    current_screen = "main_menu"

def new_match():
    """Start a new match"""
    global player_score, computer_score, current_screen
    player_score = 0
    computer_score = 0
    current_screen = "game"
    reset_board()

def quit_game():
    """Quit the game"""
    pygame.quit()
    sys.exit()

def handle_click(pos):
    """Handle mouse click during the game"""
    global game_active, winner, winning_line, player_score, computer_score, current_screen
    
    if not game_active:
        return
    
    # Convert mouse position to board position
    x, y = pos
    if 200 <= x <= 500 and 150 <= y <= 450:
        col = (x - 200) // 100
        row = (y - 150) // 100
        index = row * 3 + col
        
        # Make player move if cell is empty
        if board[index] == ' ':
            play_sound(click_sound)
            board[index] = 'X'
            
            # Check if player won
            winning_line = check_win(board, 'X')
            if winning_line:
                winner = 'X'
                game_active = False
                player_score += 1
                play_sound(win_sound)
                
                # Check if player reached match point
                if player_score >= match_point:
                    current_screen = "victory"
                return
            
            # Check for draw
            if check_draw(board):
                game_active = False
                return
            
            # Computer's turn
            pygame.time.delay(300)  # Small delay before computer moves
            computer_move()
            
            # Check if computer won
            winning_line = check_win(board, 'O')
            if winning_line:
                winner = 'O'
                game_active = False
                computer_score += 1
                play_sound(lose_sound)
                
                # Check if computer reached match point
                if computer_score >= match_point:
                    current_screen = "defeat"
                return
            
            # Check for draw again
            if check_draw(board):
                game_active = False
                return

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "game":
                handle_click(event.pos)
    
    # Draw background
    screen.blit(background, (0, 0))
    
    # Draw current screen
    if current_screen == "main_menu":
        draw_main_menu()
    elif current_screen == "game":
        draw_game_screen()
    elif current_screen == "victory":
        draw_game_screen()  # Draw game screen in background
        draw_victory_screen()
    elif current_screen == "defeat":
        draw_game_screen()  # Draw game screen in background
        draw_defeat_screen()
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
