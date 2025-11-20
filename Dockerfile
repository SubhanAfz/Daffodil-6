FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN uv pip install --no-cache-dir --system -r requirements.txt

# add gunicorn since it's used to run the app
RUN uv pip install --no-cache-dir --system 'gunicorn==23.0.0'

COPY . .

RUN uv run manage.py migrate

RUN uv run manage.py seed

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "recipify.wsgi:application"]