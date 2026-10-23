FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

RUN useradd --uid 10001 --no-create-home appuser
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]