import pygame, math
from PIL import Image
from ThuatToan import *


class Piece:
    def __init__(self, laber, surface):
        self.laber = laber
        self.surface = surface


class Button:
    def __init__(self, name, pos, size, surface, font, color=(117, 117, 117)):
        self.name = name
        self.pos = pos
        self.size = size
        self.surface = surface
        self.font = font
        self.color = color
        self.text = self.font.render(self.name, True, (0, 0, 0))

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.pos, self.size), 3)
        x_s, y_s = self.text.get_size()
        self.surface.blit(self.text, (self.pos[0] + int(self.size[0] / 2) - int(x_s / 2),
                                      self.pos[1] + int(self.size[1] / 2) - int(y_s / 2)))

    def click(self, x, y):
        if self.pos[0] <= x <= self.pos[0] + self.size[0] and self.pos[1] <= y <= self.pos[1] + self.size[1]:
            return True
        else:
            return False


def paint(surface, matrix, pieces, l):
    for y in range(0, len(matrix)):
        for x in range(0, len(matrix[0])):
            for i in pieces:
                if i.laber == matrix[y][x]:
                    surface.blit(i.surface, ((x * l) + x + 3, (y * l) + y + 3))


def cut(img, tl, dr):
    cut_img = []
    for y in range(tl[1], dr[1]):
        cut_img.append(img[y][tl[0]:dr[0]])
    cut_img = np.array(cut_img)
    return cut_img


def getSize():
    pygame.init()
    pygame.display.set_caption("Nhập n")
    myfont = pygame.font.SysFont("monospace", 14, 2)
    editSize = (300, 200)
    editScreen = pygame.display.set_mode(size=editSize)
    s = 3
    buttonAdd = Button("+", (200, 50), (40, 20), editScreen, myfont)
    buttonMinus = Button("-", (200, 90), (40, 20), editScreen, myfont)
    buttonOk = Button("Ok", (100, 140), (100, 30), editScreen, myfont)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return s
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if buttonOk.click(x, y):
                    pygame.quit()
                    return s
                if buttonAdd.click(x, y) and s < 4:
                    s += 1
                elif buttonMinus.click(x, y) and s > 3:
                    s -= 1
        editScreen.fill((255, 255, 255))
        editScreen.blit(myfont.render("Nhập kích thước ma trận n x n", True, (0, 0, 0)), (20, 20))
        editScreen.blit(myfont.render("n = ", True, (0, 0, 0)), (45, 72))
        editScreen.blit(myfont.render(str(s), True, (0, 0, 0)), (82, 72))
        pygame.draw.rect(editScreen, (100, 100, 100), (80, 70, 60, 20), 2)
        buttonAdd.draw()
        buttonMinus.draw()
        buttonOk.draw()
        pygame.display.update()


if __name__ == "__main__":
    import os, sys, time

    if not os.path.exists("image"):
        os.makedirs("image")
    mouse = pygame.mouse
    s = getSize()
    pygame.init()
    myfont = pygame.font.SysFont("monospace", 14)
    size = (600, 500)
    pygame.display.set_caption("Trò chơi ghép hình")

    screen = pygame.display.set_mode(size=size)

    T_SIZE = (308, 308)
    table = pygame.Surface(size=T_SIZE)
    terminal = pygame.Surface((230, 250))

    button1 = Button("Backward", (400, 50), (80, 30), screen, myfont)
    button2 = Button("Move on", (500, 50), (80, 30), screen, myfont)
    button3 = Button("Use algorithm", (400, 100), (180, 30), screen, myfont)
    button4 = Button("Play again", (400, 150), (180, 30), screen, myfont, color=(255, 0, 0))

    source = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 0]])
    if s == 3:
        source = np.array([[1, 2, 3],
                           [4, 5, 6],
                           [7, 8, 0]])
    elif s == 4:
        source = np.array([[1, 2, 3, 4],
                           [5, 6, 7, 8],
                           [9, 10, 11, 12],
                           [13, 14, 15, 0]])

    begin = np.copy(source)
    begin = mix(begin)

    img = pygame.image.load("image.jpg")
    img = pygame.transform.scale(img, (300, 300))
    source_img = img.copy()
    source_img = pygame.transform.scale(source_img, (160, 160))
    pygame.image.save(img, "image/pic.jpg")

    img = Image.open("image/pic.jpg")
    img = np.array(img)

    n = np.size(begin)
    a = int(math.sqrt(n))
    l = int(300 / a)
    i = 1

    for y in range(0, 300, l):
        for x in range(0, 300, l):
            cut_img = cut(img, (x, y), (x + l, y + l))
            imgSave = Image.fromarray(cut_img)
            imgSave.save(f"image/pic{i}.jpg")
            i += 1

    STATE = [begin]
    pointer = 0
    running = True
    update = False
    texts = []
    PIECE = []
    for i in range(1, n):
        PIECE.append(Piece(laber=i, surface=pygame.image.load(f"image/pic{i}.jpg")))

    matrix = np.copy(begin)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(f"image/pic.jpg")
                for i in range(1, n + 1):
                    os.remove(f"image/pic{i}.jpg")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if 20 <= x <= 320 and 20 <= y <= 320:
                    for y_a in range(0, a):
                        for x_a in range(0, a):
                            if l * x_a <= x <= l * (x_a + 1) and l * y_a <= y <= l * (y_a + 1) and running:
                                value = findValue(matrix, (y_a, x_a))
                                xp, yp = y_a, x_a
                                if value == 0:
                                    texts.clear()
                                    texts.append("Nước đi không hợp lệ")
                                else:
                                    x0, y0 = findPosition(matrix, 0)
                                    if x0 == xp - 1 and y0 == yp:
                                        moveDown(matrix, x0, y0)
                                        update = True
                                        texts.clear()
                                    elif x0 == xp + 1 and y0 == yp:
                                        moveUp(matrix, x0, y0)
                                        update = True
                                        texts.clear()
                                    elif x0 == xp and y0 == yp + 1:
                                        moveLeft(matrix, x0, y0)
                                        update = True
                                        texts.clear()
                                    elif x0 == xp and y0 == yp - 1:
                                        moveRight(matrix, x0, y0)
                                        update = True
                                        texts.clear()
                                    else:
                                        texts.clear()
                                        texts.append("Nước đi không hợp lệ")
                                    if update:
                                        if len(STATE) == pointer + 1:
                                            STATE.append(matrix)
                                            matrix = np.copy(STATE[-1])
                                        elif len(STATE) > pointer + 1:
                                            STATE = STATE[0:pointer + 1]
                                            STATE.append(matrix)
                                            matrix = np.copy(STATE[-1])
                                        pointer += 1
                                        update = False
                if button1.click(x, y):
                    if pointer > 0:
                        pointer -= 1
                        matrix = np.copy(STATE[pointer])
                if button2.click(x, y):
                    if pointer + 1 < len(STATE):
                        pointer += 1
                        matrix = np.copy(STATE[pointer])
                if button3.click(x, y):
                    STATE = STATE[0:pointer+1]
                    startTime = time.perf_counter()
                    # chay thuat toan
                    finalState, steps, nodeNotUse, nodeHadUse = GiaiBaiToanGhepHinh(matrix=matrix, source=source)
                    endTime = time.perf_counter()
                    runTime = round((endTime - startTime), 4)
                    for step in steps:
                        m = np.copy(STATE[-1])
                        x, y = findPosition(m, 0)
                        if step == "up":
                            moveUp(m, x, y)
                        elif step == "down":
                            moveDown(m, x, y)
                        elif step == "left":
                            moveLeft(m, x, y)
                        elif step == "right":
                            moveRight(m, x, y)
                        STATE.append(m)
                    texts.clear()
                    texts.append(f"Thời gian chạy: {runTime} s")
                    texts.append(f"Số bước tìm được bởi thuật")
                    texts.append(f"toán: {len(steps)}")
                    texts.append(f"Tổng số bước đi: {len(STATE) - 1}")
                    texts.append(f"Số nút đã xét: {nodeHadUse}")
                    texts.append(f"Số nút chưa xét: {nodeNotUse}")
                    texts.append(f"Tổng số nút: {nodeHadUse + nodeNotUse}")
                    pointer = len(STATE) - 1
                    matrix = STATE[pointer]
                    button3.color = (100, 100, 100)
                if button4.click(x, y) and not running:
                    STATE.clear()
                    texts.clear()
                    STATE.append(mix(begin))
                    pointer = 0
                    running = True
                    matrix = np.copy(STATE[0])
        screen.fill((255, 255, 255))
        button1.draw()
        button2.draw()
        button3.draw()
        screen.blit(table, (20, 20))
        screen.blit(terminal, (350, 200))
        screen.blit(source_img, (20, 330))
        terminal.fill((100, 100, 100))
        h = 0
        for text in texts:
            terminal.blit(myfont.render(text, True, (255, 255, 255)), (10, 10 + h))
            h += 20
        table.fill((0, 0, 0))
        paint(table, matrix, PIECE, l)
        if (matrix == source).all() and running:
            running = False
            texts.append("Bạn đã thắng")
        if not running:
            button4.draw()
        pygame.display.update()
