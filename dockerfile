FROM python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt  # ← Solo dependencias
COPY . .                           # ← Solo código
CMD ["python", "main.py"]