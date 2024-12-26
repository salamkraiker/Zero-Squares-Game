import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

def show_start_screen():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)

    title_text = font.render("Zero Squares Game", True, BLACK)
    start_text = small_font.render("1. Start Game", True, BLACK)
    level_text = small_font.render("2. Select Level", True, BLACK)
    exit_text = small_font.render("3. Exit", True, BLACK)

    while True:
        screen.fill(WHITE)
        screen.blit(title_text, (50, 50))
        screen.blit(start_text, (50, 120))
        screen.blit(level_text, (50, 160))
        screen.blit(exit_text, (50, 200))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "start_game"
                elif event.key == pygame.K_2:
                    return "select_level"
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

def select_level_screen():
    screen = pygame.display.set_mode((400, 300))
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)

    levels = [f"Level {i+1}" for i in range(30)]
    selected_level = 0

    while True:
        screen.fill(WHITE)
        title_text = font.render("Select Level", True, BLACK)
        screen.blit(title_text, (50, 50))

        for i, level in enumerate(levels):
            color = BLACK if i == selected_level else GRAY
            level_text = small_font.render(level, True, color)
            screen.blit(level_text, (50, 120 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = (selected_level - 1) % len(levels)
                elif event.key == pygame.K_DOWN:
                    selected_level = (selected_level + 1) % len(levels)
                elif event.key == pygame.K_RETURN:
                    return selected_level


def main():
    choice = show_start_screen()
    if choice == "start_game":
        print("Starting Game...")
    elif choice == "select_level":
        selected_level = select_level_screen()
        print(f"Selected {selected_level}")

if __name__ == "__main__":
    main()
