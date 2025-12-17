FROM python:3.13.11

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "./bot.py"]