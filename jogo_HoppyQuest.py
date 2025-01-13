# type: ignore
import pgzrun
import random
from pgzero.rect import Rect

# definir tamanho da tela do jogo
WIDTH = 800
HEIGHT = 400

# variaveis globais
LIVES = 3
SCORE = 0

# musica do fundo do jogo - background 
if hasattr(music, 'play'):
    music.play('background')

# Variable for music control
music_on = True

# Animacao dos frames do personagem
frames_right = [f'rabbitrun{i}_r' for i in range(8)]  # direita
frames_left = [f'rabbitrun{i}_l' for i in range(8)]   # esquerda
idle_frames = [f'idle_frame_{i}' for i in range(6)]   # parado 

# Character setup
current_frame = 0
character = Actor(frames_right[0], (100, HEIGHT - 50))  # Adjust Y position to align with the ground
speed = 5
idle_speed = 0.2  # Idle animation speed

# Background setup
backgrounds = [Actor(f'backgroud_game{i}', (WIDTH * i, HEIGHT / 2)) for i in range(3)]
for bg in backgrounds:
    bg.width = WIDTH
    bg.height = HEIGHT

background_speed = 2

# Enemies setup
enemy_frames = [f"enemy_frame_{i}" for i in range(10)]
enemies = []
current_enemy_frame = 0
spawn_timer = 0
enemy_speed = 1
# Enemy animation speed
enemy_frame_speed = 0.2
enemy_frame_counter = 0


# Coins setup
coin_frames = [f"coin_{i}" for i in range(6)]
coins = [Actor(coin_frames[0], (random.randint(WIDTH // 2, WIDTH), random.randint(50, HEIGHT - 50))) for _ in range(5)]
current_coin_frame = 0
coin_speed = 2

# Jump variables
is_jumping = False
jump_velocity = -20
gravity = 1
jump_count = 0
max_jumps = 3

# Game states
game_over = False

# Function to draw the main menu
def draw_menu():
    screen.clear()
    menu_background = Actor('start_new', (WIDTH / 2, HEIGHT / 2))
    menu_background.draw()

    # Button settings
    button_width = 180
    button_height = 30
    button_color = (174, 222, 203)  # Soft green color
    text_color = "black"

    # Buttons positions
    buttons = [
        ("Start Game", (WIDTH / 2, 270)),
        (f"Music: {'On' if music_on else 'Off'}", (WIDTH / 2, 310)),
        ("Exit", (WIDTH / 2, 350))
    ]

    # Draw buttons
    for text, position in buttons:
        rect = Rect((position[0] - button_width / 2, position[1] - button_height / 2), (button_width, button_height))
        screen.draw.filled_rect(rect, button_color)
        screen.draw.text(text, center=position, fontsize=30, color=text_color)


# Function to draw the game over screen
def draw_game_over():
    global SCORE

    screen.clear()
    gameover_background = Actor('gameover', (WIDTH / 2, HEIGHT / 2))
    gameover_background.draw()
    screen.draw.text("Voltar ao menu", center=(WIDTH / 2, 300), fontsize=30, color="black")
    screen.draw.text(f"Score: {SCORE}", center=(WIDTH / 2, 350), fontsize=50, color="black")

# Function to switch between menu and game
menu_active = True

def draw():
    global LIVES, SCORE

    if game_over:
        draw_game_over()
    elif menu_active:
        draw_menu()
    else:
        screen.clear()
        for bg in backgrounds:
            bg.draw()
        character.draw()
        for enemy in enemies:
            enemy.draw()
        for coin in coins:
            coin.draw()
        screen.draw.text(f"Sair: ESC", center=(WIDTH / 2, 15), fontsize=20, color="white")
        screen.draw.text(f"Lives: {LIVES}", (10, 30), fontsize=30, color="white")
        screen.draw.text(f"Score: {SCORE}", (10, 60), fontsize=30, color="white")


# Function to update movement and animation
def update():
    global current_frame, menu_active, music_on, is_jumping, jump_velocity, gravity, jump_count, current_enemy_frame, spawn_timer, LIVES, SCORE, current_coin_frame, game_over, enemy_frame_speed, enemy_frame_counter

    if menu_active or game_over:
        return

    # Check if character is idle
    if not keyboard.left and not keyboard.right and not is_jumping:
        current_frame += idle_speed
        if current_frame >= len(idle_frames):
            current_frame = 0
        character.image = idle_frames[int(current_frame)]  # Ensure current_frame is an integer

    # Update character movement
    if keyboard.left:
        character.x = max(0, character.x - speed)
        current_frame = int((current_frame + 1) % len(frames_left))  # Ensure current_frame is an integer
        character.image = frames_left[current_frame]
        for bg in backgrounds:
            bg.x += background_speed
    elif keyboard.right:
        character.x = min(WIDTH - 100, character.x + speed)
        current_frame = int((current_frame + 1) % len(frames_right))  # Ensure current_frame is an integer
        character.image = frames_right[current_frame]
        for bg in backgrounds:
            bg.x -= background_speed

    # Jump and gravity logic
    if is_jumping:
        character.y += jump_velocity
        jump_velocity += gravity
        if character.y >= HEIGHT - 50:
            character.y = HEIGHT - 50
            is_jumping = False
            jump_velocity = -12
            jump_count = 0

    # Loop background images
    if backgrounds[0].x <= -WIDTH:
        backgrounds[0].x = backgrounds[2].x + WIDTH
    if backgrounds[1].x <= -WIDTH:
        backgrounds[1].x = backgrounds[0].x + WIDTH
    if backgrounds[2].x <= -WIDTH:
        backgrounds[2].x = backgrounds[1].x + WIDTH

    # Enemy spawning logic
    spawn_timer += 1
    if spawn_timer > random.randint(50, 100):
        spawn_timer = 0
        if len(enemies) < 1:
            enemy = Actor(enemy_frames[0], (WIDTH + random.randint(100, 300), HEIGHT - 45))
            enemies.append(enemy)

    # Enemy movement and animation
    for enemy in enemies:
        enemy.x -= enemy_speed
        if enemy.x < -enemy.width:
            enemies.remove(enemy)

        # Update enemy animation frame
        enemy_frame_counter += enemy_frame_speed
        if enemy_frame_counter >= 1:
            enemy_frame_counter = 0
            current_enemy_frame = (current_enemy_frame + 1) % len(enemy_frames)
            enemy.image = enemy_frames[current_enemy_frame]

        # Check for collision with the character
        if character.colliderect(enemy):
            LIVES -= 1
            enemies.remove(enemy)
            if music_on and hasattr(sounds, 'point_loss'):
                sounds.point_loss.play()
            if LIVES <= 0:
                game_over = True
                music.stop()
                if music_on and hasattr(sounds, 'game_over'):
                    sounds.game_over.play()


    # Coins animation and movement
    current_coin_frame = int((current_coin_frame + 1) % len(coin_frames))  # Ensure current_coin_frame is an integer
    for coin in coins:
        coin.image = coin_frames[current_coin_frame]
        coin.x -= coin_speed
        if coin.x < -coin.width:
            coin.x = WIDTH + random.randint(50, 200)
            coin.y = random.randint(50, HEIGHT - 50)

        # Check for collision with the character
        if character.colliderect(coin):
            SCORE += 1
            coins.remove(coin)
            if music_on and hasattr(sounds, 'point_win'):
                sounds.point_win.play()  # Play point loss sound from music folder            
            new_coin = Actor(coin_frames[0], (WIDTH + random.randint(50, 200), random.randint(50, HEIGHT - 50)))
            coins.append(new_coin)

# funcao para resetar o jogo
def reset_game():
    global LIVES, SCORE, enemies, coins, character, is_jumping, jump_velocity, jump_count, music_on

    # Reset enemies and coins
    enemies.clear()
    coins.clear()
    LIVES = 3
    SCORE = 0

    # Recreate initial coins
    coins.extend([Actor(coin_frames[0], (random.randint(WIDTH // 2, WIDTH), random.randint(50, HEIGHT - 50))) for _ in range(5)])

    # Reset character position and jump state
    character.pos = (100, HEIGHT - 50)
    is_jumping = False
    jump_velocity = -20
    jump_count = 0

    # iniciar a musica de fundo
    if music_on and hasattr(music, 'play'):
        music.play('background')


# Function to capture mouse clicks in the main menu or game over screen
def on_mouse_down(pos):
    global menu_active, music_on, game_over

    if game_over:
        game_over = False
        menu_active = True
        reset_game()  # Reset game variables when returning to the menu
    elif menu_active:
        if Rect((WIDTH / 2 - 100, 250), (200, 50)).collidepoint(pos):
            menu_active = False
        elif Rect((WIDTH / 2 - 100, 300), (200, 50)).collidepoint(pos):
            music_on = not music_on
            if music_on:
                music.play('background')
            else:
                music.stop()
        elif Rect((WIDTH / 2 - 100, 350), (200, 50)).collidepoint(pos):
            exit()

def on_key_down(key):
    global is_jumping, jump_velocity, jump_count, max_jumps

    # Sair do jogo ao pressionar ESC
    if key == keys.ESCAPE:
        exit()
    
    if key == keys.SPACE:
        if jump_count < max_jumps:
            is_jumping = True
            jump_velocity = -12
            jump_count += 1

# Start the game
pgzrun.go()
