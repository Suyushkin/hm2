import os
import random
import re
from datetime import datetime, timedelta
from flask import Flask

app = Flask(__name__)

# ===== Глобальные переменные для задач =====

# Задача 2: Список машин (не пересоздаётся при каждом запросе)
cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']

# Задача 3: Список пород кошек (не пересоздаётся при каждом запросе)
cat_breeds = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая',
              'мейн-кун', 'манчкин']

# Задача 6: Загрузка слов из книги "Война и мир"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

def load_words_from_book():
    """Загружает все слова из книги и возвращает список слов без знаков препинания"""
    with open(BOOK_FILE, 'r', encoding='utf-8') as file:
        text = file.read()
        # Регулярное выражение для поиска слов (только буквы)
        words = re.findall(r'\b[а-яА-Яa-zA-Z]+\b', text)
        # Приводим все слова к нижнему регистру
        words = [word.lower() for word in words]
        return words

# Загружаем слова один раз при старте сервера
book_words = load_words_from_book()

# Задача 7: Счётчик посещений страницы /counter
counter_visits = 0

# ===== Endpoints =====

# Задача 1: /hello_world
@app.route('/hello_world')
def hello_world():
    return 'Привет, мир!'

# Задача 2: /cars
@app.route('/cars')
def get_cars():
    # Возвращаем список машин через запятую
    return ', '.join(cars_list)

# Задача 3: /cats
@app.route('/cats')
def get_cats():
    # Возвращаем случайную породу кошек
    return random.choice(cat_breeds)

# Задача 4: /get_time/now
@app.route('/get_time/now')
def get_time_now():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'Точное время: {current_time}'

# Задача 5: /get_time/future
@app.route('/get_time/future')
def get_time_future():
    current_time_after_hour = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    return f'Точное время через час будет {current_time_after_hour}'

# Задача 6: /get_random_word
@app.route('/get_random_word')
def get_random_word():
    # Выбираем случайное слово из предварительно загруженного списка
    random_word = random.choice(book_words)
    return random_word

# Задача 7: /counter
@app.route('/counter')
def counter():
    global counter_visits
    counter_visits += 1
    return str(counter_visits)

# ===== Запуск сервера =====
if __name__ == '__main__':
    print("Сервер запущен! Доступные адреса:")
    print("http://127.0.0.1:5000/hello_world")
    print("http://127.0.0.1:5000/cars")
    print("http://127.0.0.1:5000/cats")
    print("http://127.0.0.1:5000/get_time/now")
    print("http://127.0.0.1:5000/get_time/future")
    print("http://127.0.0.1:5000/get_random_word")
    print("http://127.0.0.1:5000/counter")
    app.run(debug=True)