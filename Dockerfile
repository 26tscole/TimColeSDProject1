FROM python:3.12
WORKDIR /TimColeSDProject1

# Install PyAudio dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    libffi-dev \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download Vosk model
RUN wget -O vosk-model-small-en-us-0.15.zip \
    https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip \
    && unzip vosk-model-small-en-us-0.15.zip \
    && rm vosk-model-small-en-us-0.15.zip

# Copy the rest of your project
COPY . .

CMD ["python"]