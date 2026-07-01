FROM python:3.11-slim

# System dependencies for the bot (ffmpeg, audio, 3D, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    gcc \
    g++ \
    portaudio19-dev \
    libsndfile1 \
    libassimp-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user
RUN mkdir -p /home/user/app && chown user:user /home/user/app

USER user
WORKDIR /home/user/app

ENV PATH="/home/user/.local/bin:$PATH"
ENV DATA_DIR="/tmp/data"
ENV PYTHONUNBUFFERED=1

# Better layer caching
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=user:user . .

EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1 --log-level info"]
