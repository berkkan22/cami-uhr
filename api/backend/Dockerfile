
FROM python:3.9


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./backend /code/backend


CMD ["fastapi", "run", "backend/main.py", "--port", "80"]