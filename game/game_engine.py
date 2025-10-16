import pygame
from .paddle import Paddle
from .ball import Ball

# Initialize mixer for sounds
pygame.mixer.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Create player, AI, and ball
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        # Scores and font
        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.winning_score = 3  # default Best of 3

        # Load sound effects
        self.sound_paddle = pygame.mixer.Sound("sounds/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("sounds/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("sounds/score.wav")

        # Optional volume
        self.sound_paddle.set_volume(0.5)
        self.sound_wall.set_volume(0.5)
        self.sound_score.set_volume(0.7)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move the ball
        self.ball.move()

        # Paddle collisions
        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.x = self.player.x + self.player.width
            self.ball.velocity_x *= -1
            self.sound_paddle.play()
        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.x = self.ai.x - self.ball.width
            self.ball.velocity_x *= -1
            self.sound_paddle.play()

        # Wall collisions (top/bottom)
        if self.ball.y <= 0 or self.ball.y + self.ball.height >= self.height:
            self.ball.velocity_y *= -1
            self.sound_wall.play()

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
            self.sound_score.play()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()
            self.sound_score.play()

        # AI movement
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        # Draw ball
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        # Center line
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    def check_game_over(self, screen):
        winner = None
        if self.player_score >= self.winning_score:
            winner = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            winner = "AI Wins!"

        if winner:
            # Full black Game Over screen
            screen.fill(BLACK)
            title = self.font.render(winner, True, WHITE)
            screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 3)))

            # Replay options
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, opt in enumerate(options):
                text = self.font.render(opt, True, WHITE)
                screen.blit(text, text.get_rect(center=(self.width // 2, self.height // 2 + i * 40)))

            pygame.display.flip()

            # Wait for input
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                        elif event.key == pygame.K_3:
                            self.winning_score = 3
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.winning_score = 5
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.winning_score = 7
                            waiting = False

                pygame.time.Clock().tick(30)

            # Reset game
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()
            pygame.time.delay(500)
