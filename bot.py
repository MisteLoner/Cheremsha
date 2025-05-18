from typing import List


def step_ai(board: List[list]) -> List[list]:
    """
    Возвращает новую доску с ходом бота
    Алгоритм:
    - 1. проверить если выйгрышные позиции у бота и если есть поставить туда
    - 2. проверить если выйгрышные позиции у игрока и если есть поставить туда
    - 3. проверить свободен ли центр и если да то поставить туда.
    - 4. проверить если свободные края и если есть свободные то поставить туда
    - 4.1 проверить если поставленные клетки и если есть то поставить на их путях
    - 5. проверить есть ли свободные клетки по бокам доски и если есть поставить туда
    иначе доска проигрына
    :param board: Игровая доска
        X - клетки игрока
        O - клетки бота
        _ - клетки пустоты
        пример пустой доски
        [[_, _, _],
        [_, _, _],
        [_, _, _]]
    :return: Новая доска с ходом бота
    """
    print(f"Изначальная строка: {board}")
    # Щаг 1
    # проверка по строкам
    print("проверка по строкам")
    for num, line in enumerate(board):
        print(f"Строка {line}")
        if line.count("O") == 2 and "X" not in line:
            line_index = line.index('_')
            board[num][line_index] = "O"
            return board

    # проверка по колонкам
    print("проверка по колонкам")
    for num in range(len(board)):
        line = list(lines[num] for lines in board)
        print(f"Колонка {line}")
        print(line)
        if line.count("O") == 2 and "X" not in line:
            line_index = line.index('_')
            board[line_index][num] = "O"
            return board


if __name__ == '__main__':
    boards = [["_", "_", "O"],
              ["_", "_", "_"],
              ["_", "_", "O"]]
    print(step_ai(boards))
