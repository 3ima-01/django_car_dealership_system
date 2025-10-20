FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY .env .
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 8000

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]