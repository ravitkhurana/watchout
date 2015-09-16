import pygame
import enum


class Color(enum.Enum):

    """
    Enumeration for common colors
    """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)


class Constants(object):

    """
    Class to hold constants used in game
    """
    GRAVITY = 1
    RESOLUTION = (640, 480)
    ROAD_Y = 400


class GameState(object):

    """
    Class to maintain current state of the game
    """

    def __init__(self):
        self.player = Player()
        self.obstacles = Obstacles()
        self.is_game_over = False
        self.score = 0

    def update(self):
        """
        This method updates current game state by updating obstacles, checking
        for collisions and incrementing the score. Set self.is_game_over if
        a collision is detected.
        """
        self.player.update()
        self.obstacles.update()
        self.check_collision()
        self.score += 1

    def check_collision(self):
        """
        This method checks if any of the obstacle has collided with the
        player. Sets self.is_game_over if a collision is detected.
        """
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

    """
    Class to maintain player's state.
    """

    def __init__(self):
        self.dimensions = None
        self.position = None
        self.in_jump = False
        self.velocity = [0, 0]

    def jump(self):
        """
        This method initiates a jump if player is not already in between a
        jump. Otherwise, it just updates player's position according to
        player's current velocity and value of Constants.GRAVITY.
        """
        if not self.in_jump:
            self.velocity = [0, 15]
            self.in_jump = True

    def update(self):
        """
        This method updates player's position if the player is already in
        motion.
        """
        if self.in_jump:
            t = 1
            distance = (self.velocity[1] * t) - (Constants.GRAVITY * (t ^ 2))
            self.velocity[1] -= Constants.GRAVITY * t
            self.position[1] -= distance
            if self.position[1] > Constants.ROAD_Y - self.dimensions[1]:
                self.position[1] = Constants.ROAD_Y - self.dimensions[1]
                self.in_jump = False
                self.velocity[1] = 0


class Obstacle(object):

    """
    Class to maintain an obstacle's state.
    """

    def __init__(self, dim, pos):
        self.dimensions = dim
        self.position = pos


class Obstacles(list):

    """
    Class to contain and manage all the obstacles
    """

    def __init__(self):
        super().__init__()

    def spawn_obstacle(self):
        """
        This method spawns new obstacles if required.
        """
        if len(self) == 0 or Constants.RESOLUTION[0] - self[-1].position[0] > 200:
            obstacle_dim = (20, 30)
            obstacle_pos = [Constants.RESOLUTION[0], Constants.ROAD_Y - obstacle_dim[1]]
            self.append(Obstacle(obstacle_dim, obstacle_pos))

    def update(self):
        """
        This method updates the position of all obstacles
        """
        self.spawn_obstacle()
        obstacles_to_be_removed = list()
        for obstacle in self:
            obstacle.position[0] -= 5
            if obstacle.position[0] + obstacle.dimensions[0] < 0:
                obstacles_to_be_removed.append(obstacle)
        for obstacle in obstacles_to_be_removed:
            self.remove(obstacle)


class Game(object):

    """
    The game class
    """

    def __init__(self):
        self.restart = True

    def start(self):
        """
        This method starts the game
        """
        while self.restart:
            self.restart = False
            self.main()

    def main(self):
        """
        Main method which runs the game.
        """
        pygame.init()
        # Initialize game state
        game_state = GameState()
        game_state.player.dimensions = (20, 50)
        game_state.player.position = [50, Constants.ROAD_Y - game_state.player.dimensions[1]]
        screen = pygame.display.set_mode(Constants.RESOLUTION)
        pygame.display.set_caption("Watch Out!")
        clock = pygame.time.Clock()
        done = False
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
                    if event.key == pygame.K_r:
                        self.restart = True
                        done = True
                    if event.key == pygame.K_ESCAPE:
                        done = True
            if not game_state.is_game_over:
                # * Perform calculations for movements, collision detection, etc.
                if player_jump:
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
    game = Game()
    game.start()
