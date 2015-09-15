import pygame
import enum


class Color(enum.Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)


class Constants(object):
    GRAVITY = 1


class GameState(object):
    def __init__(self):
        self.player = Player()
        self.obstacles = list()
        self.prev_obstacle = None
        self.resolution = None
        self.road_y = None
        self.is_game_over = False
        self.score = 0

    def update(self):
        self.update_obstacles()
        self.check_collision()
        self.score += 1

    def spawn_obstacle(self):
        if self.prev_obstacle is None or self.resolution[0] - self.prev_obstacle.position[0] > 200:
            obstacle_dim = (20, 30)
            obstacle_pos = [self.resolution[0], self.road_y - obstacle_dim[1]]
            self.prev_obstacle = Obstacle(obstacle_dim, obstacle_pos)
            self.obstacles.append(self.prev_obstacle)

    def update_obstacles(self):
        self.spawn_obstacle()
        obstacles_to_be_removed = list()
        for obstacle in self.obstacles:
            obstacle.position[0] -= 5
            if obstacle.position[0] + obstacle.dimensions[0] < 0:
                obstacles_to_be_removed.append(obstacle)
        for obstacle in obstacles_to_be_removed:
            self.obstacles.remove(obstacle)

    def check_collision(self):
        x_collision = False
        y_collision = False
        player_x1 = self.player.position[0]
        player_x2 = player_x1 + self.player.dimensions[0]
        player_y1 = self.player.position[1]
        player_y2 = player_y1 + self.player.dimensions[1]
        for obstacle in self.obstacles:
            obstacle_x1 = obstacle.position[0]
            obstacle_x2 = obstacle_x1 + obstacle.dimensions[0]
            obstacle_y1 = obstacle.position[1]
            obstacle_y2 = obstacle_y1 + obstacle.dimensions[1]
            if obstacle_x1 > player_x2 or obstacle_x2 < player_x1:
                x_collision = False
            else:
                x_collision = True
            if obstacle_y1 > player_y2 or obstacle_y2 < player_y1:
                y_collision = False
            else:
                y_collision = True
            if x_collision and y_collision:
                self.is_game_over = True


class Player(object):
    def __init__(self):
        self.dimensions = None
        self.position = None
        self.in_jump = False
        self.position_before_jump = None
        self.speed = 0

    def jump(self):
        if not self.in_jump:
            self.speed = 15
            self.position_before_jump = (self.position[0], self.position[1])
            self.in_jump = True
        t = 1
        distance = (self.speed * t) - (Constants.GRAVITY * (t ^ 2))
        self.speed -= Constants.GRAVITY * t
        self.position[1] -= distance
        if self.position[1] > self.position_before_jump[1]:
            self.position[1] = self.position_before_jump[1]
            self.in_jump = False
            self.position_before_jump = None


class Obstacle(object):
    def __init__(self):
        self.dimensions = None
        self.position = None

    def __init__(self, dim, pos):
        self.dimensions = dim
        self.position = pos


def main():
    pygame.init()
    # Initialize game state
    game_state = GameState()
    game_state.resolution = (640, 480)
    game_state.road_y = 400
    game_state.player.dimensions = (20, 50)
    game_state.player.position = [50, game_state.road_y - game_state.player.dimensions[1]]
    screen = pygame.display.set_mode(game_state.resolution)
    assert isinstance(screen, pygame.Surface)
    pygame.display.set_caption("Watch Out!")
    done = False
    clock = pygame.time.Clock()
    # Game loop
    while not done:
        # * Process events in the events queue
        player_jump = False
        for event in pygame.event.get():
            assert isinstance(event, pygame.event.EventType)
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_jump = True
                if event.key == pygame.K_ESCAPE:
                    done = True
        if not game_state.is_game_over:
            # * Perform calculations for movements, collision detection, etc.
            if player_jump or game_state.player.in_jump:
                game_state.player.jump()
            game_state.update()
        # * Draw on screen
        screen.fill(Color.WHITE.value)
        font = pygame.font.SysFont('Calibri', 25, True, False)
        if not game_state.is_game_over:
            text = font.render("Watch out for the bluh-dy rocks!", True, Color.BLACK.value)
        else:
            text = font.render("Game Over Mayte!", True, Color.RED.value)
        screen.blit(text, ((screen.get_width() - text.get_width())/2, 50))
        score_text = font.render("Your score: " + game_state.score.__str__(), True, Color.BLUE.value)
        screen.blit(score_text, ((screen.get_width() - score_text.get_width())/2, score_text.get_height() + 60))
        # Draw player
        player_x, player_y = game_state.player.position
        player_w, player_h = game_state.player.dimensions
        pygame.draw.rect(screen, Color.BLUE.value, [player_x, player_y, player_w, player_h], 0)
        # Draw obstacles
        for obstacle in game_state.obstacles:
            obstacle_x, obstacle_y = obstacle.position
            obstacle_w, obstacle_h = obstacle.dimensions
            pygame.draw.rect(screen, Color.RED.value, [obstacle_x, obstacle_y, obstacle_w, obstacle_h], 0)
        # * Refresh screen
        pygame.display.flip()
        # * Set maximun FPS
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
