# Використовуємо офіційний образ Python 3.9
FROM python:3.12.5

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файл requirements.txt до робочої директорії
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код до контейнера
COPY . .

# Вказуємо команду для запуску застосунку
CMD ["python", "your_script.py"]
