import pygame
import os
import sys
import random

pygame.init()

size = width, height = 1200, 700
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


fon_game = load_image('47777.jpg')
player_image = load_image('Jump.png')
button_image = load_image('buttonblue.png')
button_rect = button_image.get_rect(center=(width // 2, height // 2))
tile_width = tile_height = 50

player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
level = 0


class Fon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(tiles_group, all_sprites)
        self.image = fon_game
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(player_image, 8, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move_player(self, napr):
        self.rect.x = self.rect.x + napr[0] * tile_width
        self.rect.y = self.rect.y + napr[1] * tile_height

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, t):
        super().__init__(button_group, all_sprites)
        self.image = button_image
        self.rect = self.image.get_rect().move(
            x, y)
        self.rect.x = x
        self.rect.y = y
        self.type = t
        self.image = pygame.transform.scale(self.image, (200, 100))

    def check_on(self, pos):
        print(pos, self.rect)
        if self.rect.collidepoint(pos):
            print(123)
            return self.type
        return 2


class ClickTheColor:
    def __init__(self, fon=None):
        """Инициализация игры 'Нажми на цвет'."""
        pygame.init()

        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Нажми на цвет")

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.fon = fon
        self.colors = [self.red, self.green, self.blue]

        self.target_color = random.choice(self.colors)
        self.target_rect = self.create_target()

        self.score = 0
        self.font = pygame.font.Font(None, 40)
        self.start_time = pygame.time.get_ticks()
        self.game_duration = 10000  # 10 seconds
        self.game_over = False

    def create_target(self):
        """Создает прямоугольник-цель со случайным цветом и положением."""
        x = random.randint(100, self.width - 100)
        y = random.randint(100, self.height - 100)
        size = 50
        return pygame.Rect(x, y, size, size)

    def draw_target(self):
        """Рисует прямоугольник-цель на экране."""
        pygame.draw.rect(self.screen, self.target_color, self.target_rect)

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_score(self):
        """Отображает счет."""
        self.draw_text(f"Счет: {self.score}", 100, 30, self.black)

    def draw_timer(self):
        """Отображает таймер."""
        time_left = max(0, (self.game_duration - (pygame.time.get_ticks() - self.start_time)) / 1000)
        self.draw_text(f"Время: {time_left:.1f}", self.width - 100, 30, self.black)

    def handle_click(self, mouse_pos):
        """Обрабатывает клик мыши."""
        if self.game_over:
            return
        if self.target_rect.collidepoint(mouse_pos):
            self.score += 1
            self.target_color = random.choice(self.colors)
            self.target_rect = self.create_target()

    def check_game_over(self):
        """Проверяет, закончилась ли игра."""
        if pygame.time.get_ticks() - self.start_time > self.game_duration:
            self.game_over = True

    def draw_message(self):
        """Выводит сообщение о завершении игры."""
        if self.game_over:
            self.draw_text(f"Игра окончена! Ваш счет: {self.score}", self.width // 2, self.height // 2, self.black)

    def run(self):
        """Основной игровой цикл."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.fon is not None:
                        pygame.display.set_mode((self.fon.get_width(), self.fon.get_height()))
                        pygame.display.flip()
                    return 2
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_click(mouse_pos)
            self.check_game_over()
            self.screen.fill(self.white)
            self.draw_target()
            self.draw_score()
            self.draw_timer()
            if self.game_over:
                self.draw_message()
            pygame.display.flip()

        pygame.quit()
        sys.exit()


class TicTacToe:
    def __init__(self, fon=None):
        """Инициализация игры Крестики-нолики."""
        pygame.init()

        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Крестики-нолики")

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.grid_color = (100, 100, 100)
        self.x_color = (255, 0, 0)
        self.o_color = (0, 0, 255)

        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.cell_size = self.width // 3
        self.fon = fon
        self.restart_delay = 3000
        self.game_start_time = None

    def draw_grid(self):
        """Рисует сетку игрового поля."""
        for i in range(1, 3):
            pygame.draw.line(self.screen, self.grid_color, (0, i * self.cell_size), (self.width, i * self.cell_size), 3)
            pygame.draw.line(self.screen, self.grid_color, (i * self.cell_size, 0), (i * self.cell_size, self.height),
                             3)

    def draw_pieces(self):
        """Рисует крестики и нолики на игровом поле."""
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "X":
                    x_center = col * self.cell_size + self.cell_size // 2
                    y_center = row * self.cell_size + self.cell_size // 2
                    pygame.draw.line(self.screen, self.x_color, (x_center - 30, y_center - 30),
                                     (x_center + 30, y_center + 30), 5)
                    pygame.draw.line(self.screen, self.x_color, (x_center + 30, y_center - 30),
                                     (x_center - 30, y_center + 30), 5)
                elif self.board[row][col] == "O":
                    x_center = col * self.cell_size + self.cell_size // 2
                    y_center = row * self.cell_size + self.cell_size // 2
                    pygame.draw.circle(self.screen, self.o_color, (x_center, y_center), 30, 5)

    def handle_human_click(self, mouse_pos):
        """Обрабатывает клик мыши игрока."""
        if self.game_over:
            return
        col = mouse_pos[0] // self.cell_size
        row = mouse_pos[1] // self.cell_size
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            if self.check_winner():
                self.game_over = True
                self.winner = self.current_player
            elif self.check_tie():
                self.game_over = True
                self.winner = "Tie"
            else:
                self.current_player = "O"

    def handle_computer_move(self):
        """Выбирает ход компьютера."""
        if self.game_over:
            return

        # Простой алгоритм компьютера: выбрать случайную пустую клетку
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "":
                    empty_cells.append((row, col))
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = self.current_player

            if self.check_winner():
                self.game_over = True
                self.winner = self.current_player
            elif self.check_tie():
                self.game_over = True
                self.winner = "Tie"
            else:
                self.current_player = "X"

    def check_winner(self):
        """Проверяет, есть ли победитель."""
        # Проверка строк
        for row in self.board:
            if row[0] == row[1] == row[2] != "":
                return True
        # Проверка столбцов
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return True
        # Проверка диагоналей
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    def check_tie(self):
        """Проверяет, есть ли ничья."""
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True

    def draw_message(self):
        """Выводит сообщение о победе или ничьей."""
        font = pygame.font.Font(None, 50)
        if self.winner == "Tie":
            text = font.render("Ничья!", True, self.black)
        elif self.winner == "X":
            text = font.render("Вы победили!", True, self.black)
        else:
            text = font.render("Компьютер победил!", True, self.black)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)

    def reset_game(self):
        """Сброс игры для нового раунда"""
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.game_start_time = None

    def run(self):
        """Основной игровой цикл."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.current_player == "X":
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_human_click(mouse_pos)

            self.screen.fill(self.white)
            self.draw_grid()
            self.draw_pieces()
            if self.game_over:
                self.draw_message()
                if self.winner == "X":
                    if not self.game_start_time:
                        self.game_start_time = pygame.time.get_ticks()
                    elif pygame.time.get_ticks() - self.game_start_time > self.restart_delay:
                        return 2
                elif self.winner == "O" or self.winner == "Tie":
                    self.reset_game()
            elif self.current_player == "O":
                self.handle_computer_move()

            pygame.display.flip()

        if self.winner == "X":
            if self.fon is not None:
                pygame.display.set_mode((self.fon.get_width(), self.fon.get_height()))
                pygame.display.flip()
        pygame.quit()
        sys.exit()


class Breakout:
    def __init__(self, fon=None):
        """Инициализация игры Арканоид."""
        pygame.init()

        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Арканоид")

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (150, 150, 150)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.fon = fon
        self.paddle_width = 80
        self.paddle_height = 15
        self.paddle_x = (self.width - self.paddle_width) // 2
        self.paddle_y = self.height - self.paddle_height - 20
        self.paddle_speed = 2

        self.ball_size = 15
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = random.choice([-4, 4]) / 15
        self.ball_dy = -4 / 15

        self.block_width = 50
        self.block_height = 20
        self.blocks = self.create_blocks()

        self.game_over = False
        self.score = 0
        self.font = pygame.font.Font(None, 40)
        self.lives = 3

    def create_blocks(self):
        """Создает блоки для разрушения."""
        blocks = []
        colors = [self.red, self.green, self.blue]
        for row in range(5):
            for col in range(self.width // self.block_width):
                block_x = col * self.block_width
                block_y = row * self.block_height + 50
                block_rect = pygame.Rect(block_x, block_y, self.block_width, self.block_height)
                blocks.append((block_rect, random.choice(colors)))

        return blocks

    def draw_paddle(self):
        """Рисует платформу."""
        paddle_rect = pygame.Rect(self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height)
        pygame.draw.rect(self.screen, self.blue, paddle_rect)

    def draw_ball(self):
        """Рисует мяч."""
        pygame.draw.circle(self.screen, self.white, (self.ball_x, self.ball_y), self.ball_size)

    def draw_blocks(self):
        """Рисует все блоки."""
        for block_rect, color in self.blocks:
            pygame.draw.rect(self.screen, color, block_rect)

    def move_paddle(self, keys):
        """Двигает платформу."""
        if keys[pygame.K_LEFT] and self.paddle_x > 0:
            self.paddle_x -= self.paddle_speed
        if keys[pygame.K_RIGHT] and self.paddle_x < self.width - self.paddle_width:
            self.paddle_x += self.paddle_speed

    def move_ball(self):
        """Двигает мяч и обрабатывает столкновения."""
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Столкновение со стенами
        if self.ball_x - self.ball_size <= 0 or self.ball_x + self.ball_size >= self.width:
            self.ball_dx *= -1
        if self.ball_y - self.ball_size <= 0:
            self.ball_dy *= -1

        if self.ball_y + self.ball_size >= self.height:
            self.lives -= 1
            if self.lives == 0:
                self.game_over = True
            else:
                self.ball_x = self.width // 2
                self.ball_y = self.height // 2
                self.ball_dx = random.choice([-4, 4]) / 15
                self.ball_dy = -4 / 15

        # Столкновение с платформой
        paddle_rect = pygame.Rect(self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height)
        ball_rect = pygame.Rect(self.ball_x - self.ball_size, self.ball_y - self.ball_size,
                                self.ball_size * 2, self.ball_size * 2)
        if ball_rect.colliderect(paddle_rect):
            self.ball_dy *= -1
            self.ball_y = self.paddle_y - self.ball_size

        # Столкновение с блоками
        for block_rect, color in self.blocks:
            if ball_rect.colliderect(block_rect):
                self.blocks.remove((block_rect, color))
                self.ball_dy *= -1
                self.score += 1
                break

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_score(self):
        """Отображает счет."""
        self.draw_text(f"Счет: {self.score}", 100, 30, self.black)

    def draw_lives(self):
        """Отображает жизни."""
        self.draw_text(f"Жизни: {self.lives}", self.width - 100, 30, self.black)

    def draw_message(self):
        """Отображает сообщение о завершении игры."""
        if self.lives == 0:
            text = f"Вы проиграли! Ваш счет: {self.score}"
        elif len(self.blocks) == 0:
            text = f"Вы победили! Ваш счет: {self.score}"
        else:
            return
        self.draw_text(text, self.width // 2, self.height // 2, self.black)

    def run(self):
        """Основной игровой цикл."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.fon is not None:
                        pygame.display.set_mode((self.fon.get_width(), self.fon.get_height()))
                        pygame.display.flip()
                    return 2
            keys = pygame.key.get_pressed()
            self.move_paddle(keys)
            self.move_ball()

            self.screen.fill(self.gray)
            self.draw_blocks()
            self.draw_paddle()
            self.draw_ball()
            self.draw_score()
            self.draw_lives()
            if self.game_over or len(self.blocks) == 0:
                self.draw_message()
            pygame.display.flip()
        pygame.quit()
        sys.exit()


def start_screen():
    player = Player(0, 300)
    fon_game = Fon()
    c = ((220, 200, 3), (510, 250, 4), (860, 200, 5))
    btn1 = Button(220, 200, 3)
    btn2= Button(510, 250, 4)

    btn3 = Button(860, 200, 5)
    # for i in range(3):
    #     btn = Button(c[i][0], c[i][1], c[i][2])
    #     btn_lst.append(btn)
    screen = pygame.display.set_mode(size)
    intro_text = ["Правила (нажмите клавишу F)",
                  "",
                  "  Нажмите SPACE для начала"]

    fon = pygame.transform.scale(load_image('47777.jpg'), (width, height))
    fon.set_alpha(50)
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Times New Roman', 30)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 400
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    level = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if level != 1:
                        os.environ['SDL_VIDEO_CENTERED'] = '1'
                        screen = pygame.display.set_mode((500, 500))
                        level = 1
                    elif level == 0:
                        screen = pygame.display.set_mode(size)
                        screen.blit(fon, (0, 0))
                        text_coord = 300
                        for line in intro_text:
                            string_rendered = font.render(line, 1, pygame.Color('white'))
                            intro_rect = string_rendered.get_rect()
                            text_coord += 10
                            intro_rect.top = text_coord
                            intro_rect.x = 400
                            text_coord += intro_rect.height
                            screen.blit(string_rendered, intro_rect)
                            level = 0

                if event.key == pygame.K_SPACE:
                    screen = pygame.display.set_mode(size)
                    level = 2
                    continue
                napr = (0, 0)
                if event.key == pygame.K_w:
                    napr = (0, -1)
                if event.key == pygame.K_s:
                    napr = (0, 1)
                if event.key == pygame.K_a:
                    napr = (-1, 0)
                if event.key == pygame.K_d:
                    napr = (1, 0)
                player.move_player(napr)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    xpoint, ypoint = event.pos
                    if 220 < xpoint < 220 + 200:
                        if 200 < ypoint < 200 + 100:
                            level = 3
                            continue

                    if 510 < xpoint < 510 + 200:

                        if 250 < ypoint < 250 + 100:
                            level = 4
                            continue
                    if 860 < xpoint < 860 + 200:
                        if 200 < ypoint < 200 + 100:
                            level = 5
                            continue

        if level == 1:
            screen.fill((0, 0, 0))
            pravila_text = ["Вам нужно пройти все уровни.",
                            "Для этого проходите мини-игры",
                            "",
                            "Чтобы вернуться на главный экран,",
                            "нажмите клавишу F"]
            text_coord = 70
            for line in pravila_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        if level == 2:
            screen.fill((0, 0, 0))
            all_sprites.draw(screen)
            player_group.draw(screen)
            button_group.draw(screen)
        if level == 3:
            game = ClickTheColor()
            level = game.run()
            screen = pygame.display.set_mode(size)
            btn1.kill()

            player.rect.x = 220
            player.rect.y = 200
        if level == 4:
            game = TicTacToe()
            level = game.run()
            screen = pygame.display.set_mode(size)
            btn2.kill()

            player.rect.x = 510
            player.rect.y = 250
        if level == 5:
            game = Breakout()
            level = game.run()
            screen = pygame.display.set_mode(size)
            btn3.kill()

            player.rect.x = 860
            player.rect.y = 200
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
