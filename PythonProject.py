import pygame
import sys

# Ініціалізація PyGame
pygame.init()

# Розмір екрану та створення вікна гри
screen_size = (1280, 720)
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Jujutsu Kaisen')

# Кольори
GREEN = (124, 252, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BLUE = (0, 0, 255)

# Зображення персонажів
characters = {
    "Kugisaki Nobara (left)": pygame.image.load("Nobara_1.png").convert_alpha(),
    "Kugisaki Nobara (right)": pygame.image.load("Nobara_2.png").convert_alpha(),
    "Inumaki Toge (left)": pygame.image.load("Inumaki_1.png").convert_alpha(),
    "Inumaki Toge (right)": pygame.image.load("Inumaki_2.png").convert_alpha(),
    "Zen'in Maki (left)": pygame.image.load("Maki_1.png").convert_alpha(),
    "Zen'in Maki (right)": pygame.image.load("Maki_2.png").convert_alpha(),
    "Itadori Yūji (left)": pygame.image.load("Yugi_1.png").convert_alpha(),
    "Itadori Yūji (right)": pygame.image.load("Yugi_2.png").convert_alpha(),
    "Gojō Satoru (left)": pygame.image.load("Gojo_1.png").convert_alpha(),
    "Gojō Satoru (right)": pygame.image.load("Gojo_2.png").convert_alpha(),
    "Fushiguro Megumi (left)": pygame.image.load("Megumi_1.png").convert_alpha(),
    "Fushiguro Megumi (right)": pygame.image.load("Megumi_2.png").convert_alpha()
}

# Фон
background = pygame.image.load("arena.png")
background = pygame.transform.scale(background, screen_size)

# Ініціалізація персонажів
player1_character = "Inumaki Toge (left)"
player2_character = "Kugisaki Nobara (right)"
soldier_1 = characters[player1_character]
soldier_2 = characters[player2_character]

# Розміщення персонажів на екрані
rect_1 = soldier_1.get_rect(topleft=(200, 200))
rect_2 = soldier_2.get_rect(topleft=(1080, 200))

clock = pygame.time.Clock()

# Рахунок перемог
score = [0, 0]  # [player 1, player 2]

# Список для зберігання магічних атак
magic_attacks = []

# Кольори для атак
attack_colors = {
    "Kugisaki Nobara (left)": BLACK,
    "Kugisaki Nobara (right)": BLACK,
    "Inumaki Toge (left)": RED,
    "Inumaki Toge (right)": RED,
    "Zen'in Maki (left)": GREEN,
    "Zen'in Maki (right)": GREEN,
    "Itadori Yūji (left)": RED,
    "Itadori Yūji (right)": RED,
    "Gojō Satoru (left)": BLUE,
    "Gojō Satoru (right)": BLUE,
    "Fushiguro Megumi (left)": BLACK,
    "Fushiguro Megumi (right)": BLACK
}


# Функція виходу з гри
def exit_game():
    pygame.quit()
    sys.exit()


# Функція малювання полоски життя
def draw_health_bar(health, x, y, width, height):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, width + 4, height + 4))
    pygame.draw.rect(screen, RED, (x, y, width, height))
    pygame.draw.rect(screen, YELLOW, (x, y, width * ratio, height))


# Малювання тексту
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# Рахунок
def show_score():
    font = pygame.font.Font(None, 144)
    score_text = f"{score[0]} - {score[1]}"

    # Створення напівпрозорого чорного фону

    overlay = pygame.Surface(screen_size)
    overlay.set_alpha(128)  # Прозорість
    overlay.fill((0, 0, 0))

    # Намалювання напівпрозорого фону на екрані
    screen.blit(overlay, (0, 0))

    draw_text(score_text, font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(3000)


# Функція гри
def game():
    global soldier_1, soldier_2, rect_1, rect_2, score

    running = True
    music = pygame.mixer.Sound("Self-Embodiment Of Perfection (project).mp3")
    music.play(-1)

    health_1 = 100
    health_2 = 100

    rect_1 = soldier_1.get_rect(topleft=(200, 200))
    rect_2 = soldier_2.get_rect(topleft=(1080, 200))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    magic_attacks.append({"rect": pygame.Rect(rect_1.right, rect_1.centery, 35, 5),
                                          "player": player1_character})
                elif event.key == pygame.K_RETURN:
                    magic_attacks.append({"rect": pygame.Rect(rect_2.left - 10, rect_2.centery, 35, 5),
                                          "player": player2_character})

        screen.fill((0, 0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rect_2.move_ip(-5, 0)
        if keys[pygame.K_RIGHT]:
            rect_2.move_ip(5, 0)
        if keys[pygame.K_UP]:
            rect_2.move_ip(0, -5)
        if keys[pygame.K_DOWN]:
            rect_2.move_ip(0, 5)

        if keys[pygame.K_a]:
            rect_1.move_ip(-5, 0)
        if keys[pygame.K_d]:
            rect_1.move_ip(5, 0)
        if keys[pygame.K_w]:
            rect_1.move_ip(0, -5)
        if keys[pygame.K_s]:
            rect_1.move_ip(0, 5)

        for attack in magic_attacks:
            if attack["player"] == player1_character:
                attack["rect"].move_ip(10, 0)
                if attack["rect"].right >= WIDTH:
                    magic_attacks.remove(attack)
                elif rect_2.colliderect(attack["rect"]):
                    health_2 -= 5
                    magic_attacks.remove(attack)
            elif attack["player"] == player2_character:
                attack["rect"].move_ip(-10, 0)
                if attack["rect"].left <= 0:
                    magic_attacks.remove(attack)
                elif rect_1.colliderect(attack["rect"]):
                    health_1 -= 5
                    magic_attacks.remove(attack)

        screen.blit(background, (0, 0))
        screen.blit(soldier_1, rect_1)
        screen.blit(soldier_2, rect_2)

        draw_health_bar(health_1, 20, 20, 300, 30)
        draw_health_bar(health_2, WIDTH - 320, 20, 300, 30)

        draw_text(f"{player1_character}: {score[0]}", pygame.font.Font(None, 30), WHITE, screen, 170, 70)
        draw_text(f"{player2_character}: {score[1]}", pygame.font.Font(None, 30), WHITE, screen, WIDTH - 170, 70)

        for attack in magic_attacks:
            pygame.draw.rect(screen, attack_colors[attack["player"]], attack["rect"])

        pygame.display.flip()
        clock.tick(60)

        # Провірка на завершення гри
        if health_1 <= 0 or health_2 <= 0:
            if health_1 > health_2:
                score[0] += 1
            else:
                score[1] += 1
            show_score()
            break

    music.stop()


# Настройки
def settings_menu():
    global player1_character, player2_character

    menu_items = [f"Player 1: {player1_character}", f"Player 2: {player2_character}", "Back"]
    menu_font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)
    hover_color = GRAY

    menu_rects = []
    for i, item in enumerate(menu_items):
        text_surface = menu_font.render(item, True, text_color)
        rect = text_surface.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 + i * 60))
        menu_rects.append((item, text_surface, rect))

    while True:
        screen.fill((0, 0, 0))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (item, _, rect) in enumerate(menu_rects):
                    if rect.collidepoint(event.pos):
                        if item == "Back":
                            return
                        elif "Player 1" in item:
                            player1_character_choice()
                        elif "Player 2" in item:
                            player2_character_choice()

        menu_items = [f"Player 1: {player1_character}", f"Player 2: {player2_character}", "Back"]
        menu_rects = []
        for i, item in enumerate(menu_items):
            text_surface = menu_font.render(item, True, text_color)
            rect = text_surface.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 + i * 60))
            menu_rects.append((item, text_surface, rect))

        for i, (item, text_surface, rect) in enumerate(menu_rects):
            if rect.collidepoint(mx, my):
                text_surface = menu_font.render(item, True, hover_color)
            else:
                text_surface = menu_font.render(item, True, text_color)
            screen.blit(text_surface, rect)

        pygame.display.flip()
        clock.tick(30)


# Вибір персонажа для гравця 1
def player1_character_choice():
    global soldier_1, player1_character

    menu_items = [item for item in characters.keys() if "left" in item] + ["Back"]
    menu_font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)
    hover_color = GRAY

    # Позиціонування елементів меню
    menu_rects = []
    for i, item in enumerate(menu_items):
        text_surface = menu_font.render(item, True, text_color)
        rect = text_surface.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 +
                                             (i - len(menu_items) // 2) * 60))
        menu_rects.append((item, text_surface, rect))

    while True:
        screen.fill((0, 0, 0))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (item, _, rect) in enumerate(menu_rects):
                    if rect.collidepoint(event.pos):
                        if item == "Back":
                            return
                        else:
                            player1_character = item
                            soldier_1 = characters[player1_character]
                            return
        # Малювання елементів меню
        for i, (item, text_surface, rect) in enumerate(menu_rects):
            if rect.collidepoint(mx, my):
                text_surface = menu_font.render(item, True, hover_color)
            else:
                text_surface = menu_font.render(item, True, text_color)
            screen.blit(text_surface, rect)

        pygame.display.flip()
        clock.tick(30)


# Вибір персонажа для гравця 2
def player2_character_choice():
    global soldier_2, player2_character

    menu_items = [item for item in characters.keys() if "right" in item] + ["Back"]
    menu_font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)
    hover_color = GRAY

    # Позиціонування елементів меню
    menu_rects = []
    for i, item in enumerate(menu_items):
        text_surface = menu_font.render(item, True, text_color)
        rect = text_surface.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 +
                                             (i - len(menu_items) // 2) * 60))
        menu_rects.append((item, text_surface, rect))

    while True:
        screen.fill((0, 0, 0))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (item, _, rect) in enumerate(menu_rects):
                    if rect.collidepoint(event.pos):
                        if item == "Back":
                            return
                        else:
                            player2_character = item
                            soldier_2 = characters[player2_character]
                            return

        # Малювання елементів меню
        for i, (item, text_surface, rect) in enumerate(menu_rects):
            if rect.collidepoint(mx, my):
                text_surface = menu_font.render(item, True, hover_color)
            else:
                text_surface = menu_font.render(item, True, text_color)
            screen.blit(text_surface, rect)

        pygame.display.flip()
        clock.tick(30)


# Головне меню
def main_menu():
    menu_items = ["Start", "Settings", "Exit"]
    menu_font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)
    hover_color = (200, 200, 200)

    # Позиціонування елементів меню
    menu_rects = []
    for i, item in enumerate(menu_items):
        text_surface = menu_font.render(item, True, text_color)
        rect = text_surface.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 + i * 60))
        menu_rects.append((text_surface, rect))

    while True:
        screen.fill((0, 0, 0))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (_, rect) in enumerate(menu_rects):
                    if rect.collidepoint(event.pos):
                        if menu_items[i] == "Start":
                            game()
                        elif menu_items[i] == "Settings":
                            settings_menu()
                        elif menu_items[i] == "Exit":
                            exit_game()

        # Малювання елементів меню
        for i, (text_surface, rect) in enumerate(menu_rects):
            if rect.collidepoint(mx, my):
                text_surface = menu_font.render(menu_items[i], True, hover_color)
            else:
                text_surface = menu_font.render(menu_items[i], True, text_color)
            screen.blit(text_surface, rect)

        pygame.display.flip()
        clock.tick(30)


# Запуск головного меню
if __name__ == "__main__":
    main_menu()
