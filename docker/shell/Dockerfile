# Sử dụng Python 3.9 làm base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Cài đặt các công cụ cần thiết
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    vim \
    && apt-get clean

# Copy file vào container (tuỳ chọn, không bắt buộc)
COPY . /app

# Giữ container chạy với một bash shell (chỉ để test, có thể thay đổi)
CMD [ "bash" ]
