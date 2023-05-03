import random
import datetime

start = datetime.datetime.now()

def make_column():
    column_list = []
    for i in range(9):
        column = []
        for j in range(9):
            col = sudoku[j][i]
            column.append(col)
        column_list.append(column)
    return column_list

def make_box():
    box_list = []
    for i in range(0, 7, 3): # 0, 3, 6
        for j in range(0, 7, 3): # 0, 3, 6
            box = []
            for x in range(3):
                for y in range(3):
                    b = sudoku[x+i][y+j]
                    box.append(b)
            box_list.append(box)
    return box_list

def boxNo_check(x, y):
    if 0 <= x < 3 and  0 <= y < 3:
        return 0
    elif 0 <= x < 3 and 3 <= y < 6: # x = 0, y = 3
        return 1
    elif 0 <= x < 3 and 6 <= y < 9:
        return 2
    elif 3 <= x < 6 and 0 <= y < 3:
        return 3
    elif 3 <= x < 6 and 3 <= y < 6:
        return 4
    elif 3 <= x < 6 and 6 <= y < 9: # x = 4, y = 6
        return 5
    elif 6 <= x < 9 and 0 <= y < 3:
        return 6
    elif 6 <= x < 9 and 3 <= y < 6:
        return 7
    elif 6 <= x < 9 and 6 <= y < 9:
        return 8

# 空のブロックにランダムで入れる数字のリストを作成
def check(x, y): # x = 2, y = 0
    boxNo = boxNo_check(x, y) # 0
    check_list = []
    column_list = make_column()
    box_list = make_box()

    # 行、列、ボックスにおいて重複しない数字を探す
    for i in range(1, 10):
        if i not in sudoku[x] and i not in column_list[y] and i not in box_list[boxNo]:
            check_list.append(i)
    return check_list

# ブロックにランダムで入れる数字が無くなれば、空のリストを返す
def solve():
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                pass
            else:
                c = check(i, j)
                if c != []:
                    x = random.choice(c)
                    sudoku[i][j] = x
                elif c == []:
                    return c

# 空のブロックに入れる数字が無くなるまで探索を繰り返す
c = []
while c == []:
    # 元のリストの作成
    sudoku = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
              [6, 0, 0, 1, 9, 5, 0, 0, 0],
              [0, 9, 8, 0, 0, 0, 0, 6, 0],
              [8, 0, 0, 0, 6, 0, 0, 0, 3],
              [4, 0, 0, 8, 0, 3, 0, 0, 1],
              [7, 0, 0, 0, 2, 0, 0, 0, 6],
              [0, 6, 0, 0, 0, 0, 2, 8, 0],
              [0, 0, 0, 4, 1, 9, 0, 0, 5],
              [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    c = solve()

# 実行時間の計測
end = datetime.datetime.now()
elapsed = end - start
print(elapsed)

# 答え
sudoku