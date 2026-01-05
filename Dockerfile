FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    DATA_DIR=/app/data \
    HABIT_LOG_HOST=0.0.0.0 \
    HABIT_LOG_PORT=10021

WORKDIR /app

RUN groupadd --system app \
    && useradd --system --gid app \
    --home /home/app --create-home --shell /usr/sbin/nologin app

COPY requirements.txt /app/
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app src /app/src

RUN install -d -m 775 -o app -g app /app/data

USER app

EXPOSE 10021

CMD ["python", "-m", "src.habit_log"]
