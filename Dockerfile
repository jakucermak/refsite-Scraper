FROM python:3.12.1-bullseye

# Vytvoření pracovního adresáře v kontejneru
WORKDIR /app

COPY ./src ./src
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Exponování portu, na kterém bude běžet FastAPI aplikace
EXPOSE 8000
WORKDIR /app/src
# Spuštění FastAPI aplikace při spuštění kontejneru
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

