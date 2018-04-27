import pygame
import world
import mobs

display_height = 1000
display_width = 1000
fps = 60

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class GameManager:
    player_rot = 0
    player_mov = 0
    crashed = False
    world_mgr = None
    player = None
    mob_mgr = None

    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption('CAVES!')
        self.clock = pygame.time.Clock()

    def draw(self):
        self.gameDisplay.fill(black)

        self.world_mgr.render(self.gameDisplay)

        # draw player
        pygame.draw.circle(self.gameDisplay, blue, list(map(int, self.player.pos)), 7, 0)

        self.mob_mgr.render(self.gameDisplay)

        pygame.display.update()
        self.clock.tick(fps)

    def take_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # x button is pressed
                self.crashed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print(self.player.pos, self.player.direction)
                if event.key == pygame.K_c:
                    self.world_mgr.add_cave(pygame.mouse.get_pos(), 50)

                if event.key == pygame.K_SPACE:
                    self.player.throw_bomb()

                # player movement
                if event.key == pygame.K_w:
                    self.player_mov += 1
                if event.key == pygame.K_s:
                    self.player_mov -= 1
                if event.key == pygame.K_a:
                    self.player_rot -= 5
                if event.key == pygame.K_d:
                    self.player_rot += 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player_mov -= 1
                if event.key == pygame.K_s:
                    self.player_mov += 1
                if event.key == pygame.K_a:
                    self.player_rot += 5
                if event.key == pygame.K_d:
                    self.player_rot -= 5

    def logic(self):
        # player movement
        if self.player_mov == 1:
            self.player.move()
        if self.player_mov == -1:
            self.player.move(-0.5)
        self.player.rotate(self.player_rot)

        self.mob_mgr.move_all()

    def mainloop(self):
        while not self.crashed:
            self.draw()
            self.take_input()
            self.logic()

    def start(self):
        self.world_mgr = world.WorldManager()
        self.player = mobs.Player([500, 500])
        self.mob_mgr = mobs.MobManager()

        self.mainloop()


game_mgr = GameManager()
