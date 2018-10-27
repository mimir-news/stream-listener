FROM python:3.6-slim-stretch
RUN apt-get update && apt-get upgrade -y && apt-get install -y build-essential

# Copy app source.
WORKDIR /app/streamlistener
COPY . .

# Install requirements.
RUN pip install --no-cache-dir -r requirements.txt

# Start command.
CMD ["sh", "start.sh"]
