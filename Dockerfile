FROM python:3.13-slim
WORKDIR /botik
RUN pip install --no-cache-dir aiogram requests
COPY . .
CMD ["python", "bot.py"]