import pygame
import random
import os
import math
from queue import Queue

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arabic Learning Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
LIGHT_BLUE = (173, 216, 230)
GOLD = (255, 215, 0)
DARK_GOLD = (218, 165, 32)
SHADOW_COLOR = (169, 169, 169)

# Background
try:
    background_img = pygame.image.load(os.path.join('images', 'abstract_pattern.png'))  # Add an abstract and colorful pattern image
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
except FileNotFoundError:
    print("Background image 'abstract_pattern.png' not found.")
    background_img = None

# Load Arabic letters, numbers, and words
letters = ['ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي']
numbers = ['١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩', '١٠']  # Arabic numbers 1 to 10
words = ['بيت', 'تفاح', 'مدرسة']  # Example Arabic words
current_category = 'letters'

letter_positions = []

# Load sound files
sounds = {}

# Load multiple correct and wrong sound files
correct_sounds = []
wrong_sounds = []

for i in range(1, 4):  # Assuming there are 3 correct and 3 wrong sound files
    try:
        correct_sounds.append(pygame.mixer.Sound(os.path.join('sounds', f'correct_{i}.wav')))
    except FileNotFoundError:
        print(f"Correct sound 'correct_{i}.wav' not found.")
    try:
        wrong_sounds.append(pygame.mixer.Sound(os.path.join('sounds', f'wrong_{i}.wav')))
    except FileNotFoundError:
        print(f"Wrong sound 'wrong_{i}.wav' not found.")

# Load general prompt sounds
try:
    sounds['find_the_letter'] = pygame.mixer.Sound(os.path.join('sounds', 'find_the_letter.wav'))
except FileNotFoundError:
    print("General prompt sound 'find_the_letter.wav' not found.")

try:
    sounds['find_the_number'] = pygame.mixer.Sound(os.path.join('sounds', 'find_the_number.wav'))
except FileNotFoundError:
    print("General prompt sound 'find_the_number.wav' not found.")

try:
    sounds['find_whos_sound'] = pygame.mixer.Sound(os.path.join('sounds', 'find_whos_sound.wav'))
except FileNotFoundError:
    print("General prompt sound 'find_whos_sound.wav' not found.")

for letter in letters:
    try:
        sounds[f'prompt_{letter}'] = pygame.mixer.Sound(os.path.join('sounds', f'prompt_{letter}.wav'))
    except FileNotFoundError:
        print(f"Sound for {letter} not found.")

for i in range(1, 11):
    try:
        sounds[f'prompt_{i}'] = pygame.mixer.Sound(os.path.join('sounds', f'prompt_{i}.wav'))
    except FileNotFoundError:
        print(f"Sound for number {i} not found.")

# Load arrow image
arrow_img = pygame.image.load(os.path.join('images', 'arrow.png'))
arrow_img = pygame.transform.scale(arrow_img, (50, 50))

# Load images and sounds for "Who's Sound is This" category
who_images = {}
who_sounds = {}

who_items = ['grand_grandma', 'grandma', 'grandpa', 'yaser', 'ammar', 'sumayah', 'anas', 'cow', 'dog', 'cat', 'fart']

for item in who_items:
    try:
        who_images[item] = pygame.image.load(os.path.join('who_images', f'{item}.png'))
    except FileNotFoundError:
        print(f"Image for {item} not found.")
    try:
        who_sounds[item] = pygame.mixer.Sound(os.path.join('who_sounds', f'{item}.wav'))
    except FileNotFoundError:
        print(f"Sound for {item} not found.")

# Load images for letters, numbers, and words
letter_images = {}
for letter in letters:
    try:
        letter_images[letter] = pygame.image.load(os.path.join('letter_images', f'{letter}.png'))
    except FileNotFoundError:
        print(f"Image for {letter} not found.")

number_images = {}
number_image_names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
for i, name in enumerate(number_image_names, start=1):
    try:
        number_images[numbers[i - 1]] = pygame.image.load(os.path.join('number_images', f'{name}.png'))
    except FileNotFoundError:
        print(f"Image for number {name} not found.")

word_images = {}
try:
    word_images['بيت'] = pygame.image.load(os.path.join('word_images', 'house.png'))
except FileNotFoundError:
    print("Image for house not found.")
try:
    word_images['تفاح'] = pygame.image.load(os.path.join('word_images', 'apple.png'))
except FileNotFoundError:
    print("Image for apple not found.")
try:
    word_images['مدرسة'] = pygame.image.load(os.path.join('word_images', 'school.png'))
except FileNotFoundError:
    print("Image for school not found.")

# Sound Queue to manage overlapping issues
sound_queue = Queue()

# Function to play a sequence of sounds
def play_sounds_sequence(*sounds_to_play):
    for sound in sounds_to_play:
        if sound is not None:
            sound_queue.put(sound)

def play_sound_from_queue():
    if not sound_queue.empty() and not pygame.mixer.get_busy():
        sound = sound_queue.get()
        sound.play()

# Function to draw buttons for game selection
def draw_buttons():
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(WHITE)
    font = pygame.font.Font(pygame.font.match_font('arial'), 60)

    # Button 1: Find the Letter
    button_1 = pygame.Rect(400, 200, 400, 100)
    shadow_1 = button_1.move(5, 5)  # Create shadow effect
    pygame.draw.rect(screen, SHADOW_COLOR, shadow_1, border_radius=20)
    pygame.draw.rect(screen, GOLD, button_1, border_radius=20)
    pygame.draw.rect(screen, DARK_GOLD, button_1, width=5, border_radius=20)
    text_1 = font.render('Find the Letter', True, BLACK)
    screen.blit(text_1, (button_1.x + (button_1.width - text_1.get_width()) // 2, button_1.y + (button_1.height - text_1.get_height()) // 2))

    # Button 2: Find the Number
    button_2 = pygame.Rect(400, 350, 400, 100)
    shadow_2 = button_2.move(5, 5)  # Create shadow effect
    pygame.draw.rect(screen, SHADOW_COLOR, shadow_2, border_radius=20)
    pygame.draw.rect(screen, GOLD, button_2, border_radius=20)
    pygame.draw.rect(screen, DARK_GOLD, button_2, width=5, border_radius=20)
    text_2 = font.render('Find the Number', True, BLACK)
    screen.blit(text_2, (button_2.x + (button_2.width - text_2.get_width()) // 2, button_2.y + (button_2.height - text_2.get_height()) // 2))

    # Button 3: Who's Sound is This
    button_3 = pygame.Rect(400, 500, 400, 100)
    shadow_3 = button_3.move(5, 5)  # Create shadow effect
    pygame.draw.rect(screen, SHADOW_COLOR, shadow_3, border_radius=20)
    pygame.draw.rect(screen, GOLD, button_3, border_radius=20)
    pygame.draw.rect(screen, DARK_GOLD, button_3, width=5, border_radius=20)
    text_3 = font.render("Who's Sound is This", True, BLACK)
    screen.blit(text_3, (button_3.x + (button_3.width - text_3.get_width()) // 2, button_3.y + (button_3.height - text_3.get_height()) // 2))

    pygame.display.update()
    return button_1, button_2, button_3

# Function to draw items on the screen (using images)
def draw_items(dancing=False):
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(WHITE)
    letter_positions.clear()
    x, y = 100, 100
    items = []
    if current_category == 'letters':
        items = letters
        images = letter_images
    elif current_category == 'numbers':
        items = numbers
        images = number_images
    elif current_category == 'words':
        items = words
        images = word_images
    elif current_category == 'who':
        items = who_items
        images = who_images

    for item in items:
        if item in images:
            offset = random.randint(-10, 10) if dancing else 0
            item_img = images[item]
            item_img = pygame.transform.scale(item_img, (120, 120))  # Scale to appropriate size
            item_rect = item_img.get_rect(center=(x, y + offset))
            screen.blit(item_img, item_rect)
            letter_positions.append((item, item_rect))
            x += 170
            if x > WIDTH - 100:
                x = 100
                y += 150

    # Draw Back Button
    font = pygame.font.Font(pygame.font.match_font('arial'), 50)
    back_button = pygame.Rect(50, 800, 150, 50)
    shadow_back = back_button.move(5, 5)
    pygame.draw.rect(screen, SHADOW_COLOR, shadow_back, border_radius=10)
    pygame.draw.rect(screen, LIGHT_BLUE, back_button, border_radius=10)
    pygame.draw.rect(screen, DARK_BLUE, back_button, width=3, border_radius=10)
    text_back = font.render('Back', True, BLACK)
    screen.blit(text_back, (back_button.x + (back_button.width - text_back.get_width()) // 2, back_button.y + (back_button.height - text_back.get_height()) // 2))

    # Draw Replay Button
    replay_button = pygame.Rect(1000, 800, 150, 50)
    shadow_replay = replay_button.move(5, 5)
    pygame.draw.rect(screen, SHADOW_COLOR, shadow_replay, border_radius=10)
    pygame.draw.rect(screen, LIGHT_BLUE, replay_button, border_radius=10)
    pygame.draw.rect(screen, DARK_BLUE, replay_button, width=3, border_radius=10)
    text_replay = font.render('Replay', True, BLACK)
    screen.blit(text_replay, (replay_button.x + (replay_button.width - text_replay.get_width()) // 2, replay_button.y + (replay_button.height - text_replay.get_height()) // 2))

    pygame.display.update()
    return back_button, replay_button

# Function to animate correct item
def animate_correct_item(item_rect):
    for i in range(5):
        pygame.draw.rect(screen, GREEN, item_rect.inflate(20, 20), 5)
        pygame.display.update()
        pygame.time.delay(100)
        draw_items()
        pygame.display.update()
        pygame.time.delay(100)

# Function to give feedback when wrong item is selected
def animate_wrong_item(item_rect, current_item_rect):
    for i in range(3):
        pygame.draw.rect(screen, RED, item_rect.inflate(20, 20), 5)
        pygame.display.update()
        pygame.time.delay(100)
        draw_items()
        pygame.display.update()
        pygame.time.delay(100)

    # Animate an arrow moving towards the correct item
    if current_item_rect:  # Ensure current_item_rect exists
        arrow_pos = list(item_rect.center)
        target_pos = current_item_rect.center
        step_count = 30
        for step in range(step_count):
            draw_items()
            t = step / step_count
            arrow_pos[0] = (1 - t) * item_rect.center[0] + t * target_pos[0]
            arrow_pos[1] = (1 - t) * item_rect.center[1] + t * target_pos[1]
            angle = math.degrees(math.atan2(target_pos[1] - arrow_pos[1], target_pos[0] - arrow_pos[0]))
            rotated_arrow = pygame.transform.rotate(arrow_img, -angle)
            arrow_rect = rotated_arrow.get_rect(center=arrow_pos)
            screen.blit(rotated_arrow, arrow_rect)
            pygame.display.update()
            pygame.time.delay(50)

# Function to make items dance
def animate_dancing_items():
    for _ in range(20):  # Make the items dance for a short duration
        draw_items(dancing=True)
        pygame.time.delay(100)

# Function to play prompt sound without overlapping
def play_prompt_sound(current_item):
    # Play general prompt sound first if applicable
    if current_category == 'letters' and 'find_the_letter' in sounds:
        sound_queue.put(sounds['find_the_letter'])
    elif current_category == 'numbers' and 'find_the_number' in sounds:
        sound_queue.put(sounds['find_the_number'])
    elif current_category == 'who' and 'find_whos_sound' in sounds:
        sound_queue.put(sounds['find_whos_sound'])
    
    # Wait for the general prompt to finish before playing the specific item sound
    while pygame.mixer.get_busy():
        pygame.time.delay(100)  # Wait 100ms while a sound is playing
    
    # Play specific item sound
    if current_category == 'numbers' and current_item in numbers:
        try:
            sound_queue.put(sounds[f'prompt_{numbers.index(current_item) + 1}'])
        except KeyError:
            print(f"Sound for number {current_item} not found, skipping.")
    elif current_category == 'who' and current_item in who_sounds:
        sound_queue.put(who_sounds[current_item])
    elif f'prompt_{current_item}' in sounds:
        try:
            sound_queue.put(sounds[f'prompt_{current_item}'])
        except KeyError:
            print(f"Sound for {current_item} not found, skipping.")


# Main game loop
def main():
    global current_category
    running = True
    clock = pygame.time.Clock()

    # Show initial menu with buttons
    button_1, button_2, button_3 = draw_buttons()

    category_selected = False
    current_item = None
    used_items = set()

    while running:
        play_sound_from_queue()
        if not category_selected:
            # Event handling for selecting category
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button_1.collidepoint(mouse_pos):
                        current_category = 'letters'
                        used_items.clear()
                        current_item = random.choice([item for item in letters if item not in used_items])
                        used_items.add(current_item)
                        play_prompt_sound(current_item)
                        category_selected = True
                    elif button_2.collidepoint(mouse_pos):
                        current_category = 'numbers'
                        used_items.clear()
                        current_item = random.choice([item for item in numbers if item not in used_items])
                        used_items.add(current_item)
                        play_prompt_sound(current_item)
                        category_selected = True
                    elif button_3.collidepoint(mouse_pos):
                        current_category = 'who'
                        used_items.clear()
                        current_item = random.choice([item for item in who_items if item not in used_items])
                        used_items.add(current_item)
                        play_prompt_sound(current_item)
                        category_selected = True
        else:
            back_button, replay_button = draw_items()

            # Event handling for game interaction
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if back_button.collidepoint(mouse_pos):
                        category_selected = False
                        button_1, button_2, button_3 = draw_buttons()
                    elif replay_button.collidepoint(mouse_pos):
                        play_prompt_sound(current_item)  # Replay the current prompt sound
                    else:
                        # Check if the clicked item is correct
                        for item, rect in letter_positions:
                            if rect.collidepoint(mouse_pos):
                                if item == current_item:
                                    random.choice(correct_sounds).play()
                                    animate_correct_item(rect)
                                    animate_dancing_items()
                                    remaining_items = [item for item in (letters if current_category == 'letters' else numbers if current_category == 'numbers' else who_items if current_category == 'who' else words) if item not in used_items]
                                    if remaining_items:
                                        current_item = random.choice(remaining_items)
                                        used_items.add(current_item)
                                        play_prompt_sound(current_item)
                                    else:
                                        used_items.clear()
                                        current_item = random.choice(letters if current_category == 'letters' else numbers if current_category == 'numbers' else who_items if current_category == 'who' else words)
                                        used_items.add(current_item)
                                        play_prompt_sound(current_item)
                                else:
                                    random.choice(wrong_sounds).play()
                                    # Get the correct item rect for arrow animation
                                    current_item_rect = [r for l, r in letter_positions if l == current_item]
                                    if current_item_rect:
                                        animate_wrong_item(rect, current_item_rect[0])

        # Refresh the screen
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
