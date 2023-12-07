import numpy as np
import random
import time


class State:
    def __init__(self, matrix, g, h, step, f_matrix):
        self.matrix = matrix
        self.g = g
        self.h = h
        self.f = g + h
        self.step = step
        self.f_matrix = f_matrix


def mix(matrix):
    steps = random.randint(50, 101)
    for i in range(0, steps):
        canMove = moveCanDo(matrix)
        m = random.choice(canMove)
        move(matrix, m)
    return matrix


def move(matrix, order):
    x, y = findPosition(matrix, 0)
    if order == "up":
        moveUp(matrix, x, y)
    if order == "down":
        moveDown(matrix, x, y)
    if order == "left":
        moveLeft(matrix, x, y)
    if order == "right":
        moveRight(matrix, x, y)


def moveUp(matrix, x, y):
    swap(matrix, (x, y), (x - 1, y))


def moveDown(matrix, x, y):
    swap(matrix, (x, y), (x + 1, y))


def moveLeft(matrix, x, y):
    swap(matrix, (x, y), (x, y - 1))


def moveRight(matrix, x, y):
    swap(matrix, (x, y), (x, y + 1))


# Doi gia tri hai vi tri f va t
def swap(matrix, f, t):
    x = matrix[t[0], t[1]]
    matrix[t[0], t[1]] = matrix[f[0], f[1]]
    matrix[f[0], f[1]] = x


# Tim vi tri cua o co gia tri = value
def findPosition(matrix, value):
    x, y = 0, 0
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            if matrix[i][j] == value:
                x = i
                y = j
    return x, y


def findValue(matrix, pos):
    return matrix[pos[0]][pos[1]]


# Tim cac buoc co the di
def moveCanDo(matrix):
    x, y = findPosition(matrix, 0)
    canMove = []
    if x != 0:
        canMove.append("up")
    if x != len(matrix) - 1:
        canMove.append("down")
    if y != 0:
        canMove.append("left")
    if y != len(matrix[0]) - 1:
        canMove.append("right")
    return canMove


def heuristic(matrix, source):
    h = 0
    for x in range(0, len(source)):
        for y in range(0, len(source[0])):
            v = source[x][y]
            if v != 0:
                xs, ys = findPosition(matrix, v)
                h += abs(xs - x) + abs(ys - y)
    return h


# true if matrix in CLOSE
def check(matrix, CLOSE):
    for state in CLOSE:
        if (state.matrix == matrix).all():
            return True
    return False


def GiaiBaiToanGhepHinh(matrix, source):
    #
    startTime = time.perf_counter()
    #

    OPEN = []
    CLOSE = []

    # g = so buoc di; h = chi phi uoc luong
    OPEN.append(State(matrix=matrix, g=0, h=heuristic(matrix, source), step="", f_matrix=None))
    while True:
        if not OPEN:
            print("Bai toan ko co loi giai")
            break
        # tim state co f nho nhat
        l = 0
        minF = OPEN[0].f
        for i in range(1, len(OPEN)):
            if minF > OPEN[i].f:
                minF = OPEN[i].f
                l = i
        # print(len(OPEN), len(CLOSE), OPEN[l].f)
        state = OPEN[l]
        CLOSE.append(state)
        OPEN.remove(state)

        if (state.matrix == source).all():
            # ket qua
            steps = []
            s = state
            while True:
                # truy nguoc lai
                steps.insert(0, s.step)
                for x in CLOSE:
                    if (x.matrix == s.f_matrix).all():
                        s = x
                if (s.matrix == matrix).all():
                    break
            return state, steps, len(OPEN), len(CLOSE)
        else:
            newState = []
            move = moveCanDo(state.matrix)
            x, y = findPosition(state.matrix, 0)
            for newMove in move:
                if newMove == "up":
                    newMatrix = np.copy(state.matrix)
                    moveUp(newMatrix, x, y)
                    newState.append(State(matrix=newMatrix, g=state.g + 1, h=heuristic(newMatrix, source),
                                          step="up", f_matrix=np.copy(state.matrix)))
                elif newMove == "down":
                    newMatrix = np.copy(state.matrix)
                    moveDown(newMatrix, x, y)
                    newState.append(State(matrix=newMatrix, g=state.g + 1, h=heuristic(newMatrix, source),
                                          step="down", f_matrix=np.copy(state.matrix)))
                elif newMove == "left":
                    newMatrix = np.copy(state.matrix)
                    moveLeft(newMatrix, x, y)
                    newState.append(State(matrix=newMatrix, g=state.g + 1, h=heuristic(newMatrix, source),
                                          step="left", f_matrix=np.copy(state.matrix)))
                elif newMove == "right":
                    newMatrix = np.copy(state.matrix)
                    moveRight(newMatrix, x, y)
                    newState.append(State(matrix=newMatrix, g=state.g + 1, h=heuristic(newMatrix, source),
                                          step="right", f_matrix=np.copy(state.matrix)))

            # loai cac trang thai da co trong CLOSE
            for state in newState:
                if check(state.matrix, CLOSE):
                    newState.remove(state)
            OPEN += newState

######################################################################
        if round(time.perf_counter() - startTime) % 10 == 0:
            print(len(OPEN), len(CLOSE))


if __name__ == "__main__":
    source = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 0]])
    # source = np.array([[1, 2, 3, 4],
    #                    [5, 6, 7, 8],
    #                    [9, 10, 11, 12],
    #                    [13, 14, 15, 0]])
    begin = np.copy(source)
    begin = mix(begin)
    print("Trang thai dau:")
    print(begin)

    startTime = time.perf_counter()
    finalState, steps, nodeNotUse, nodeHadUse = GiaiBaiToanGhepHinh(begin, source)
    endTime = time.perf_counter()
    print(finalState.matrix)
    print(finalState.f)
    print(steps)
    print(f"So nut da xet: {nodeHadUse}\tSo nut chua xet: {nodeNotUse}")
    print(f"Thoi gian chay: {endTime - startTime} s")
