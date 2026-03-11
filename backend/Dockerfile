# ---- Backend Dockerfile ----
# dlib 需要 cmake + build-essential 才能編譯，使用完整 python 映像
FROM python:3.11

WORKDIR /app

# 安裝系統依賴（dlib、opencv 必要）
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libboost-python-dev \
    libboost-thread-dev \
    && rm -rf /var/lib/apt/lists/*

# 先複製 requirements 以利 Docker 快取
COPY requirements.txt .

# 安裝 Python 依賴（dlib 編譯約需 5-10 分鐘）
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼
COPY . .

# 建立 uploads 目錄
RUN mkdir -p uploads

EXPOSE 9453

CMD ["python", "app.py"]
