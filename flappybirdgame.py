import pygame
import random
import sys
import os
from enum import Enum

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2

class FlappyBird:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700
    FPS = 60

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird- ASTHA")
        self.clock = pygame.time.Clock()
        self.load_assets()
        self.bird = None
        self.pipes = []
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_state = GameState.MENU
        self.last_pipe_time = 0
        self.pipe_frequency = 1500
        
        self.reset_game()
        self.game_loop()
    
    def load_assets(self):
        def load_image(filename, size=None):
            try:
                image = pygame.image.load(filename).convert_alpha()
                return pygame.transform.scale(image, size) if size else image
            except pygame.error:
                print(f"Warning: Could not load image {filename}, using placeholder")
                surface = pygame.Surface(size or (50, 50), pygame.SRCALPHA)
                pygame.draw.rect(surface, (255, 0, 0), surface.get_rect(), 1)
                if size is None and isinstance(surface, pygame.Surface):
                    return pygame.transform.scale(surface, (50, 50))
                return surface
        self.bird_img = load_image("bird.png", (50, 50))
        self.pipe_img = load_image("pipe.png", (100, 500))
        
        try:
            self.background_img = pygame.image.load("background.png").convert()
            self.background_img = pygame.transform.scale(self.background_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        except pygame.error:
            print("Warning: Could not load background image, using placeholder")
            self.background_img = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.background_img.fill((135, 206, 235)) 
        
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        
        def load_sound(filename):
            try:
                return pygame.mixer.Sound(filename)
            except pygame.error:
                print(f"Warning: Could not load sound {filename}")
                return None 
        
        self.flap_sound = load_sound("flap.wav")
        self.hit_sound = load_sound("hit.wav")
        self.point_sound = load_sound("point.wav")
    
    def reset_game(self):
        """Reset the game state for a new game"""
        self.bird = Bird(self.bird_img, self.flap_sound)
        self.pipes = [Pipe(self.pipe_img, self.SCREEN_WIDTH + i * 400) for i in range(2)]
        self.score = 0
        self.game_state = GameState.MENU
        self.last_pipe_time = pygame.time.get_ticks()
    
    def game_loop(self):
        """Main game loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_state == GameState.MENU:
                            self.game_state = GameState.PLAYING
                        elif self.game_state == GameState.PLAYING:
                            self.bird.flap()
                        elif self.game_state == GameState.GAME_OVER:
                            self.reset_game()
                            self.game_state = GameState.PLAYING
            
            self.screen.blit(self.background_img, (0, 0))
            
            if self.game_state == GameState.MENU:
                self.draw_menu()
                
            elif self.game_state == GameState.PLAYING:
               
                self.bird.update()
                self.update_pipes()
                self.bird.draw(self.screen)
                for pipe in self.pipes:
                    pipe.draw(self.screen)
                
                self.draw_score()
                if self.check_collisions() or self.bird.rect.bottom >= self.SCREEN_HEIGHT:
                    if self.hit_sound:
                        self.hit_sound.play()
                    self.game_over()
                
            elif self.game_state == GameState.GAME_OVER:
                self.bird.draw(self.screen)
                for pipe in self.pipes:
                    pipe.draw(self.screen)
                self.draw_score()
                
                self.draw_game_over()
            
            pygame.display.update()
            self.clock.tick(self.FPS)
        
        self.save_high_score()
        pygame.quit()
        sys.exit()
    
    def update_pipes(self):
        """Update pipe positions and spawn new pipes"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_time > self.pipe_frequency:
            self.pipes.append(Pipe(self.pipe_img, self.SCREEN_WIDTH))
            self.last_pipe_time = current_time
        
        pipes_to_remove = []
        for pipe in self.pipes:
            pipe.update()
            if not pipe.scored and pipe.x + pipe.width < self.bird.rect.left:
                self.score += 1
                pipe.scored = True
                if self.point_sound:
                    self.point_sound.play()
                if self.score % 5 == 0 and self.pipe_frequency > 800:
                    self.pipe_frequency -= 100
            
            if pipe.x + pipe.width < 0:
                pipes_to_remove.append(pipe)
        
        for pipe in pipes_to_remove:
            self.pipes.remove(pipe)
    
    def check_collisions(self):
        """Check if bird collides with any pipe"""
        for pipe in self.pipes:
            if pipe.collide(self.bird):
                return True
        return False
    
    def game_over(self):
        """Handle game over state"""
        self.game_state = GameState.GAME_OVER

        if self.score > self.high_score:
            self.high_score = self.score
    
    def draw_menu(self):
        """Draw the start menu"""
        title = self.large_font.render("FLAPPY BIRD", True, self.WHITE)
        instruction = self.font.render("Press SPACE to Start", True, self.WHITE)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, self.WHITE)
        
        self.bird.rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50)
        self.bird.draw(self.screen)

        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 4))
        instruction_rect = instruction.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))
        high_score_rect = high_score_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 100))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(instruction, instruction_rect)
        self.screen.blit(high_score_text, high_score_rect)
    
    def draw_game_over(self):
        """Draw the game over screen"""
        game_over_text = self.large_font.render("GAME OVER", True, self.WHITE)
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, self.WHITE)
        restart_text = self.font.render("Press SPACE to Restart", True, self.WHITE)
        
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  
        self.screen.blit(overlay, (0, 0))
        
        game_over_rect = game_over_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 3))
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        high_score_rect = high_score_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))
        restart_rect = restart_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 100))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(high_score_text, high_score_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def draw_score(self):
        """Draw current score during gameplay"""
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open("high_score.txt", "w") as file:
                file.write(str(self.high_score))
        except IOError:
            pass 


class Bird:
    def __init__(self, image, sound=None):
        self.image = image
        self.original_image = image 
        self.rect = self.image.get_rect(center=(100, FlappyBird.SCREEN_HEIGHT // 2))
        self.velocity = 0
        self.gravity = 0.5
        self.max_velocity = 10
        self.flap_sound = sound
        self.angle = 0
    
    def flap(self):
        self.velocity = -8
        if self.flap_sound:
            self.flap_sound.play()
    
    def update(self):
        self.velocity = min(self.velocity + self.gravity, self.max_velocity)
        self.rect.y += self.velocity
        
        self.angle = -self.velocity * 3  
        self.angle = max(-30, min(self.angle, 45))  
        
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        
       
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Pipe:
    def __init__(self, image, x):
        self.image = image
        self.x = x
        self.width = 80
        self.height = 500
        self.gap = 200 
        self.speed = 5
        self.scored = False  
        
       
        self.top = random.randint(100, FlappyBird.SCREEN_HEIGHT - self.gap - 100)
        self.bottom = self.top + self.gap
    
    def update(self):
        self.x -= self.speed
    
    def draw(self, screen):
        
        top_pipe = pygame.transform.flip(self.image, False, True)
        screen.blit(top_pipe, (self.x, self.top - self.height))
        screen.blit(self.image, (self.x, self.bottom))
    
    def collide(self, bird):
        top_pipe_rect = pygame.Rect(self.x, 0, self.width, self.top)
        bottom_pipe_rect = pygame.Rect(self.x, self.bottom, self.width, FlappyBird.SCREEN_HEIGHT - self.bottom)
        
        return bird.rect.colliderect(top_pipe_rect) or bird.rect.colliderect(bottom_pipe_rect)


if __name__ == "__main__":
    game = FlappyBird()