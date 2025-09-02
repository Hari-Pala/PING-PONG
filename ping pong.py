#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pong (Pygame) - 2 Player
Controls:
  Left paddle: W/S
  Right paddle: Up/Down
  P: pause  |  R: restart  |  Esc: quit
"""
import pygame, sys, random

W, H = 900, 520
PADDLE_W, PADDLE_H = 14, 100
BALL_SIZE = 14
PADDLE_SPEED = 6
BALL_SPEED = 6

WHITE = (235, 242, 255)
FG = (200, 210, 230)
BG = (12, 14, 28)
ACCENT = (138, 156, 255)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_W, PADDLE_H)
        self.speed = 0

    def move(self):
        self.rect.y += self.speed
        if self.rect.top < 20:
            self.rect.top = 20
        if self.rect.bottom > H - 20:
            self.rect.bottom = H - 20

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=6)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(W//2 - BALL_SIZE//2, H//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        self.vx = random.choice([-1, 1]) * BALL_SPEED
        self.vy = random.choice([-1, 1]) * BALL_SPEED * 0.75

    def reset(self, direction=None):
        self.rect.center = (W//2, H//2)
        self.vx = (direction if direction else random.choice([-1, 1])) * BALL_SPEED
        self.vy = random.choice([-1, 1]) * BALL_SPEED * 0.75

    def move(self, p1, p2, score):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        # top/bottom bounds
        if self.rect.top <= 20 or self.rect.bottom >= H-20:
            self.vy *= -1

        # paddle collisions
        if self.rect.colliderect(p1.rect) and self.vx < 0:
            offset = (self.rect.centery - p1.rect.centery) / (PADDLE_H/2)
            self.vx = abs(self.vx) * 1.05
            self.vy = BALL_SPEED * offset * 1.2
        if self.rect.colliderect(p2.rect) and self.vx > 0:
            offset = (self.rect.centery - p2.rect.centery) / (PADDLE_H/2)
            self.vx = -abs(self.vx) * 1.05
            self.vy = BALL_SPEED * offset * 1.2

        # scoring
        if self.rect.right < 0:
            score[1] += 1
            self.reset(direction=1)
        if self.rect.left > W:
            score[0] += 1
            self.reset(direction=-1)

    def draw(self, screen):
        pygame.draw.rect(screen, ACCENT, self.rect, border_radius=6)

def draw_court(screen):
    pygame.draw.rect(screen, (18,22,44), (0,0,W,H))
    # bounds
    pygame.draw.rect(screen, (28,32,58), (10,10,W-20,H-20), border_radius=14, width=2)
    # center dashed line
    for y in range(20, H-20, 22):
        pygame.draw.line(screen, (48,54,92), (W//2, y), (W//2, y+12), 3)

def announce_winner(screen, big_font, score):
    """Show who wins (or tie) before restarting."""
    if score[0] > score[1]:
        msg = "Player 1 Wins!"
        color = (120, 255, 160)
    elif score[1] > score[0]:
        msg = "Player 2 Wins!"
        color = (120, 255, 160)
    else:
        msg = "It's a Tie!"
        color = (255, 220, 120)

    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    title = big_font.render(msg, True, color)
    sub = big_font.render("Restarting...", True, FG)
    screen.blit(title, (W//2 - title.get_width()//2, H//2 - 40))
    screen.blit(sub, (W//2 - sub.get_width()//2, H//2 + 10))

    pygame.display.flip()
    pygame.time.wait(1800)  # wait ~1.8 seconds

def main():
    pygame.init()
    pygame.display.set_caption("Pong (2-Player)")
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 28)
    big = pygame.font.SysFont("consolas", 56, bold=True)
    label_font = pygame.font.SysFont("consolas", 24, bold=True)   # NEW

    p1 = Paddle(40, H//2 - PADDLE_H//2)
    p2 = Paddle(W-40-PADDLE_W, H//2 - PADDLE_H//2)
    ball = Ball()
    score = [0, 0]
    paused = False

    while True:
        dt = clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if e.key == pygame.K_p:
                    paused = not paused
                if e.key == pygame.K_r:
                    # <-- show winner first, then restart
                    announce_winner(screen, big, score)
                    score = [0, 0]
                    ball.reset()
                    p1.rect.centery = H//2
                    p2.rect.centery = H//2
                if e.key == pygame.K_w:
                    p1.speed = -PADDLE_SPEED
                if e.key == pygame.K_s:
                    p1.speed = PADDLE_SPEED
                if e.key == pygame.K_UP:
                    p2.speed = -PADDLE_SPEED
                if e.key == pygame.K_DOWN:
                    p2.speed = PADDLE_SPEED
            if e.type == pygame.KEYUP:
                if e.key in (pygame.K_w, pygame.K_s):
                    p1.speed = 0
                if e.key in (pygame.K_UP, pygame.K_DOWN):
                    p2.speed = 0

        if not paused:
            p1.move()
            p2.move()
            ball.move(p1, p2, score)

        # draw
        screen.fill(BG)
        draw_court(screen)
        p1.draw(screen)
        p2.draw(screen)
        ball.draw(screen)

        s_left = big.render(str(score[0]), True, FG)
        s_right = big.render(str(score[1]), True, FG)
        lbl1 = label_font.render("Player 1", True, (180, 190, 210))
        lbl2 = label_font.render("Player 2", True, (180, 190, 210))
        screen.blit(lbl1, (W//2 - 120 - lbl1.get_width()//2, 10))
        screen.blit(lbl2, (W//2 + 120 - lbl2.get_width()//2, 10))
        screen.blit(s_left, (W//2 - 80 - s_left.get_width(), 40))
        screen.blit(s_right, (W//2 + 80, 40))

        tips = font.render("W/S & ↑/↓ to move | P pause | R restart | Esc quit", True, (160,170,200))
        screen.blit(tips, (W//2 - tips.get_width()//2, H-32))

        pygame.display.flip()

if __name__ == "__main__":
    main()
