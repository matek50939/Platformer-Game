import pygame
import random
import asyncio

pygame.init()

class Platform:
    def __init__(self, x, y, width=100, height=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.scored = False

platforms = []
score = 0

def resolve_platform_collisions(rect, vy):
    global score
    for plat in platforms:
        if rect.colliderect(plat.rect):
            if vy > 0 and rect.bottom - vy <= plat.rect.top:
                rect.bottom = plat.rect.top
                if not plat.scored:
                    score += 1
                    plat.scored = True
                return 0, True
            if vy < 0 and rect.top - vy >= plat.rect.bottom:
                rect.top = plat.rect.bottom
                return 0, False
    return vy, False

async def main():
    global score
    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jump Cube")

    BLUE = (100, 150, 255)
    GREEN = (0, 255, 0)
    BROWN = (139, 69, 19)
    WHITE = (255, 255, 255)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    for i in range(8):
        x = random.randint(0, WIDTH - 100)
        y = HEIGHT - 50 - i * 100
        platforms.append(Platform(x, y))

    spawn_platform = random.choice(platforms)

    player_size = 30
    player_x = spawn_platform.rect.x + spawn_platform.rect.width // 2 - player_size // 2
    player_y = spawn_platform.rect.y - player_size
    player_vel_y = 0
    gravity = 0.5
    jump_strength = -12
    can_jump = True

    running = True

    while running:
        clock.tick(60)
        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= 5
        if keys[pygame.K_d]:
            player_x += 5
        if keys[pygame.K_w] and can_jump:
            player_vel_y = jump_strength
            can_jump = False

        if player_x < -player_size:
            player_x = WIDTH
        if player_x > WIDTH:
            player_x = -player_size

        player_vel_y += gravity
        player_y += player_vel_y
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        player_vel_y, landed = resolve_platform_collisions(player_rect, player_vel_y)
        if landed:
            can_jump = True
        else:
            can_jump = False

        player_x = player_rect.x
        player_y = player_rect.y

        if player_y < HEIGHT // 2:
            offset = HEIGHT // 2 - player_y
            player_y = HEIGHT // 2
            player_rect.y = player_y
            for plat in platforms:
                plat.rect.y += offset

        platforms[:] = [p for p in platforms if p.rect.y <= HEIGHT]

        while len(platforms) < 8:
            last_platform = min(platforms, key=lambda p: p.rect.y)
            x = random.randint(max(0, last_platform.rect.x - 150),
                               min(WIDTH - 100, last_platform.rect.x + 150))
            y = last_platform.rect.y - random.randint(80, 130)
            platforms.append(Platform(x, y))

        for plat in platforms:
            pygame.draw.rect(screen, BROWN, plat.rect)

        pygame.draw.rect(screen, GREEN, player_rect)

        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        if player_y > HEIGHT:
            running = False

        pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
