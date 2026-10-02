import pygame
import random
import sys

pygame.init()

# Window settings
WIDTH, HEIGHT = 1100, 650
FPS = 60

# Colours
WHITE = (255, 255, 255)
BLACK = (10, 10, 20)
YELLOW = (255, 220, 50)
RED = (220, 60, 60)
GREEN = (70, 200, 90)
BLUE = (70, 150, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Battle AI")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("arial", 28)
large_font = pygame.font.SysFont("arial", 60, bold=True)

# Game settings
SHIP_WIDTH = 70
SHIP_HEIGHT = 50
SHIP_SPEED = 5

BULLET_WIDTH = 12
BULLET_HEIGHT = 5
BULLET_SPEED = 8

MAX_HEALTH = 10
MAX_BULLETS = 3
PLAYER_FIRE_COOLDOWN = 15

class Spaceship:
    def __init__(self, x, y, colour, facing_right):
        self.rect = pygame.Rect(x, y, SHIP_WIDTH, SHIP_HEIGHT)
        self.colour = colour
        self.facing_right = facing_right
        self.health = MAX_HEALTH

    def draw(self):
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=8)

        # Cockpit
        cockpit = pygame.Rect(
            self.rect.x + 15,
            self.rect.y + 10,
            20,
            15,
        )
        pygame.draw.rect(screen, BLACK, cockpit, border_radius=4)

        # Engine
        if self.facing_right:
            engine_x = self.rect.left - 8
        else:
            engine_x = self.rect.right - 2

        engine = pygame.Rect(
            engine_x,
            self.rect.y + 17,
            10,
            16,
        )
        pygame.draw.rect(screen, BLUE, engine)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        # Keep the spaceship inside the screen
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(80, min(HEIGHT - self.rect.height - 20, self.rect.y))


class Bullet:
    def __init__(self, x, y, direction, colour):
        self.rect = pygame.Rect(x, y, BULLET_WIDTH, BULLET_HEIGHT)
        self.direction = direction
        self.colour = colour

    def move(self):
        self.rect.x += self.direction * BULLET_SPEED

    def draw(self):
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=3)

    def is_off_screen(self):
        return self.rect.right < 0 or self.rect.left > WIDTH


def draw_health_bar(x, y, health, colour, label):
    pygame.draw.rect(screen, WHITE, (x, y, 300, 25), 2)

    health_width = max(0, int(296 * health / MAX_HEALTH))
    pygame.draw.rect(
        screen,
        colour,
        (x + 2, y + 2, health_width, 21),
    )

    text = font.render(f"{label}: {health}", True, WHITE)
    screen.blit(text, (x, y - 35))


def draw_background():
    screen.fill(BLACK)

    # Simple stars
    random.seed(10)

    for _ in range(80):
        x = random.randint(0, WIDTH)
        y = random.randint(80, HEIGHT)
        pygame.draw.circle(screen, WHITE, (x, y), 1)


def create_bullet(ship, direction):
    if direction == 1:
        x = ship.rect.right
    else:
        x = ship.rect.left - BULLET_WIDTH

    y = ship.rect.centery - BULLET_HEIGHT // 2

    return Bullet(x, y, direction, ship.colour)


def draw_center_text(text, colour=WHITE):
    rendered = large_font.render(text, True, colour)
    screen.blit(
        rendered,
        (
            WIDTH // 2 - rendered.get_width() // 2,
            HEIGHT // 2 - rendered.get_height() // 2,
        ),
    )


def reset_game():
    player = Spaceship(
        100,
        HEIGHT // 2 - SHIP_HEIGHT // 2,
        RED,
        True,
    )

    ai = Spaceship(
        WIDTH - 170,
        HEIGHT // 2 - SHIP_HEIGHT // 2,
        YELLOW,
        False,
    )

    return player, ai, [], [], 0


def main():
    player, ai, player_bullets, ai_bullets, ai_fire_timer = reset_game()
    player_fire_timer = 0

    running = True
    game_over = False
    winner = ""

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if game_over and event.key == pygame.K_r:
                    player, ai, player_bullets, ai_bullets, ai_fire_timer = reset_game()
                    game_over = False
                    winner = ""

        if not game_over:
            # -------------------------
            # Controls: WASD = Move | Left Mouse Button = Fire
            # Player movement
            # -------------------------
            keys = pygame.key.get_pressed()

            dx = 0
            dy = 0

            if keys[pygame.K_a]:
                dx -= SHIP_SPEED
            if keys[pygame.K_d]:
                dx += SHIP_SPEED
            if keys[pygame.K_w]:
                dy -= SHIP_SPEED
            if keys[pygame.K_s]:
                dy += SHIP_SPEED

            player.move(dx, dy)

            # Player firing
            mouse_buttons = pygame.mouse.get_pressed()

            if player_fire_timer > 0:
                player_fire_timer -= 1

            if (
                mouse_buttons[0]
                and player_fire_timer == 0
                and len(player_bullets) < MAX_BULLETS
            ):
                player_bullets.append(create_bullet(player, 1))
                player_fire_timer = PLAYER_FIRE_COOLDOWN

            # -------------------------
            # Basic AI movement
            # -------------------------
            if ai.rect.centery < player.rect.centery:
                ai.move(0, SHIP_SPEED // 2)
            elif ai.rect.centery > player.rect.centery:
                ai.move(0, -(SHIP_SPEED // 2))

            # -------------------------
            # AI automatic firing
            # -------------------------
            ai_fire_timer += 1

            if ai_fire_timer >= 45 and len(ai_bullets) < MAX_BULLETS:
                ai_bullets.append(create_bullet(ai, -1))
                ai_fire_timer = 0

            # -------------------------
            # Move player bullets
            # -------------------------
            for bullet in player_bullets[:]:
                bullet.move()

                if bullet.is_off_screen():
                    player_bullets.remove(bullet)
                    continue

                if bullet.rect.colliderect(ai.rect):
                    ai.health -= 1
                    player_bullets.remove(bullet)

            # -------------------------
            # Move AI bullets
            # -------------------------
            for bullet in ai_bullets[:]:
                bullet.move()

                if bullet.is_off_screen():
                    ai_bullets.remove(bullet)
                    continue

                if bullet.rect.colliderect(player.rect):
                    player.health -= 1
                    ai_bullets.remove(bullet)

            # -------------------------
            # Check winner
            # -------------------------
            if ai.health <= 0:
                winner = "PLAYER WINS!"
                game_over = True

            elif player.health <= 0:
                winner = "AI WINS!"
                game_over = True

        # -------------------------
        # Drawing
        # -------------------------
        draw_background()

        pygame.draw.line(
            screen,
            WHITE,
            (WIDTH // 2, 80),
            (WIDTH // 2, HEIGHT),
            2,
        )

        player.draw()
        ai.draw()

        for bullet in player_bullets:
            bullet.draw()

        for bullet in ai_bullets:
            bullet.draw()

        draw_health_bar(
            40,
            40,
            player.health,
            GREEN,
            "PLAYER",
        )

        draw_health_bar(
            WIDTH - 340,
            40,
            ai.health,
            RED,
            "AI",
        )

        if game_over:
            draw_center_text(winner)

            restart_text = font.render(
                "Press R to restart or ESC to quit",
                True,
                WHITE,
            )

            screen.blit(
                restart_text,
                (
                    WIDTH // 2 - restart_text.get_width() // 2,
                    HEIGHT // 2 + 70,
                ),
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()