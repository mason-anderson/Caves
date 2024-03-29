import pygame
import world
import mobs
import gui
import extra_math as math
from random import randint

display_height = 700
display_width = 1000
fps = 45

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (72, 72, 72)

pygame.init()


class GameManager:
    player_rot = 0
    player_mov = 0
    screen_x = 0
    screen_y = 0
    crashed = False

    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption('CAVES!')
        self.clock = pygame.time.Clock()

    def draw(self):
        self.gameDisplay.fill(black)

        world_mgr.render(self.gameDisplay)

        # draw player
        pygame.draw.circle(self.gameDisplay, blue,
                           [int(player.pos[0] + self.screen_x), int(player.pos[1] + self.screen_y)], 7, 0)

        new_pos = [500, 500]
        new_pos[0] += math.cos(math.radians(player.direction)) * 12
        new_pos[1] += math.sin(math.radians(player.direction)) * 12

        pygame.draw.line(self.gameDisplay, blue, [500, 500], new_pos)

        mob_mgr.render(self.gameDisplay)

        self.menu()

        pygame.display.update()
        self.clock.tick(fps)

    def take_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # x button is pressed
                self.crashed = True
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    mob_mgr.new_mob(world.Chest, [pygame.mouse.get_pos()[0] - self.screen_x,
                                                  pygame.mouse.get_pos()[1] - self.screen_y], {"bombs": 5})
                    # print(player.bombs)
                if event.key == pygame.K_c:
                    mob_mgr.new_mob(mobs.Enemy, [pygame.mouse.get_pos()[0] - self.screen_x,
                                                 pygame.mouse.get_pos()[1] - self.screen_y])
                if event.key == pygame.K_m:
                    world_mgr.make_cave(
                        [pygame.mouse.get_pos()[0] - self.screen_x, pygame.mouse.get_pos()[1] - self.screen_y], 25, 40)

                if event.key == pygame.K_SPACE:
                    player.shoot()
                if event.key == pygame.K_e:
                    player.throw_bomb()

                # moving
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
            player.move()
        if self.player_mov == -1:
            player.move(-0.5)
        player.rotate(self.player_rot * 2)

        if player.health < 1:
            self.crashed = True
            player.heath = 100

        if not randint(0, 120):
            world_mgr.extend_caves(player.pos)

        mob_mgr.move_all()

        self.screen_x = 500 - player.pos[0]
        self.screen_y = 500 - player.pos[1]

    def mainloop(self):
        while not self.crashed:
            self.draw()
            self.take_input()
            self.logic()

    def menu(self):
        pygame.draw.rect(self.gameDisplay, grey, (800, 0, 200, 200))
        gui.center_text(self.gameDisplay, "Thou hath " + str(player.bombs) + " bombs", 900, 10, 15, white)
        gui.center_text(self.gameDisplay, "Thou hath " + str(player.points) + " points", 900, 30, 15, white)

        # Health Bar
        pygame.draw.rect(self.gameDisplay, red, (800, 190, 200, 10))
        pygame.draw.rect(self.gameDisplay, green, (800, 190, int(player.health) * 2, 10))
        gui.center_text(self.gameDisplay, "Health Bar: " + str(player.health) + "%", 900, 190, 15, black)


game_mgr = GameManager()
world_mgr = None
player = None
mob_mgr = None


def start():
    global world_mgr
    global player
    global mob_mgr

    game_mgr.crashed = False

    world_mgr = None
    player = None
    mob_mgr = None

    world_mgr = world.WorldManager()
    player = mobs.Player([500, 500])
    mob_mgr = mobs.MobManager()

    mob_mgr.enemies = []
    mob_mgr.items = []

    world_mgr.generate_world()

    game_mgr.mainloop()
