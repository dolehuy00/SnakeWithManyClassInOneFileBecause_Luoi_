
import pygame, random, time, sys

class InputBox:

    def __init__(self, x, y, w, h, text, font, text_color, color_inactive, color_active, border_radius):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.text = text
        self.txt_surface = font.render(text, True, text_color)
        self.active = False
        self.font = font
        self.colorChange = color_active
        self.text_color = text_color
        self.border_radius = border_radius
        self.defaultBorderColor = color_inactive

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.colorChange if self.active else self.defaultBorderColor
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if not len(self.text) == 7 and not event.unicode == ' ':
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.text_color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2, self.border_radius)

class Button:

    def __init__(self, text, font, width, height, pos):
        self.pressed = False
        self.font = font

        self.rect = pygame.Rect(pos, (width, height))
        self.color = '#B97A57'

        self.text = text
        self.text_surf = self.font.render(text, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, border_radius, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius = border_radius)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = '#C99B53'
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
        else:
            self.color = '#B97A57'
            self.pressed = False

class BXH:

    def __init__(self):
        pass

    @staticmethod
    def sort_bxh(list):
        for i in range(0, len(list)):
            list[i] = list[i].split(' ')
            list[i][1] = int(list[i][1])
        list = sorted(list, key=lambda x: x[1], reverse=True)
        list.pop(-1)
        for i in range(0, len(list)):
            list[i] = list[i][0] + ' ' + str(list[i][1])
        print(list)
        return list

    @staticmethod
    def write_bxh(link, name_player, score):
        list_data = ShowInformation.read_file(link)
        list_data.append(name_player + ' ' + str(score))
        list_data = BXH.sort_bxh(list_data)
        for i in range(0, len(list_data)):
            list_data[i] = list_data[i] + '\n'
        ShowInformation.write_file(link, list_data)

class ShowInformation:

    def __init__(self):
        pass

    @staticmethod
    def show_score_playing(pos, text_color, text_size, score, screen):
        font = pygame.font.SysFont('calibri', text_size)
        surf = font.render('Score: {0}'.format(score), True, text_color)
        rect = surf.get_rect()
        rect.midtop = pos
        screen.blit(surf, rect)

    @staticmethod
    def show_score_game_over(name, pos, text_color, text_size, score, screen):
        font = pygame.font.SysFont('calibri', text_size)
        surf = font.render('{1}: {0}'.format(score, name), True, text_color)
        rect = surf.get_rect()
        rect.midtop = pos
        screen.blit(surf, rect)

    @staticmethod
    def show_name_player(screen, name, pos, text_color, text_size):
        font = pygame.font.SysFont('calibri', text_size)
        surf = font.render(name, True, text_color)
        screen.blit(surf, pos)

    @staticmethod
    def read_file(link):
        with open(link, 'r') as f:
            data = [s.strip() for s in f.readlines()]
        f.close()
        return data

    @staticmethod
    def write_file(link, data):
        with open(link, 'w') as f:
            f.writelines(data)
        f.close()

class Food:

    def __init__(self, screen, image, width):
        self.food_pos = self.random_food()
        self.screen = screen
        self.image = image
        self.width = width

    @staticmethod
    def random_food():
        food_x = random.randrange(2, 124)
        food_y = random.randrange(4, 68)
        if food_x % 2 != 0:
            food_x += 1
        if food_y % 2 != 0:
            food_y += 1
        food_pos = [food_x * 10, food_y * 10]
        return food_pos

    def random(self):
        self.food_pos = self.random_food()

    def draw(self):
        self.screen.blit(self.image, pygame.Rect(self.food_pos[0], self.food_pos[1], self.width, self.width))

class Snake:

    def __init__(self, width, default_pos, default_direction, snake_body, image_head, image_body, screen):
        self.screen = screen
        self.image_body = image_body
        self.image_head = image_head
        self.snake_pos = default_pos
        self.snake_body = snake_body
        self.direction = default_direction
        self.change_to = default_direction
        self.width = width

    def change_direction(self, change_to):
        self.change_to = change_to
        if self.change_to == 'RIGHT' and not self.direction == 'LEFT' and not self.direction == 'RIGHT':
            self.direction = 'RIGHT'
        if self.change_to == 'LEFT' and not self.direction == 'RIGHT' and not self.direction == 'LEFT':
            self.direction = 'LEFT'
        if self.change_to == 'UP' and not self.direction == 'DOWN' and not self.direction == 'UP':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and not self.direction == 'UP' and not self.direction == 'DOWN':
            self.direction = 'DOWN'

        if self.direction == 'RIGHT':
            self.snake_pos[0] += self.width
        if self.direction == 'LEFT':
            self.snake_pos[0] -= self.width
        if self.direction == 'UP':
            self.snake_pos[1] -= self.width
        if self.direction == 'DOWN':
            self.snake_pos[1] += self.width

    def eating(self, food_pos):
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == food_pos[0] and self.snake_pos[1] == food_pos[1]:
            return True
        else:
            self.snake_body.pop()
            return False

    def draw(self):
        for pos in self.snake_body:
            self.screen.blit(self.image_body, pygame.Rect(pos[0], pos[1], self.width, self.width))
        self.screen.blit(self.image_head, pygame.Rect(self.snake_body[0][0], self.snake_body[0][1], self.width, self.width))

class Impediment:

    def __init__(self, screen):
        self.screen = screen
        self.rectangle_y = pygame.image.load('rectangle_y.png')
        self.rectangle_x = pygame.image.load('rectangle_x.png')
        self.long_rectangle = pygame.image.load('long_rectangle.png')

    def draw(self):
        self.screen.blit(self.rectangle_y, (621, 161))
        self.screen.blit(self.rectangle_x, (221, 241))
        self.screen.blit(self.rectangle_x, (221, 401))
        self.screen.blit(self.long_rectangle, (701, 301))
        self.screen.blit(self.long_rectangle, (701, 381))

    def draw_warning(self):
        pygame.draw.rect(self.screen, red, (621, 161, 58, 398), 1)
        pygame.draw.rect(self.screen, red, (221, 221, 398, 58), 1)
        pygame.draw.rect(self.screen, red, (221, 401, 398, 58), 1)
        pygame.draw.rect(self.screen, red, (701, 301, 298, 18), 1)
        pygame.draw.rect(self.screen, red, (701, 381, 298, 18), 1)

class GamePause:

    def __init__(self, screen):
        self.screen = screen
        self.continue_ = False
        self.home = False

        bnt_font = pygame.font.Font(None, 30)
        self.button_exit = Button('Exit', bnt_font, 250, 45, (350, 340))
        self.button_home = Button('Home', bnt_font, 250, 45, (680, 340))
        self.button_continue = Button('Continue', bnt_font, 250, 50, (515, 420))

        text_view_font = pygame.font.SysFont('calibri', 25, True)
        text_view = text_view_font.render('Go home will not save score!', True, black)

        self.pause_surface = pygame.Surface((710, 400))
        self.pause_surface.blit(pygame.image.load('gamePauseImg.png'), (0, 0))
        self.pause_surface.blit(text_view, (200,160))

    def continue_game(self):
        return self.continue_

    def not_continue(self):
        self.continue_ = False

    def go_home(self):
        return self.home

    def not_go_home(self):
        self.home = False

    def game_pause(self):
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.blit(self.pause_surface, (285, 150))

        self.button_exit.draw(10, self.screen)
        self.button_continue.draw(10, self.screen)
        self.button_home.draw(10, self.screen)
        if self.button_continue.pressed:
            self.continue_ = True
        if self.button_exit.pressed:
            sys.exit()
        if self.button_home.pressed:
            self.home = True
        pygame.display.update()

class GameOver:

    def __init__(self, screen):
        self.screen = screen
        self.name_player = ''
        self.score = 0
        self.restart = False
        self.home = False

        self.game_over_surface = pygame.image.load('gameOverImg.png')

        bnt_font = pygame.font.Font(None, 30)
        self.button_exit = Button('Exit', bnt_font, 250, 40, (350, 380))
        self.button_home = Button('Home', bnt_font, 250, 40, (680, 380))
        self.button_restart = Button('Restart', bnt_font, 250, 50, (515, 450))

    def update_bxh(self):
        BXH().write_bxh('top5.txt', self.name_player, self.score)

    def set_name_player(self, name):
        self.name_player = name

    def set_score(self, score):
        self.score = score

    def not_restart(self):
        self.restart = False

    def restart_game(self):
        return self.restart

    def not_go_home(self):
        self.home = False

    def go_home(self):
        return self.home

    def game_over(self):
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.blit(self.game_over_surface, (285, 150))

        self.button_exit.draw(10, self.screen)
        self.button_restart.draw(10, self.screen)
        self.button_home.draw(10, self.screen)
        if self.button_restart.pressed:
            self.restart = True
        if self.button_exit.pressed:
            sys.exit()
        if self.button_home.pressed:
            self.home = True

        ShowInformation.show_score_game_over(self.name_player, (620, 320), black, 40, self.score, self.screen)

        pygame.display.update()

class GameHome:

    def __init__(self, screen):
        self.screen = screen
        self.name_player = 'Player'
        self.main = False

        font_title = pygame.font.SysFont('broadway', 100)
        self.surf_title = font_title.render('SNAKE', True, black)
        self.rect_title = self.surf_title.get_rect()
        self.rect_title.midtop = (640, 100)

        self.top_score_surface = pygame.Surface((300, 210))
        self.top_score_surface.fill(white)
        self.data = ShowInformation.read_file('top5.txt')
        self.font_bxh = pygame.font.SysFont('calibri', 27, True)

        font_text_field_enter_name = pygame.font.SysFont('calibri', 25, True)
        self.text_field_enter_name = font_text_field_enter_name.render('Enter your name!', True, black)
        self.input_name = InputBox(540, 470, 200, 40, self.name_player, pygame.font.SysFont('calibri', 35),
                                   "black", "red", "blue", 5)

        self.button_start = Button('Start', pygame.font.Font(None, 30), 300, 50, (490, 530))
        self.button_exit = Button('Exit', pygame.font.Font(None, 30), 300, 40, (490, 600))

    def update_bxh(self):
        self.top_score_surface.fill(white)
        self.data = ShowInformation.read_file('top5.txt')

    def set_name_player(self, name):
        self.name_player = name

    def get_name_player(self):
        return self.name_player

    def not_to_main(self):
        self.main = False

    def to_main(self):
        return self.main

    def game_home(self):
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if len(self.input_name.text) < 8:
                self.input_name.handle_event(event)

        self.screen.fill(white)

        self.screen.blit(self.surf_title, self.rect_title)

        for i in range(0, 5):
            surf = self.font_bxh.render('Top ' + str(i + 1) + ': ', True, black)
            self.top_score_surface.blit(surf, (10, 10 + i * 40))

            surf = self.font_bxh.render((self.data[i].split(' '))[0], True, black)
            self.top_score_surface.blit(surf, (90, 10 + i * 40))

            surf = self.font_bxh.render((self.data[i].split(' '))[1], True, black)
            self.top_score_surface.blit(surf, (250, 10 + i * 40))
        pygame.draw.rect(self.top_score_surface, red, (1, 1, 299, 209), 2, 15)
        self.screen.blit(self.top_score_surface, (490, 220))

        self.screen.blit(self.text_field_enter_name, (550, 440))
        self.input_name.draw(self.screen)

        self.button_start.draw(10, self.screen)
        self.button_exit.draw(10, self.screen)

        if self.button_start.pressed:
            self.name_player = self.input_name.text
            self.main = True
        if self.button_exit.pressed:
            sys.exit()

        pygame.display.update()

class GameMain:

    def __init__(self, screen):
        self.screen = screen
        self.name_player = ''
        self.score = 0
        self.width_snake = 20
        self.over = False
        self.pause = False
        self.speed = 100

        self.button_pause = Button('Pause', pygame.font.Font(None, 20), 100, 25, (590, 3))

        self.image_body = pygame.transform.scale(pygame.image.load('body.png'), (self.width_snake, self.width_snake))
        self.image_head = pygame.transform.scale(pygame.image.load('head.png'), (self.width_snake, self.width_snake))
        self.image_food = pygame.transform.scale(pygame.image.load('food.png'), (self.width_snake, self.width_snake))
        self.snake_pos = [100, 80]
        self.snake_body = [[100, 80], [80, 80]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.snake = Snake(self.width_snake, self.snake_pos, self.direction, self.snake_body, self.image_head,
                           self.image_body, self.screen)
        self.food = Food(self.screen, self.image_food, self.width_snake)

        self.imp = Impediment(self.screen)

    def set_name_player(self, name):
        self.name_player = name

    def get_name_player(self):
        return self.name_player

    def get_score(self):
        return self.score

    def set_new(self):
        self.score = 0
        self.speed = 100
        self.snake_pos = [100, 80]
        self.snake_body = [[100, 80], [80, 80]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.snake = Snake(self.width_snake, self.snake_pos, self.direction, self.snake_body, self.image_head, self.image_body,
                           self.screen)

    def not_game_over(self):
        self.over = False

    def game_over(self):
        return self.over

    def not_pause(self):
        self.pause = False

    def pause_game(self):
        return self.pause

    def game_main(self):
        speed = self.speed - self.score
        pygame.time.delay(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    self.change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.evet.Event(pygame.QUIT))

        self.snake.change_direction(self.change_to)

        if self.snake.eating(self.food.food_pos):
            self.score += 1
            self.food.random()

        if self.food.food_pos in self.snake_body:
            self.food.random()

        self.screen.fill(brown)

        if self.score > 2:
            if self.score < 5:
                self.imp.draw_warning()
            if  200 < self.food.food_pos[0] < 620 and 220 < self.food.food_pos[1] < 300:
                self.food.random()
            if  200 < self.food.food_pos[0] < 620 and 380 < self.food.food_pos[1] < 460:
                self.food.random()
            if  600 < self.food.food_pos[0] < 680 and 140 < self.food.food_pos[1] < 560:
                self.food.random()
            if  680 < self.food.food_pos[0] < 1000 and 280 < self.food.food_pos[1] < 320:
                self.food.random()
            if  680 < self.food.food_pos[0] < 1000 and 360 < self.food.food_pos[1] < 400:
                self.food.random()

        if self.snake.snake_pos[0] > 1250 or self.snake.snake_pos[0] < 10:
            self.over = True
        if self.snake.snake_pos[1] > 680 or self.snake.snake_pos[1] < 30:
            self.over = True

        if self.score > 4:
            self.imp.draw()
            if  200 < self.snake.snake_pos[0] < 620 and 220 < self.snake.snake_pos[1] < 300:
                self.over = True
            if  200 < self.snake.snake_pos[0] < 620 and 380 < self.snake.snake_pos[1] < 460:
                self.over = True
            if  600 < self.snake.snake_pos[0] < 680 and 140 < self.snake.snake_pos[1] < 560:
                self.over = True
            if  680 < self.snake.snake_pos[0] < 1000 and 280 < self.snake.snake_pos[1] < 320:
                self.over = True
            if  680 < self.snake.snake_pos[0] < 1000 and 360 < self.snake.snake_pos[1] < 400:
                self.over = True

        self.snake.draw()

        self.food.draw()

        pygame.draw.rect(self.screen, black, (10, 30, 1260, 680), 1)

        ShowInformation.show_score_playing((70, 10), black, 20, self.score, self.screen)

        ShowInformation.show_name_player(self.screen, self.name_player, (1200, 10), black, 20)

        self.button_pause.draw(2, self.screen)
        if self.button_pause.pressed:
            self.pause = True

        pygame.display.update()
        pygame.time.Clock().tick(60)

pygame.init()

game_surface = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Snake')

red = pygame.Color(255, 0, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(222, 170, 115)

def run():
    home = GameHome(game_surface)
    main = GameMain(game_surface)
    pause = GamePause(game_surface)
    game_over = GameOver(game_surface)

    display = 'home'
    while True:
        if display == 'home':
            home.game_home()
            if home.to_main():
                display = 'main'
                main.set_name_player(home.get_name_player())
                main.set_new()
                home.not_to_main()

        if display == 'main':
            main.game_main()
            if main.game_over():
                display = 'over'
                game_over.set_name_player(main.get_name_player())
                game_over.set_score(main.get_score())
                game_over.update_bxh()
                main.not_game_over()
            if main.pause_game():
                display = 'pause'
                main.not_pause()

        if display == 'pause':
            pause.game_pause()
            if pause.go_home():
                display = 'home'
                pause.not_go_home()
            if pause.continue_game():
                display = 'main'
                pause.not_continue()

        if display == 'over':
            game_over.game_over()
            if game_over.restart_game():
                display = 'main'
                main.set_new()
                game_over.not_restart()
            if game_over.go_home():
                display = 'home'
                home.update_bxh()
                game_over.not_go_home()

run()