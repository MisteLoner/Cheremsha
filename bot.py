import itertools
import logging
import random
from typing import List


def return_line(board: List[list]) -> list:
    """
    Возвращает строки доски
    :param board:
    :return:
    """
    return [line for line in board]


def return_columns(board: List[list]) -> list:
    """
    Возвращает колонки доски
    :param board:
    :return:
    """
    return [list(column[num] for column in board) for num in range(len(board))]


def return_diagonals(board: List[List[str]]) -> list:
    """
    Возвращает диагонали доски
    :param board:
    :return:
    """
    return [list(lines[nums if num else len(board[0]) - 1 - nums] for nums, lines in enumerate(board)) for num in
            range(2)]


def check_board(board: List[list], config: dict, char: str) -> tuple[List[list], bool]:
    """
    Проверяет если выйгрышные позиции и если есть ставит туда
    :param board: Игровая доска
    :param config: Конфиг доски с сигнатурой символов
    :param char: bot_char если проверка бота иначе player_char
    :return:
    """
    bot_char = config["bot_char"] if char == "bot_char" else config["player_char"]
    anti_char = config["player_char"] if char == "bot_char" else config["bot_char"]
    empty_char = config["empty_char"]
    logging.info("Проверка по строкам")
    for num, line in enumerate(return_line(board)):
        logging.debug(f"Строка {" ".join(line)}")
        if line.count(bot_char) == 2 and anti_char not in line:
            line_index = line.index(empty_char)
            logging.debug(f"Установка символа {config["bot_char"]} в {" ".join(line)} в индекс [{num}][{line_index}]")
            board[num][line_index] = config["bot_char"]
            return board, True

    # проверка по колонкам
    logging.info("Проверка по колонкам")
    for num, column in enumerate(return_columns(board)):
        logging.debug(f"Колонка {" ".join(column)}")
        if column.count(bot_char) == 2 and anti_char not in column:
            colum_index = column.index(empty_char)
            logging.debug(
                f"Установка символа {config["bot_char"]} в {" ".join(column)} в индекс [{num}][{colum_index}]")
            board[colum_index][num] = config["bot_char"]
            return board, True

    logging.info("Проверка по диагоналям")
    for num, diagonal in enumerate(return_diagonals(board)):
        logging.debug(f"Диагональ {" ".join(diagonal)}")
        if diagonal.count(bot_char) == 2 and anti_char not in diagonal:
            diagonal_index = diagonal.index(empty_char)
            print(diagonal_index)
            if not num:
                logging.debug(
                    f"Установка символа {config["bot_char"]} в диагональ \"{" ".join(diagonal)}\" в индекс [{3 - diagonal_index}][{diagonal_index}]")
                board[diagonal_index][2 - diagonal_index] = config["bot_char"]
            else:
                logging.debug(
                    f"Установка символа {config["bot_char"]} в диагональ \"{" ".join(diagonal)}\" в индекс [{3 - diagonal_index}][{diagonal_index}]")
                board[diagonal_index][diagonal_index] = config["bot_char"]
            return board, True
    return board, False


def step_ai(board: List[list], config: dict) -> List[list]:
    """
    Возвращает новую доску с ходом бота
    Алгоритм:
    - 1. проверить если выйгрышные позиции у бота и если есть поставить туда.
    - 2. проверить если выйгрышные позиции у игрока и если есть поставить туда.
    - 3. проверить свободен ли центр и если да то поставить туда.
    - 4. проверить если свободные края и если есть свободные то поставить туда.
    - 4.1 проверить если поставленные клетки и если есть то поставить на их путях.
    - 5. проверить есть ли свободные клетки по бокам доски и если есть поставить туда.
    Иначе доска заполнена.
    :param config:
    :param board: Игровая доска
        X - клетки игрока
        O - клетки бота
        _ - клетки пустоты
        пример пустой доски
        | 0 | 1 | 2|
        0[[_, _, _],
        1[_, _, _],
        2[_, _, _]]
    :return: Новая доска с ходом бота
    """
    angles = [i for i in list(itertools.product([0, 2], repeat=2)) if
              board[i[0]][i[1]] not in [config["bot_char"], config["player_char"]]]
    sides = [i for i in list(itertools.permutations([0, 1], 2)) + list(itertools.permutations([1, 2], 2)) if
             board[i[0]][i[1]] not in [config["bot_char"], config["player_char"]]]
    logging.info(f"Изначальная доска: {return_board(board)}")
    logging.debug("ШАГ 1 - проверить если выйгрышные позиции у бота и если есть поставить туда")
    bot_board = check_board(board, config, "bot_char")
    if bot_board[1]:
        return bot_board[0]

    logging.debug("ШАГ 2 - проверить если выйгрышные позиции у игрока и если есть поставить туда")
    player_board = check_board(board, config, "player_char")
    if player_board[1]:
        return player_board[0]

    logging.debug("ШАГ 3 - проверить свободен ли центр и если да то поставить туда.")
    if board[1][1] == config["empty_char"]:
        board[1][1] = config["bot_char"]
        return board

    logging.debug("ШАГ 4 - проверить если свободные края и если есть свободные то поставить туда.")
    if any(angles):
        cry_index = random.choice(angles)
        board[cry_index[0]][cry_index[1]] = config["bot_char"]
        return board

    logging.debug("ШАГ 5 - проверить есть ли свободные клетки по бокам доски и если есть поставить туда.")
    if any(sides):
        cry_index = random.choice(sides)
        board[cry_index[0]][cry_index[1]] = config["bot_char"]
        return board
    return board


def return_board(board: List[list]) -> str:
    """
    Возвращает строковое представление игрового поля
    :param board: Игровое поле
    :return: Строку представления поля
    """
    return "".join(["".join([f"{char} " for char in line]) + "\n" for line in board])


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
    board_config = {"player_char": "X",
                    "bot_char": "O",
                    "empty_char": "_"}
    boards = [["_", "_", "_"],
              ["_", "_", "_"],
              ["_", "_", "_"]]
    for i in range(3):
        boards = step_ai(boards, config=board_config)
        print(return_board(boards))
