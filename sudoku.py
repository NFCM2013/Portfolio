import random
import copy

def flat(sudoku):
    flat = [x for row in sudoku for x in row]
    return flat

def get_row(sudoku,grid):
    row = [[]for i in range(grid)]
    count = 0
    for element in sudoku:
        row_num = count//grid
        row[row_num].append(element)
        count += 1
    return row

def get_column(sudoku,grid):
    column = [[]for i in range(grid)]
    count = 0
    for element in sudoku:
        row_num = count % grid
        column[row_num].append(element)
        count += 1
    return column

def create_card(grid):
    card = [[] for a in range(grid)]  # 全候補用意
    for i in range(grid):
        for j in range(grid):
            card[i].append(j + 1)
    return card

def clear_card_based_on_row(row, card, grid, row_num):
    for column in range(grid):  # その行の各要素まわす
        if row[row_num][column]:  # 埋まってるものがあったら
            for num_column in range(grid):
                card[num_column].remove(row[row_num][column])  # それと同じ数の候補を消す
    return card

def clear_card_based_on_column(column, card, grid):
    for i in range(grid):
        for j in range(grid):
            if column[i][j] in card[i]:
                card[i].remove(column[i][j])
    return card

def clear_card_based_on_block(answer,card,grid,card_row):
    block = [[[] for j in range(3)] for k in range(3)]
    for i in range(grid):
        block_row = i // 3
        for j in range(grid):
            block_column = j // 3
            block[block_row][block_column].append(answer[i][j])
    for k in range(grid):
        for x in range(grid):
            if block[card_row // 3][k // 3][x] in card[k]:
                card[k].remove(block[card_row // 3][k // 3][x])
    return card


def fill_in_the_blank(answer,card,order,row_num):
    for column in order:
        if not answer[row_num][column]:
            if not card[column]:
                return False
            else:
                answer[row_num][column] = random.choice(card[column])
                for num_column in range(len(order)):
                    if answer[row_num][column] in card[num_column]:
                        card[num_column].remove(answer[row_num][column])
        # print(answer)
    return answer

def get_card_length_order(card):
    count = []
    for i in card:
        length = len(i)
        count.append(length)
    order = []
    char = 0
    while len(order) < len(count):
        for i in range(len(count)):
            if count[i] == char:
                order.append(i)
        char += 1
    return order

def sudoku_checker(answer,grid):
    def row_column_checker(answer,grid):
        for row in range(grid):
            if 0 in answer[row]:
                return False
            for column in range(grid):
                next_row = row+1
                while next_row<grid:
                    if answer[row][column] == answer[next_row][column]:
                        return False
                    next_row += 1
        return True
    def block_checker(answer,grid):
        block = [[[]for j in range(3)]for k in range(3)]
        for i in range(grid):
            block_row = i // 3
            for j in range(grid):
                block_column = j // 3
                block[block_row][block_column].append(answer[i][j])
        for i in range(3):
            for j in range(3):
                print(sum(block[i][j]))
                if sum(block[i][j]) != 45:
                    return False
        return True
    return row_column_checker(answer,grid) and block_checker(answer,grid)

sudoku =[[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
          ]
grid = len(sudoku[0])
answer = copy.deepcopy(sudoku)
while not sudoku_checker(answer,grid):
    answer = copy.deepcopy(sudoku)
    for x in range(grid):
        row = get_row(flat(answer),grid)
        column = get_column(flat(answer),grid)
        card = create_card(grid)
        card = clear_card_based_on_row(row,card,grid,x)
        card = clear_card_based_on_column(column,card,grid)
        card = clear_card_based_on_block(answer,card,grid,x)
        order = get_card_length_order(card)
        answer = fill_in_the_blank(answer,card,order,x)
        #print(answer)
        if answer== False:
            answer = copy.deepcopy(sudoku)
            break
print(answer)