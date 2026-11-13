# 1. Basis-Image verwenden
FROM python:3.12-slim

# 2. Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# 3. requirements.txt ZUERST kopieren (Nutzt den Docker-Cache optimal)
COPY requirements.txt .

# 4. Abhängigkeiten fest im Image installieren
RUN pip install --no-cache-dir -r requirements.txt

# 5. Den restlichen Code kopieren
COPY . .

# 6. Eigener Nutzer statt root
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# 7. Port freigeben
EXPOSE 8501

# 8. Startbefehl (Headless für Server)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
