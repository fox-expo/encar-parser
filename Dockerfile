FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libatspi2.0-0 \
    libxcomposite1 libxdamage1 libxfixes3 libgbm1 libxcb1 libxkbcommon0 \
    libasound2 libx11-xcb1 libxrandr2 libxss1 libxtst6 libgtk-3-0 libdrm2 \
    libxshmfence1 libxext6 libxrender1 libx11-6 libxau6 libxdmcp6 \
    fonts-liberation libappindicator3-1 libnss3-dev libnspr4-dev wget \
    ca-certificates && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps

COPY encar_parser.py .
WORKDIR /

CMD ["python", "encar_parser.py"]
