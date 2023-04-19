import sqlite3
import random
connection = sqlite3.connect("Database.sl3", 5)
cur = connection.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS data (name TEXT PRIMARY KEY, highscore REAL)")

player_name = input("Введите своё имя: ")

# ищем игрока в таблице
cur.execute("SELECT * FROM data WHERE name=?", (player_name,))
player = cur.fetchone()

if player is not None:
    # если игрок уже существует, извлекаем его рекорд
    print(f"С возвращением, {player_name}! Ваш личный рекорд: {player[1]}.")
    highscore = player[1]
else:
    # добавляем новую запись для нового игрока
    print(f"Добро пожаловать, {player_name}!")
    cur.execute("INSERT INTO data(name, highscore) VALUES (?, 0)", (player_name,))
    highscore = 0

def display_intro():
    title = "** Математическая Игра **"
    print("*" * len(title))
    print(title)
    print("*" * len(title))



def display_menu():
    menu_list = ["1. Сложение", "2. Вычитание", "3. Умножение", "4. Целочисленное Деление", "5. Выход"]
    print(menu_list[0])
    print(menu_list[1])
    print(menu_list[2])
    print(menu_list[3])
    print(menu_list[4])


def display_separator():
    print("-" * 24)


def get_user_input():
    user_input = int(input("Ваш выбор: "))
    while user_input > 5 or user_input <= 0:
        print("Некорректный запрос.")
        user_input = int(input("Пожалуйста, попробуйте снова: "))
    else:
        return user_input


def get_user_solution(problem):
    while True:
        user_input = input(f"{problem} = ")
        if user_input == "":
            print("Введите число")
        else:
            try:
                result = int(user_input)
                return result
            except ValueError:
                print("Введите число")



def check_solution(user_solution, solution, count):
    if user_solution == solution:
        count = count + 1
        print("Правильно!")
        return count
    else:
        print("Неправильно!")
        return count


def menu_option(index, count):
    number_one = random.randrange(1, 50)
    number_two = random.randrange(1, 50)
    if index == 1:
        problem = str(number_one) + " + " + str(number_two)
        solution = number_one + number_two
        user_solution = get_user_solution(problem)
        count = check_solution(user_solution, solution, count)
        return count
    elif index == 2:
        problem = str(number_one) + " - " + str(number_two)
        solution = number_one - number_two
        user_solution = get_user_solution(problem)
        count = check_solution(user_solution, solution, count)
        return count
    elif index == 3:
        number_two = random.randrange(1, 15)
        problem = str(number_one) + " * " + str(number_two)
        solution = number_one * number_two
        user_solution = get_user_solution(problem)
        count = check_solution(user_solution, solution, count)
        return count
    else:
        number_two = random.randrange(1, 15)
        problem = str(number_one) + " // " + str(number_two)
        solution = number_one // number_two
        user_solution = get_user_solution(problem)
        count = check_solution(user_solution, solution, count)
        return count


def display_result(total, correct):
    if total > 0:
        result = correct / total
        percentage = round((result * 100), 2)
    if total == 0:
        percentage = 0
    print("Вы ответили на", total, "вопросов,", correct, "из которых были правильны.")
    print("Ваш счёт: ", percentage, "%. Спасибо за уделённое время!", sep = "")


    cur.execute("INSERT INTO data(highscore) VALUES (?)", (correct,))



def main():
    display_intro()
    display_menu()
    display_separator()

    option = get_user_input()
    total = 0
    correct = 0
    while option != 5:
        total = total + 1
        correct = menu_option(option, correct)
        option = get_user_input()

    print("Покинуть игру.")
    display_separator()
    display_result(total, correct)

    cur.execute("UPDATE data SET highscore = ? WHERE name = ?", (correct, player_name))
    connection.commit()
    connection.close()

main()

