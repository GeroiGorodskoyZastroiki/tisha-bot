import os
import nltk
import random
from dotenv import load_dotenv
from pyrogram import Client, filters
from nltk.tokenize import word_tokenize

# Загрузка ресурсов для токенизации
nltk.download('punkt')  

# Загрузка переменных окружения из файла .env
load_dotenv('.env')

# Получение параметров из .env файла
api_id = int(os.getenv('API_ID'))
api_hash = str(os.getenv('API_HASH'))
bot_token = str(os.getenv('BOT_TOKEN'))

# Инициализация клиента Pyrogram
app = Client('my_bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Обработчик входящих сообщений
@app.on_message(filters.private)  # Фильтр для приватных сообщений
def meow(client, message):
    # Проверяем случайное число для отправки сообщения или фото
    rand = random.uniform(0, 1)
    if has_meaning(message.text):
        send_random_line(client, message)
    if has_meaning(message.text) and rand < 1/4:
        send_random_photo(client, message)

def has_meaning(input_text):
    words = word_tokenize(input_text)
    word_count = len(words)
    min_word_count = 1
    return word_count >= min_word_count

# Функция для отправки случайной строки на основе вероятностей
def send_random_line(client, message):
    with open('lines.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

        # Вычисляем диапазоны вероятностей для строк из файла
        cumulative_range = 0
        ranges = []
        for line in lines:
            chance = int(line.split()[0])
            ranges.append((cumulative_range, cumulative_range + chance))
            cumulative_range += chance
        
        # Генерируем случайное число в пределах суммы вероятностей
        random_num = random.randint(0, sum(int(line.split()[0]) for line in lines) - 1)
        
        # Определяем, какую строку отправить на основе случайного числа и диапазонов вероятностей
        for index, (start, end) in enumerate(ranges):
            if start <= random_num < end:
                random_line = lines[index].split(maxsplit=1)[1]  # Получаем текст строки без вероятности
                # Генерируем случайное число повторений строки от 1 до 5
                repetitions = random.randint(1, 5)
                # Формируем строку, повторяя случайную строку нужное количество раз через пробел
                repeated_string = " ".join([random_line.strip() for _ in range(repetitions)])
                client.send_message(message.chat.id, repeated_string)
                break

# Функция для отправки случайного фото из папки
def send_random_photo(client, message):
    photo_path = 'photos/'  # Путь к папке с фото
    photo = random.choice(os.listdir(photo_path))
    client.send_photo(message.chat.id, photo=open(photo_path + photo, 'rb'))

# Запуск бота
app.run()