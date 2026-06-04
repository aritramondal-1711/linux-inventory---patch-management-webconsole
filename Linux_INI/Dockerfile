FROM python:slim
WORKDIR /app

RUN apt update && apt install ssh  -y
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install ansible

COPY . .
EXPOSE 8000

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
