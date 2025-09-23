FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# unbuffered mode for print messages
CMD ["python", "-u", "main.py"]
