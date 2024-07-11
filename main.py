import pygame, sys, random
from pygame.math import Vector2
import file_handling
from file_handling import load_food_data
import os

pygame.init()

title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 30)

PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0), (0, 128, 128), (0, 0, 255), (75, 0, 130)]

cell_size = 30
number_of_cells = 25

OFFSET = 100


def home_screen():
    home_screen_font = pygame.font.Font(None, 60)
    scoreboard_font = pygame.font.Font(None, 36)

    while True:
        screen.fill(PURPLE)
        home_screen_text = home_screen_font.render("Press 's' to start the game", True, WHITE)
        screen_width, screen_height = screen.get_size()

        # Center the home screen text horizontally and position it at the top
        home_screen_text_rect = home_screen_text.get_rect()
        home_screen_text_rect.midtop = (screen_width // 2, OFFSET)
        screen.blit(home_screen_text, home_screen_text_rect)

        # Load high scores and display the top 5
        high_scores = file_handling.load_high_scores()
        high_scores.sort(reverse=True)
        top_scores = high_scores[:5]

        # Render the scoreboard
        scoreboard_text = scoreboard_font.render("Top Scores:", True, WHITE)
        scoreboard_rect = scoreboard_text.get_rect()
        scoreboard_rect.midtop = (screen_width // 2, OFFSET + 100)
        screen.blit(scoreboard_text, scoreboard_rect)

        for i, score in enumerate(top_scores, start=1):
            score_text = scoreboard_font.render(f"{i}. {score}", True, WHITE)
            score_rect = score_text.get_rect()
            score_rect.midtop = (screen_width // 2, scoreboard_rect.bottom + 40 * i)
            screen.blit(score_text, score_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    run_game()

def run_game():
    game.state = "RUNNING"
    while game.state == "RUNNING":
        for event in pygame.event.get():
            if event.type == SNAKE_UPDATE:
                game.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game.state == "STOPPED":
                    game.state = "RUNNING"
                if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                    game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                    game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                    game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                    game.snake.direction = Vector2(1, 0)

      # Draw
        screen.fill(PURPLE)
        pygame.draw.rect(screen, WHITE,
                       (OFFSET - 5, OFFSET - 5, cell_size * number_of_cells + 10, cell_size * number_of_cells + 10), 5)
        game.draw()
        pygame.display.update()
        clock.tick(60)

class GameObject:
    def __init__(self, position):
        self.position = position

    def draw(self):
        raise NotImplementedError("draw method must be implemented in subclass")

    def update(self):
        raise NotImplementedError("update method must be implemented in subclass")

class Food(GameObject):
    def __init__(self, snake_body, food_data):
        self.image_name = "apple.png"
        self.value = food_data.get(self.image_name, 5) # Assumes a default value of 5 if not found
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(os.path.join(script_dir, "Graphics", self.image_name))
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        super().__init__(self.generate_random_pos(snake_body))


    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(self.image, food_rect)

    def update(self):
        pass  

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position

class BonusFood(GameObject):
    def __init__(self, snake_body, food_position, food_data):
        self.image_name = "banana.png"
        self.value = food_data.get(self.image_name, 10) # Assumes a default value of 10 if not found
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(os.path.join(script_dir, "Graphics", self.image_name))
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        super().__init__(self.generate_random_pos(snake_body, food_position))

    def draw(self):
        bonus_food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(self.image, bonus_food_rect)

    def update(self):
        pass  

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body, food_position):
        position = self.generate_random_cell()
        while position in snake_body or position == food_position:
            position = self.generate_random_cell()
        return position

class StrawberryFood(Food):
  def __init__(self, snake_body, food_data):
      super().__init__(snake_body, food_data)
      self.image_name = "strawberry.png"  
      self.image = pygame.image.load(f"Graphics/{self.image_name}")
      self.image = pygame.transform.scale(self.image, (cell_size, cell_size))


class Snake(GameObject):
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.add_segment = False
        self.eat_sound = pygame.mixer.Sound("Sounds/eat.mp3")
        self.wall_hit_sound = pygame.mixer.Sound("Sounds/wall.mp3")
        super().__init__(self.body[0])  

    def draw(self):
        for i, segment in enumerate(self.body):
            segment_rect = (OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, COLORS[i % len(COLORS)], segment_rect)

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]
        self.position = self.body[0] 

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)

class Game:
    def __init__(self):
      self.food_data = file_handling.load_food_data()
      self.snake = Snake()
      self.food = Food(self.snake.body, self.food_data)
      self.bonus_food = BonusFood(self.snake.body, self.food.position, self.food_data)
      self.strawberry_food = StrawberryFood(self.snake.body, self.food_data)
      self.game_objects = [self.snake, self.food, self.bonus_food, self.strawberry_food]
      self.state = "RUNNING"
      self.score = 0
      self.games_played = 0

    def draw(self):
      for obj in self.game_objects:
          obj.draw()
      title_surface = title_font.render("BMET SUTTON COLDFIELD ARCADE", True, WHITE)
      score_surface = score_font.render(f"Score: {self.score}", True, WHITE)
      screen.blit(title_surface, (OFFSET - 5, 20))
      screen.blit(score_surface, (OFFSET - 5, OFFSET + cell_size * number_of_cells + 10))
  
    def update(self):
      if self.state == "RUNNING":
          for obj in self.game_objects:
              obj.update()
          self.check_collision_with_food()
          self.check_collision_with_bonus_food()
          self.check_collision_with_strawberry_food()  
          self.check_collision_with_edges()
          self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
           self.food.position = self.food.generate_random_pos(self.snake.body)
           self.snake.add_segment = True
           self.score += self.food.value 

    def check_collision_with_bonus_food(self):
        if self.snake.body[0] == self.bonus_food.position:
           self.bonus_food.position = self.bonus_food.generate_random_pos(self.snake.body, self.food.position)
           self.snake.add_segment = True
           self.score += self.bonus_food.value
           self.snake.eat_sound.play()

    def check_collision_with_strawberry_food(self):
        if self.snake.body[0] == self.strawberry_food.position:
           self.strawberry_food.position = self.strawberry_food.generate_random_pos(self.snake.body)
           self.snake.body.pop()
           self.score -= 2  # Deduct 2 pointss

    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.games_played += 1  # Increment the games_played counter
        self.update_high_scores()
        self.score = 0
        self.snake.wall_hit_sound.play()

    def update_high_scores(self):
        high_scores = file_handling.load_high_scores()
        high_scores.append(self.score)
        high_scores.sort(reverse=True)
        high_scores = high_scores[:5]  # Keep only the top 5 scores
        file_handling.save_high_scores(high_scores)

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

screen = pygame.display.set_mode((2 * OFFSET + cell_size * number_of_cells, 2 * OFFSET + cell_size * number_of_cells))

pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

game = Game()
food_surface = pygame.image.load("Graphics/apple.png")

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

def main():
    global game
    game = Game()
    home_screen()

if __name__ == "__main__":
    main()

while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)

    # Draw
    screen.fill(PURPLE)
    pygame.draw.rect(screen, WHITE,
                     (OFFSET - 5, OFFSET - 5, cell_size * number_of_cells + 10, cell_size * number_of_cells + 10), 5)
    game.draw()
    title_surface = title_font.render("BMET SUTTON COLDFIELD ARCADE", True, WHITE)
    score_surface = score_font.render(str(game.score), True, WHITE)
    screen.blit(title_surface, (OFFSET - 5, 20))
    screen.blit(score_surface, (OFFSET - 5, OFFSET + cell_size * number_of_cells + 10))
    pygame.display.update()
    clock.tick(60)

