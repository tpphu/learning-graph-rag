# Sử dụng Python 3.9 làm base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các công cụ cơ bản và các phụ thuộc của Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    unzip \
    libnss3 \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libu2f-udev \
    fonts-liberation \
    libvulkan1 \
    xdg-utils \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Tải và cài đặt Google Chrome từ liên kết trực tiếp
# Tham khao nhung version cu hon khac o day
# https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/
COPY raw/google-chrome-stable_114.0.5735.198-1_amd64.deb google-chrome-stable_114.0.5735.198-1_amd64.deb
RUN apt-get install -y ./google-chrome-stable_114.0.5735.198-1_amd64.deb && \
    rm google-chrome-stable_114.0.5735.198-1_amd64.deb

# Tải và cài đặt ChromeDriver phiên bản tương ứng
RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin && \
    rm chromedriver_linux64.zip

# Cài đặt pipenv để quản lý môi trường Python
RUN pip install pipenv

# Copy các tệp cấu hình pipenv
COPY Pipfile Pipfile.lock /app/

# Cài đặt các thư viện Python thông qua pipenv
RUN pipenv install --deploy --system

# Copy mã nguồn ứng dụng
COPY . /app/

# Cấp quyền cho thư mục làm việc
RUN chmod -R 777 /app

# Đặt lệnh khởi chạy mặc định
CMD ["bash"]
