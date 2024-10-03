FROM python:3.12-slim

RUN #apt-get update \
#    && apt-get install -y gcc \
#    && apt-get clean

# Set the locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

RUN chmod +x ./scripts/start_api.sh

# Run app.py when the container launches
CMD ["sh", "-c", "./scripts/start_api.sh"]
