import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
import threading
import pygame
import os
import json

# Initialize Pygame mixer for sound effects and animations
try:
    pygame.mixer.init()
    # Load sound effects with error handling
    hit_sound = pygame.mixer.Sound("hit.wav") if os.path.exists("hit.wav") else None
    miss_sound = pygame.mixer.Sound("miss.wav") if os.path.exists("miss.wav") else None
    sink_sound = pygame.mixer.Sound("sink.wav") if os.path.exists("sink.wav") else None
except pygame.error:
    hit_sound = None
    miss_sound = None
    sink_sound = None

def play_sound(sound):
    if sound:
        threading.Thread(target=sound.play).start()

def create_board(size):
    return [["O" for _ in range(size)] for _ in range(size)]

def place_ships(board, ships):
    ship_positions = []
    directions = [(0, 1), (1, 0)]  # horizontal or vertical
    for _ in range(ships):
        while True:
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board) - 1)
            direction = random.choice(directions)
            if can_place_ship(board, row, col, direction):
                for i in range(3):  # example length of ship
                    r, c = row + i * direction[0], col + i * direction[1]
                    board[r][c] = "S"
                    ship_positions.append((r, c))
                break
    return ship_positions

def can_place_ship(board, row, col, direction, length=3):
    for i in range(length):
        r, c = row + i * direction[0], col + i * direction[1]
        if r >= len(board) or c >= len(board) or board[r][c] != "O":
            return False
    return True

def save_high_score(score):
    try:
        with open("high_scores.json", "r") as file:
            scores = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []

    scores.append(score)
    scores = sorted(scores)[:5]  # Keep only top 5 scores

    with open("high_scores.json", "w") as file:
        json.dump(scores, file)

def display_high_scores():
    try:
        with open("high_scores.json", "r") as file:
            scores = json.load(file)
        score_text = "\n".join([f"{i+1}. {s} seconds" for i, s in enumerate(scores)])
        messagebox.showinfo("High Scores", f"Top Scores:\n{score_text}")
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showinfo("High Scores", "No high scores yet. Be the first!")

def play_battleship_gui():
    board_size = 5
    num_ships = 3
    board = create_board(board_size)
    ship_positions = place_ships(board, num_ships)
    turns = 7
    start_time = time.time()

    def update_timer():
        elapsed_time = int(time.time() - start_time)
        timer_label.config(text=f"⏱ Time: {elapsed_time} seconds")
        root.after(1000, update_timer)

    def animate_hit_miss(button, animation_type):
        colors = {"hit": ["#FF6B6B", "#FFFF00"], "miss": ["#00796B", "#00BFFF"]}
        if animation_type in colors:
            for color in colors[animation_type]:
                button.config(bg=color)
                button.update()
                time.sleep(0.1)
            button.config(bg=colors[animation_type][0])

    def make_guess(row, col):
        nonlocal turns
        if turns <= 0:
            messagebox.showinfo("Game Over", "No more turns left. Please restart the game.")
            return
        if board[row][col] == "X":
            messagebox.showinfo("Battleship", "You already guessed that one.")
        elif board[row][col] == "S":
            board[row][col] = "X"
            button_grid[row][col].config(text="💥", state=tk.DISABLED, foreground="#FFFFFF")
            threading.Thread(target=animate_hit_miss, args=(button_grid[row][col], "hit")).start()
            play_sound(hit_sound)
            ship_positions.remove((row, col))
            if not ship_positions:
                play_sound(sink_sound)
                threading.Thread(target=animate_hit_miss, args=(button_grid[row][col], "hit")).start()
                elapsed_time = int(time.time() - start_time)
                messagebox.showinfo("Battleship", f"Congratulations! You sunk all the battleships in {elapsed_time} seconds!")
                save_high_score(elapsed_time)
                root.destroy()
            else:
                messagebox.showinfo("Battleship", "You hit a ship!")
        else:
            board[row][col] = "X"
            button_grid[row][col].config(text="X", state=tk.DISABLED, foreground="#FFFFFF")
            threading.Thread(target=animate_hit_miss, args=(button_grid[row][col], "miss")).start()
            play_sound(miss_sound)
            turns -= 1
            if turns == 0:
                remaining_ships = [f"Row: {r}, Col: {c}" for r, c in ship_positions]
                elapsed_time = int(time.time() - start_time)
                messagebox.showinfo("Game Over", f"Game Over. The remaining ships were at: {', '.join(remaining_ships)}. Time taken: {elapsed_time} seconds.")
                game_over_label = tk.Label(root, text="Game Over", font=("Helvetica", 24, "bold"), bg="#1E1E1E", fg="#FF6B6B")
                game_over_label.pack(pady=20)
            else:
                messagebox.showinfo("Battleship", f"You missed! Turns left: {turns}")

    def give_hint():
        if ship_positions:
            hint_row, hint_col = random.choice(ship_positions)
            messagebox.showinfo("Hint", f"A battleship is somewhere around Row: {hint_row}, Column: {hint_col}")
        else:
            messagebox.showinfo("Hint", "No ships left to hint!")

    def restart_game():
        root.destroy()
        play_battleship_gui()

    root = tk.Tk()
    root.title("Battleship Game")
    root.configure(bg="#1E1E1E")
    root.geometry("700x800")
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Helvetica", 12), padding=10, background="#4ECDC4", foreground="#FFFFFF")

    title_label = tk.Label(root, text="\U0001F6A5 Battleship Game \U0001F6A5", font=("Helvetica", 34, "bold"), bg="#1E1E1E", fg="#4ECDC4")
    title_label.pack(pady=10)

    timer_label = tk.Label(root, text="⏱ Time: 0 seconds", font=("Helvetica", 16), bg="#1E1E1E", fg="#FFFFFF")
    timer_label.pack(pady=10)

    frame = tk.Frame(root, bg="#1E1E1E")
    frame.pack(pady=20)

    button_grid = []
    for r in range(board_size):
        row = []
        for c in range(board_size):
            btn = tk.Button(frame, text="\U0001F3F3", command=lambda r=r, c=c: make_guess(r, c), font=("Helvetica", 16, "bold"), width=4, height=2, bg="#00796B", fg="#E1F5FE", relief=tk.RAISED, bd=6)
            btn.grid(row=r, column=c, padx=10, pady=10)
            row.append(btn)
        button_grid.append(row)

    button_frame = tk.Frame(root, bg="#1E1E1E")
    button_frame.pack(pady=20)

    hint_button = tk.Button(button_frame, text="\U0001F575 Hint", command=give_hint, font=("Helvetica", 16, "bold"), width=14, bg="#FFD700", fg="#1E1E1E", relief=tk.RAISED, bd=6)
    hint_button.grid(row=0, column=0, padx=10, pady=10)

    restart_button = tk.Button(button_frame, text="\U0001F504 Restart", command=restart_game, font=("Helvetica", 16, "bold"), width=14, bg="#FF6347", fg="#FFFFFF", relief=tk.RAISED, bd=6)
    restart_button.grid(row=0, column=1, padx=10, pady=10)

    high_score_button = tk.Button(button_frame, text="\U0001F4C8 High Scores", command=display_high_scores, font=("Helvetica", 16, "bold"), width=14, bg="#4ECDC4", fg="#1E1E1E", relief=tk.RAISED, bd=6)
    high_score_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    footer_label = tk.Label(root, text="\U0001F340 Good Luck, Captain! \U0001F340", font=("Helvetica", 20, "italic"), bg="#1E1E1E", fg="#FFFFFF")
    footer_label.pack(pady=20)

    update_timer()
    root.mainloop()

if __name__ == "__main__":
    play_battleship_gui()




    import random
import time
import threading
import pygame
import os
import json

# Initialize Pygame mixer for sound effects and Pygame for graphics
pygame.init()
try:
    pygame.mixer.init()
    # Load sound effects with error handling
    hit_sound = pygame.mixer.Sound("hit.wav") if os.path.exists("hit.wav") else None
    miss_sound = pygame.mixer.Sound("miss.wav") if os.path.exists("miss.wav") else None
    sink_sound = pygame.mixer.Sound("sink.wav") if os.path.exists("sink.wav") else None
except pygame.error:
    hit_sound = None
    miss_sound = None
    sink_sound = None

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (20, 20, 60)
LIGHT_BLUE = (173, 216, 230)
BUTTON_COLOR = (78, 205, 196)
BUTTON_HOVER_COLOR = (90, 220, 210)

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
CELL_SIZE = 60
MARGIN = 10

def play_sound(sound):
    if sound:
        threading.Thread(target=sound.play).start()

def create_board(size):
    return [["O" for _ in range(size)] for _ in range(size)]

def place_ships(board, ships):
    ship_positions = []
    directions = [(0, 1), (1, 0)]  # horizontal or vertical
    for _ in range(ships):
        while True:
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board) - 1)
            direction = random.choice(directions)
            if can_place_ship(board, row, col, direction):
                for i in range(3):  # example length of ship
                    r, c = row + i * direction[0], col + i * direction[1]
                    board[r][c] = "S"
                    ship_positions.append((r, c))
                break
    return ship_positions

def can_place_ship(board, row, col, direction, length=3):
    for i in range(length):
        r, c = row + i * direction[0], col + i * direction[1]
        if r >= len(board) or c >= len(board) or board[r][c] != "O":
            return False
    return True

def save_high_score(score):
    try:
        with open("high_scores.json", "r") as file:
            scores = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []

    scores.append(score)
    scores = sorted(scores)[:5]  # Keep only top 5 scores

    with open("high_scores.json", "w") as file:
        json.dump(scores, file)

def display_high_scores(screen):
    try:
        with open("high_scores.json", "r") as file:
            scores = json.load(file)
        score_text = [f"{i+1}. {s} seconds" for i, s in enumerate(scores)]
    except (FileNotFoundError, json.JSONDecodeError):
        score_text = ["No high scores yet. Be the first!"]

    font = pygame.font.Font(None, 36)
    screen.fill(BLACK)
    y_offset = 100
    for line in score_text:
        text = font.render(line, True, WHITE)
        screen.blit(text, (50, y_offset))
        y_offset += 40
    pygame.display.flip()
    time.sleep(3)

def draw_button(screen, text, rect, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    current_color = color

    if rect.collidepoint(mouse):
        current_color = hover_color
        if click[0] == 1 and action is not None:
            action()

    pygame.draw.rect(screen, current_color, rect)
    font = pygame.font.Font(None, 40)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def play_battleship_pygame():
    board_size = 5
    num_ships = 3
    board = create_board(board_size)
    ship_positions = place_ships(board, num_ships)
    turns = 7
    start_time = time.time()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Battleship Game")
    clock = pygame.time.Clock()

    hint_button_rect = pygame.Rect(100, 600, 150, 50)
    restart_button_rect = pygame.Rect(300, 600, 150, 50)
    high_scores_button_rect = pygame.Rect(500, 600, 200, 50)

    def restart_game():
        nonlocal board, ship_positions, turns, start_time
        board = create_board(board_size)
        ship_positions = place_ships(board, num_ships)
        turns = 7
        start_time = time.time()

    running = True
    while running:
        screen.fill(DARK_BLUE)
        elapsed_time = int(time.time() - start_time)
        font = pygame.font.Font(None, 50)
        timer_text = font.render(f"⏱ Time: {elapsed_time} seconds", True, WHITE)
        screen.blit(timer_text, (10, 10))
        turns_text = font.render(f"Turns Left: {turns}", True, WHITE)
        screen.blit(turns_text, (SCREEN_WIDTH - 250, 10))

        # Draw the board
        for row in range(board_size):
            for col in range(board_size):
                color = LIGHT_BLUE if board[row][col] == "O" else RED if board[row][col] == "X" else GREEN
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + CELL_SIZE) * col + MARGIN + 150,
                                  (MARGIN + CELL_SIZE) * row + MARGIN + 150,
                                  CELL_SIZE,
                                  CELL_SIZE],
                                 border_radius=5)
                if board[row][col] == "X":
                    explosion_center = [(MARGIN + CELL_SIZE) * col + MARGIN + 150 + CELL_SIZE // 2,
                                        (MARGIN + CELL_SIZE) * row + MARGIN + 150 + CELL_SIZE // 2]
                    pygame.draw.circle(screen, YELLOW, explosion_center, 10)

        # Draw buttons
        draw_button(screen, "Hint", hint_button_rect, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: print("Hint button clicked"))
        draw_button(screen, "Restart", restart_button_rect, BUTTON_COLOR, BUTTON_HOVER_COLOR, restart_game)
        draw_button(screen, "High Scores", high_scores_button_rect, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: display_high_scores(screen))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = (pos[0] - 150) // (CELL_SIZE + MARGIN)
                row = (pos[1] - 150) // (CELL_SIZE + MARGIN)

                if 0 <= row < board_size and 0 <= col < board_size:
                    if board[row][col] == "X":
                        print("Already guessed that one.")
                    elif board[row][col] == "S":
                        board[row][col] = "X"
                        play_sound(hit_sound)
                        ship_positions.remove((row, col))
                        if not ship_positions:
                            play_sound(sink_sound)
                            elapsed_time = int(time.time() - start_time)
                            save_high_score(elapsed_time)
                            print(f"Congratulations! You sunk all the battleships in {elapsed_time} seconds!")
                            running = False
                    else:
                        board[row][col] = "X"
                        play_sound(miss_sound)
                        turns -= 1
                        if turns == 0:
                            remaining_ships = [f"Row: {r}, Col: {c}" for r, c in ship_positions]
                            elapsed_time = int(time.time() - start_time)
                            print(f"Game Over. The remaining ships were at: {', '.join(remaining_ships)}. Time taken: {elapsed_time} seconds.")
                            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    play_battleship_pygame()