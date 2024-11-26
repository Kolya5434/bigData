# Используйте базовый образ Python
FROM python:3.12

# Установите Xvfb и необходимые зависимости для tkinter
RUN apt-get update && \
    apt-get install -y python3-tk xvfb && \
    apt-get clean

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файлы проекта в контейнер
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Настройте Xvfb для работы с tkinter
ENV DISPLAY=:99

# Запустите Xvfb и приложение
CMD ["xvfb-run", "-s", "-screen 0 1024x768x24", "python", "main.py"]