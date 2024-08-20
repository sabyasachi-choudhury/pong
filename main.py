# Imports
import random
import pygame

from pygame.locals import (K_UP, K_DOWN, K_ESCAPE, KEYDOWN)


# Creating the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((30, 150))
        self.surf.fill((0, 94, 255))
        self.rect = self.surf.get_rect(center=(15, s_height / 2))

    # Moving the player
    def player_move(self, press):
        player_speed = 1
        if press[K_UP]:
            self.rect.move_ip(0, -player_speed)
        if press[K_DOWN]:
            self.rect.move_ip(0, player_speed)

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > s_height:
            self.rect.bottom = s_height


# Creating Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((30, 150))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(s_width - 15, s_height / 2))


# Creating the ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.transform.smoothscale(pygame.image.load("ball_pink.svg").convert(), (30, 30))
        self.rect = self.surf.get_rect(center=(s_width / 2, s_height / 2))


# Initialise pygame
pygame.init()

# set vars
run = True
bg = (135, 250, 168)
s_width = 800
s_height = 600
ball_x = random.choice([-1, 1])
ball_y = random.choice([-1, 1])
enemy_y = 1
points = 0
bounce = pygame.mixer.Sound("bounce.wav")
game_speed = 800

# Making screen and Creating surfaces
screen = pygame.display.set_mode((s_width, s_height))
player = Player()
enemy = Enemy()
ball = Ball()

# Groups
all_sprites = pygame.sprite.Group()
all_sprites.add(enemy, player, ball)

# Playing background music
pygame.mixer.Sound("bg_music.wav").play(loops=-1)

# Increasing game speed
GameSpeedSet = pygame.USEREVENT + 1
pygame.time.set_timer(GameSpeedSet, 100)

# Main loop
while run:
    # get_pressed
    presses = pygame.key.get_pressed()

    # Detecting events and esc_press
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
        if event.type == GameSpeedSet:
            game_speed = game_speed + 2

    # Background
    screen.fill((0, 0, 0))

    # Ball's movement
    ball.rect.move_ip(ball_x, ball_y)

    if (ball.rect.top == 0) or (ball.rect.bottom == s_height):
        ball_y = -ball_y

    elif (ball.rect.top == enemy.rect.bottom and ball.rect.right > s_width - 30) or \
            (ball.rect.bottom == enemy.rect.top and ball.rect.right > s_width - 30):
        ball_y = -ball_y
        bounce.play()

    elif (ball.rect.top == player.rect.bottom and ball.rect.left < 30) or \
            (ball.rect.bottom == player.rect.top and ball.rect.left < 30):
        ball_y = -ball_y
        points = points + 1
        bounce.play()

    elif ball.rect.right == enemy.rect.left and ((enemy.rect.top < ball.rect.top < enemy.rect.bottom) or
                                                 (enemy.rect.top < ball.rect.bottom < enemy.rect.bottom)):
        ball_x = -ball_x
        bounce.play()

    elif (ball.rect.left == player.rect.right) and ((player.rect.top < ball.rect.top < player.rect.bottom) or
                                                    (player.rect.top < ball.rect.bottom < player.rect.bottom)):
        ball_x = -ball_x
        points = points + 1
        bounce.play()

    elif ball.rect.right < 0 or ball.rect.left > s_width:
        ball.kill()
        run = False

    # Player movement
    player.player_move(presses)

    # Enemy movement
    enemy.rect.center = (s_width - 15, ball.rect.y)

    # Rendering
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Displaying and frame rate regulation
    pygame.display.flip()

    pygame.time.Clock().tick(900)

# Ending
print("Total score:", points)
pygame.quit()