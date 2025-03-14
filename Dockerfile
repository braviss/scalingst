FROM python:3.11

# Устанавливаем зависимости из requirements.txt
COPY requirements.txt /app/

WORKDIR /app

# Устанавливаем зависимости через pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY . /app

# Делаем скрипт запуска исполнимым
RUN chmod +x /app/ops/scripts/start-server.sh

# Указываем команду для запуска контейнера
CMD ["bash", "/app/ops/scripts/start-server.sh"]
