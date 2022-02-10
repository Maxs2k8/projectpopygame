import pygame
import random
import sys
import pyttsx3

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 30
 
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
 
    def render(self, screen):
        color = pygame.Color('white')
        for y in range(self.height):
            for x in range(self.width):
                coor = (x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, color, coor, 1)
 
 
    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y
 
    def on_click(self, cell):
        pass
 
    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


class Minesweeper(Board):
    def __init__(self, width, height, need):
        self.engine = pyttsx3.init()
        super().__init__(width, height)
        self.schot = 0
        self.board = [[-1] * width for inet in range(height)]
        ter = 0
        while ter < need:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] == -1:
                self.board[y][x] = 10
                ter += 1
 
    def open_click(self, cell):
        engine = self.engine
        schot = self.schot
        x, y = cell
        if self.board[y][x] == 10:
            engine.say(f"Вы проиграли! Ваш счёт составил: {self.schot}")
            print(f"Вы проиграли! Ваш счёт составил: {self.schot}")
            engine.runAndWait()
            pygame.quit()
            sys.exit()
            return
        s = 0
        s3 = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                    continue
                if self.board[y + dy][x + dx] == 10:
                    s += 1
        schot += 1
        if s == 0: 
            s1 = 0
            for x1 in range(self.width):
                for y1 in range(self.height):
                    mona = False
                    s1 = 0
                    if self.board[y1][x1] == -1:
                        for dy1 in range(-1, 2):
                            for dx1 in range(-1, 2):
                                if x1 + dx1 < 0 or x1 + dx1 >= self.width or y1 + dy1 < 0 or y1 + dy1 >= self.height:
                                    continue
                                if self.board[y1 + dy1][x1 + dx1] == 10:
                                    s1 += 1
                                elif self.board[y1 + dy1][x1 + dx1] == 0:
                                    mona = True
                                if self.board[y1 + dy1][x1 + dx1] == -1:
                                    s3 = 0
                                    x2 = x1 + dx1
                                    y2 = y1 + dy1
                                    for dy2 in range(-1, 2):
                                        for dx2 in range(-1, 2):
                                            if x2 + dx2 < 0 or x2 + dx2 >= self.width or y2 + dy2 < 0 or y2 + dy2 >= self.height:
                                                continue
                                            if self.board[y2 + dy2][x2 + dx2] == 10:
                                                s3 += 1
                                    if (s3 != 10 and s1 == 10) or (s3 == 0 and s1 != 10) and (abs(y1 - y2) <= 1 and abs(x1 - x2) <= 1):
                                        self.board[y2][x2] = s3
                                if self.board[y1 + dy1][x1 + dx1] == 10:
                                    s1 += 1
                                elif self.board[y1 + dy1][x1 + dx1] == 0:
                                    mona = True
                                    schot += 1
                        if mona:
                            self.board[y1][x1] = s1 // 2
        self.board[y][x] = s
        gg = True
        for y in range(y):
            for x in range(x):
                if self.board[y][x] in [-1]:
                    gg = False
        if gg:
            print("Поздравляю! Вы смогли пройти игру! Ваша награда - возможность поставить мне 100 баллов! XD")
            engine.say("Поздравляю! Вы смогли пройти игру!")
            try:
                with open('rec.txt', mode="r", encoding="utf-8") as rec:
                    if int(rec.readlines[0]) < schot:
                        print("Вы установили новый рекод, поздравляем!")
            except Exception:
                print("Вы установили новый рекод, поздравляем!")
            with open('rec.txt', mode="w", encoding="utf-8") as rec:
                rec.write(str(schot))
            engine.runAndWait()
 
    def on_click(self, cell):
        self.open_click(cell)
 
    def render(self, screen):
        color = pygame.Color('red')
        for y in range(self.height):
            for x in range(self.width):
                coor = (x * self.cell_size + self.left, y * self.cell_size + self.top,
                        self.cell_size, self.cell_size)
                coor1 = (x * self.cell_size + self.left + 2, y * self.cell_size + self.top + 2,
                        self.cell_size, self.cell_size)
                pygame.draw.rect(screen, pygame.Color('white'), coor, 1)
                if self.board[y][x] >= 0 and self.board[y][x] != 10:
                    font = pygame.font.Font(None, self.cell_size - 7)
                    text = font.render(str(self.board[y][x]), 1, (100, 255, 100))
                    screen.blit(text, coor1)
 
 
def main():
    engine = pyttsx3.init()
    engine.say("Внимание! Большая часть информации об игре будет выводиться в консоль питона, поэтому внимательно следите за ней!")
    print("""Здравствуйте! Это игра сапёр, написанная на pygame.
Введите пожалуйста (всё на отдельных строчках!):
Ширина поля
Высота поля
Кол-во мин на поле""")
    engine.runAndWait()
    try:
        rx = int(input())
        ry = int(input())
        km = int(input())
    except Exception as e:
        engine.say(f"Упс! Произошла ошибка: {e}, сообщите об этом в дискорде разработчику -  @Maxs#8815 !")
        print(f"Упс! Произошла ошибка: {e}, сообщите об этом в дискорде разработчику -  @Maxs#8815 !")
        engine.runAndWait()
        sys.exit()
    pygame.init()
    size = rx * 30, ry * 30
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Сапёр')
    clock = pygame.time.Clock()
    board = Minesweeper(rx, ry, km)
    ticks = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(50)
        ticks += 1
    pygame.quit()
 
 
if __name__ == '__main__':
    main()