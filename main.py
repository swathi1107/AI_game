import pygame
import random
import sys
import os
import json

# AI Robot Rescue - a beginner-friendly Python/Pygame endless runner
# Controls: LEFT/RIGHT to change lanes, UP or SPACE to jump, DOWN to slide.
# Answer learning questions when prompted. Press ESC to quit.

pygame.init()
pygame.display.set_caption("AI Robot Rescue — Run, Learn, Survive")
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

# Colors
BG = (13, 20, 38)
ROAD = (34, 44, 67)
LANE = (75, 94, 128)
WHITE = (245, 248, 255)
CYAN = (57, 220, 235)
YELLOW = (255, 212, 77)
RED = (255, 93, 110)
GREEN = (96, 235, 156)
PURPLE = (166, 133, 255)
DARK = (8, 12, 24)

ROAD_LEFT, ROAD_RIGHT = 190, 810
LANES = [300, 500, 700]
PLAYER_Y = 500
SAVE_FILE = "best_score.json"

QUESTIONS = [
    {"q": "What does AI stand for?", "options": ["Artificial Intelligence", "Automatic Internet", "Advanced Input"], "answer": 0, "fact": "AI helps computers perform tasks that usually need human intelligence."},
    {"q": "Which is a strong password?", "options": ["123456", "robot", "R0b0t!Safe_82"], "answer": 2, "fact": "Use long, unique passwords and enable multi-factor authentication."},
    {"q": "What should you do with a suspicious link?", "options": ["Click quickly", "Check it; don't click if unsure", "Send it to everyone"], "answer": 1, "fact": "Phishing messages try to trick people into revealing information."},
    {"q": "What is a dataset?", "options": ["A collection of data", "A computer cable", "A game level"], "answer": 0, "fact": "AI systems often learn patterns from examples in datasets."},
    {"q": "Which information should you keep private online?", "options": ["Your password", "A public weather report", "A public science fact"], "answer": 0, "fact": "Never share passwords or one-time passcodes."},
    {"q": "What does a firewall help do?", "options": ["Cook food", "Filter network traffic", "Charge a laptop"], "answer": 1, "fact": "A firewall helps control incoming and outgoing network traffic."},
    {"q": "Can AI sometimes make mistakes?", "options": ["No, never", "Yes, it can", "Only at night"], "answer": 1, "fact": "Always check important AI-generated information."},
]

def load_best():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return int(json.load(f).get("best", 0))
    except (OSError, ValueError, json.JSONDecodeError):
        return 0

def save_best(value):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({"best": int(value)}, f)
    except OSError:
        pass

def draw_text(text, font_size, color, x, y, center=False, bold=False):
    font = pygame.font.SysFont("arial", font_size, bold=bold)
    surface = font.render(str(text), True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)
    return rect

def rounded_rect(color, rect, radius=12, border=None, width=2):
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(screen, border, rect, width, border_radius=radius)

def draw_background(offset):
    screen.fill(BG)
    # subtle stars
    for i in range(45):
        x = (i * 97 + 23) % WIDTH
        y = (i * 53 + 17) % HEIGHT
        pygame.draw.circle(screen, (38, 53, 82), (x, y), 1)
    pygame.draw.rect(screen, ROAD, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
    pygame.draw.line(screen, LANE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
    pygame.draw.line(screen, LANE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)
    # lane dashes move with the world
    dash_offset = int(offset) % 90
    for x in [400, 600]:
        for y in range(-90, HEIGHT + 90, 90):
            yy = y + dash_offset
            pygame.draw.rect(screen, (78, 91, 122), (x - 3, yy, 6, 42), border_radius=3)
    # side decorations
    for y in range(-70, HEIGHT + 80, 140):
        yy = (y + int(offset * 0.55)) % (HEIGHT + 140) - 70
        pygame.draw.circle(screen, (23, 47, 68), (130, yy), 25, 3)
        pygame.draw.circle(screen, (23, 47, 68), (870, yy), 25, 3)

def draw_robot(x, y, jumping=False, sliding=False):
    # Shadow
    pygame.draw.ellipse(screen, (7, 11, 20), (x - 38, PLAYER_Y + 42, 76, 17))
    if sliding:
        # horizontal robot pose
        rounded_rect((130, 151, 178), (x - 38, y + 5, 76, 37), 12, CYAN, 3)
        rounded_rect((205, 229, 244), (x - 28, y - 5, 42, 34), 10, CYAN, 3)
        pygame.draw.circle(screen, DARK, (x - 15, y + 8), 4)
        pygame.draw.circle(screen, DARK, (x + 1, y + 8), 4)
        pygame.draw.line(screen, CYAN, (x - 25, y + 42), (x - 43, y + 49), 6)
        pygame.draw.line(screen, CYAN, (x + 24, y + 42), (x + 42, y + 49), 6)
    else:
        body_y = y + (8 if jumping else 0)
        rounded_rect((130, 151, 178), (x - 29, body_y - 3, 58, 58), 13, CYAN, 3)
        rounded_rect((205, 229, 244), (x - 31, body_y - 39, 62, 43), 12, CYAN, 3)
        pygame.draw.circle(screen, DARK, (x - 13, body_y - 23), 5)
        pygame.draw.circle(screen, DARK, (x + 13, body_y - 23), 5)
        pygame.draw.line(screen, CYAN, (x, body_y - 40), (x, body_y - 51), 3)
        pygame.draw.circle(screen, YELLOW, (x, body_y - 54), 5)
        pygame.draw.line(screen, CYAN, (x - 21, body_y + 55), (x - 27, body_y + 72), 7)
        pygame.draw.line(screen, CYAN, (x + 21, body_y + 55), (x + 27, body_y + 72), 7)
        pygame.draw.line(screen, CYAN, (x - 29, body_y + 12), (x - 41, body_y + 29), 6)
        pygame.draw.line(screen, CYAN, (x + 29, body_y + 12), (x + 41, body_y + 29), 6)

def draw_obstacle(obj):
    x, y = LANES[obj["lane"]], obj["y"]
    if obj["type"] == "barrier":
        rounded_rect((105, 42, 62), (x - 43, y - 20, 86, 48), 9, RED, 3)
        for k in range(3):
            pygame.draw.line(screen, (255, 160, 162), (x - 31 + k * 25, y - 15), (x - 17 + k * 25, y + 22), 5)
    elif obj["type"] == "gate":
        pygame.draw.rect(screen, PURPLE, (x - 43, y - 58, 13, 70), border_radius=5)
        pygame.draw.rect(screen, PURPLE, (x + 30, y - 58, 13, 70), border_radius=5)
        pygame.draw.rect(screen, (125, 96, 216), (x - 43, y - 61, 86, 18), border_radius=5)
        draw_text("SLIDE", 12, WHITE, x, y - 42, center=True, bold=True)
    else:
        rounded_rect((37, 94, 108), (x - 29, y - 32, 58, 58), 12, GREEN, 3)
        draw_text("+", 30, WHITE, x, y - 3, center=True, bold=True)

def reset_game():
    return {
        "lane": 1, "obstacles": [], "distance": 0.0, "score": 0, "energy": 0,
        "speed": 5.0, "spawn": 0, "jump_timer": 0, "slide_timer": 0,
        "game_over": False, "question": None, "question_index": 0,
        "question_wait": False, "feedback": "", "feedback_timer": 0,
        "next_question": 650, "flash": 0
    }

best_score = load_best()
game = reset_game()
state = "menu"  # menu, playing, question, gameover

def spawn_obstacle():
    roll = random.random()
    kind = "energy" if roll < 0.25 else ("gate" if roll < 0.55 else "barrier")
    return {"lane": random.randrange(3), "y": -50, "type": kind, "passed": False}

def start_question():
    game["question"] = random.choice(QUESTIONS)
    game["question_wait"] = True
    game["feedback"] = ""
    game["feedback_timer"] = 0

def handle_answer(index):
    q = game["question"]
    if q is None:
        return
    if index == q["answer"]:
        game["score"] += 50
        game["feedback"] = "Correct! +50 points"
        game["flash"] = 12
    else:
        game["feedback"] = "Not quite — learn this fact!"
    game["feedback_timer"] = 150
    game["question_wait"] = False

def end_game():
    global state, best_score
    game["game_over"] = True
    state = "gameover"
    if game["score"] > best_score:
        best_score = game["score"]
        save_best(best_score)

def draw_hud():
    rounded_rect((18, 28, 49), (22, 18, 220, 90), 15, (53, 76, 110), 2)
    draw_text(f"SCORE  {game['score']}", 24, WHITE, 40, 31, bold=True)
    draw_text(f"ENERGY  {game['energy']}", 18, GREEN, 40, 67, bold=True)
    rounded_rect((18, 28, 49), (760, 18, 218, 90), 15, (53, 76, 110), 2)
    draw_text(f"BEST  {best_score}", 20, YELLOW, 780, 31, bold=True)
    draw_text(f"SPEED  {game['speed']:.1f}", 18, CYAN, 780, 65, bold=True)

def draw_panel(title, subtitle=None):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((4, 8, 18, 190))
    screen.blit(overlay, (0, 0))
    rounded_rect((20, 31, 57), (175, 115, 650, 425), 24, (63, 93, 140), 3)
    draw_text(title, 38, CYAN, WIDTH // 2, 165, center=True, bold=True)
    if subtitle:
        draw_text(subtitle, 20, WHITE, WIDTH // 2, 210, center=True)

def draw_menu():
    draw_background(game["distance"] * 2)
    draw_robot(500, 405)
    draw_text("AI ROBOT RESCUE", 46, CYAN, WIDTH // 2, 115, center=True, bold=True)
    draw_text("RUN  •  LEARN  •  SURVIVE", 22, WHITE, WIDTH // 2, 165, center=True, bold=True)
    rounded_rect((22, 42, 70), (315, 260, 370, 65), 15, CYAN, 2)
    draw_text("PRESS ENTER TO START", 23, WHITE, WIDTH // 2, 292, center=True, bold=True)
    draw_text("← → Move lanes     ↑ / SPACE Jump     ↓ Slide", 18, (203, 215, 235), WIDTH // 2, 365, center=True)
    draw_text("Collect green energy cells. Avoid red barriers and slide under purple gates.", 16, (170, 187, 215), WIDTH // 2, 400, center=True)
    draw_text("Answer AI & cybersecurity questions to earn bonus points.", 16, (170, 187, 215), WIDTH // 2, 428, center=True)
    draw_text(f"Best score: {best_score}", 18, YELLOW, WIDTH // 2, 490, center=True, bold=True)

def draw_question():
    draw_panel("LEARNING CHECKPOINT", "Choose the correct answer (1, 2, or 3)")
    q = game["question"]
    if not q:
        return
    # wrap question manually for readable layout
    draw_text(q["q"], 24, WHITE, WIDTH // 2, 260, center=True, bold=True)
    for i, option in enumerate(q["options"]):
        rect = pygame.Rect(245, 300 + i * 54, 510, 43)
        rounded_rect((32, 48, 78), rect, 10, (75, 103, 151), 2)
        draw_text(f"{i+1}.  {option}", 19, WHITE, rect.x + 18, rect.y + 10)
    draw_text("Correct answers give +50 points.", 16, GREEN, WIDTH // 2, 480, center=True)
    if game["feedback"]:
        draw_text(game["feedback"], 20, YELLOW if "Correct" in game["feedback"] else RED, WIDTH // 2, 515, center=True, bold=True)
        draw_text(q["fact"], 15, (190, 205, 229), WIDTH // 2, 540, center=True)

def draw_gameover():
    draw_background(game["distance"] * 2)
    draw_robot(500, 405)
    draw_panel("MISSION ENDED", "The robot needs a recharge!")
    draw_text(f"Your score: {game['score']}", 27, WHITE, WIDTH // 2, 275, center=True, bold=True)
    draw_text(f"Energy collected: {game['energy']}", 21, GREEN, WIDTH // 2, 320, center=True)
    draw_text(f"Best score: {best_score}", 21, YELLOW, WIDTH // 2, 355, center=True)
    rounded_rect((22, 42, 70), (335, 405, 330, 55), 13, CYAN, 2)
    draw_text("PRESS ENTER TO PLAY AGAIN", 19, WHITE, WIDTH // 2, 432, center=True, bold=True)
    draw_text("Press ESC to quit", 16, (180, 194, 220), WIDTH // 2, 485, center=True)

def move_lane(direction):
    game["lane"] = max(0, min(2, game["lane"] + direction))

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif state == "menu":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    game = reset_game()
                    state = "playing"
            elif state == "gameover":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    game = reset_game()
                    state = "playing"
            elif state == "playing":
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    move_lane(-1)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    move_lane(1)
                elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                    if game["jump_timer"] <= 0 and game["slide_timer"] <= 0:
                        game["jump_timer"] = 42
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if game["slide_timer"] <= 0 and game["jump_timer"] <= 0:
                        game["slide_timer"] = 34
            elif state == "question":
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3) and game["question_wait"]:
                    handle_answer(event.key - pygame.K_1)

    if state == "playing":
        game["distance"] += game["speed"]
        game["score"] += 1
        game["speed"] = min(11.0, 5.0 + game["distance"] / 6000)
        game["spawn"] += 1
        if game["spawn"] > max(34, 78 - int(game["speed"] * 3)):
            game["obstacles"].append(spawn_obstacle())
            game["spawn"] = 0
        if game["jump_timer"] > 0:
            game["jump_timer"] -= 1
        if game["slide_timer"] > 0:
            game["slide_timer"] -= 1
        if game["flash"] > 0:
            game["flash"] -= 1

        player_x = LANES[game["lane"]]
        player_jump = game["jump_timer"] > 0
        player_slide = game["slide_timer"] > 0
        player_y = PLAYER_Y - (95 * (1 - abs(game["jump_timer"] - 21) / 21) if player_jump else 0)

        for obj in list(game["obstacles"]):
            obj["y"] += game["speed"]
            if obj["y"] > HEIGHT + 80:
                game["obstacles"].remove(obj)
                continue
            # collision window near the robot
            if abs(obj["y"] - PLAYER_Y) < 35 and obj["lane"] == game["lane"]:
                if obj["type"] == "energy":
                    game["energy"] += 1
                    game["score"] += 25
                    game["obstacles"].remove(obj)
                elif obj["type"] == "barrier" and not player_jump:
                    end_game()
                    break
                elif obj["type"] == "gate" and not player_slide:
                    end_game()
                    break

        if state == "playing" and game["distance"] >= game["next_question"]:
            game["next_question"] += random.randint(700, 1000)
            start_question()
            state = "question"

    elif state == "question":
        if not game["question_wait"] and game["feedback_timer"] > 0:
            game["feedback_timer"] -= 1
            if game["feedback_timer"] <= 0:
                game["question"] = None
                state = "playing"

    if state == "menu":
        draw_menu()
    elif state == "playing":
        draw_background(game["distance"] * 2)
        for obj in game["obstacles"]:
            draw_obstacle(obj)
        x = LANES[game["lane"]]
        jumping = game["jump_timer"] > 0
        sliding = game["slide_timer"] > 0
        y = PLAYER_Y - (95 * (1 - abs(game["jump_timer"] - 21) / 21) if jumping else 0)
        draw_robot(x, int(y), jumping, sliding)
        draw_hud()
        if game["flash"] > 0:
            pygame.draw.rect(screen, (100, 255, 180), (0, 0, WIDTH, HEIGHT), 5)
    elif state == "question":
        draw_background(game["distance"] * 2)
        for obj in game["obstacles"]:
            draw_obstacle(obj)
        draw_robot(LANES[game["lane"]], PLAYER_Y)
        draw_hud()
        draw_question()
    elif state == "gameover":
        draw_gameover()

    pygame.display.flip()

pygame.quit()
sys.exit()
