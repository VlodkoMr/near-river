FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

RUN chmod +x ./scripts/start_api.sh

# Run app.py when the container launches
CMD ["sh", "-c", "./scripts/start_api.sh"]
