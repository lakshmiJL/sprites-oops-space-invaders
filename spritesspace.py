import pygame
import os

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Set up display
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# Load assets
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('/Users/Kuttimma/Documents/Official/JetLearn/GameDev2/Lesson6/Assets', 'ship1.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('/Users/Kuttimma/Documents/Official/JetLearn/GameDev2/Lesson6/Assets', 'ship2.png'))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('/Users/Kuttimma/Documents/Official/JetLearn/GameDev2/Lesson6/Assets', 'space.png')), (WIDTH, HEIGHT))

# Set constants
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Load fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(
            YELLOW_SPACESHIP_IMAGE if color == 'yellow' else RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90 if color == 'yellow' else 270)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.color = color
        self.health = 10

    def handle_movement(self, keys_pressed):
        if self.color == 'yellow':
            if keys_pressed[pygame.K_a] and self.rect.x - VEL > 0:  # LEFT
                self.rect.x -= VEL
            if keys_pressed[pygame.K_d] and self.rect.x + VEL + self.rect.width < BORDER.x:  # RIGHT
                self.rect.x += VEL
            if keys_pressed[pygame.K_w] and self.rect.y - VEL > 0:  # UP
                self.rect.y -= VEL
            if keys_pressed[pygame.K_s] and self.rect.y + VEL + self.rect.height < HEIGHT - 15:  # DOWN
                self.rect.y += VEL
        elif self.color == 'red':
            if keys_pressed[pygame.K_LEFT] and self.rect.x - VEL > BORDER.x + BORDER.width:  # LEFT
                self.rect.x -= VEL
            if keys_pressed[pygame.K_RIGHT] and self.rect.x + VEL + self.rect.width < WIDTH:  # RIGHT
                self.rect.x += VEL
            if keys_pressed[pygame.K_UP] and self.rect.y - VEL > 0:  # UP
                self.rect.y -= VEL
            if keys_pressed[pygame.K_DOWN] and self.rect.y + VEL + self.rect.height < HEIGHT - 15:  # DOWN
                self.rect.y += VEL


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = color
        self.rect = pygame.Rect(x, y, 10, 5)
    
    def update(self):
        if self.color == 'yellow':
            self.rect.x += BULLET_VEL
            if self.rect.x > WIDTH:
                self.kill()
        elif self.color == 'red':
            self.rect.x -= BULLET_VEL
            if self.rect.x < 0:
                self.kill()


def draw_window(red, yellow, red_bullets, yellow_bullets):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(f"Health: {red.health}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow.health}", 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(yellow.image, yellow.rect.topleft)
    WIN.blit(red.image, red.rect.topleft)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet.rect)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet.rect)

    pygame.display.update()


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        if red.rect.colliderect(bullet.rect):
            pygame.event.post(pygame.event.Event(RED_HIT))
            bullet.kill()

    for bullet in red_bullets:
        if yellow.rect.colliderect(bullet.rect):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            bullet.kill()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = Spaceship(700, 300, 'red')
    yellow = Spaceship(100, 300, 'yellow')

    red_bullets = pygame.sprite.Group()
    yellow_bullets = pygame.sprite.Group()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = Bullet(yellow.rect.x + yellow.rect.width, yellow.rect.y + yellow.rect.height // 2 - 2, 'yellow')
                    yellow_bullets.add(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = Bullet(red.rect.x, red.rect.y + red.rect.height // 2 - 2, 'red')
                    red_bullets.add(bullet)

            if event.type == RED_HIT:
                red.health -= 1

            if event.type == YELLOW_HIT:
                yellow.health -= 1

        winner_text = ""
        if red.health <= 0:
            winner_text = "Yellow Wins!"

        if yellow.health <= 0:
            winner_text = "Red Wins!"

        if winner_text:
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow.handle_movement(keys_pressed)
        red.handle_movement(keys_pressed)

        yellow_bullets.update()
        red_bullets.update()

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets)

    main()


if __name__ == "__main__":
    main()
