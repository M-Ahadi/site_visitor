FROM python:3.7-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt update && \
    apt install --no-install-recommends -y \
                 xvfb \
                 wget \
                 unzip

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get purge -y --auto-remove && \
    rm -rf /etc/apt/sources.list.d/temp.list && \
    rm google-chrome-stable_current_amd64.deb

RUN wget -q https://chromedriver.storage.googleapis.com/LATEST_RELEASE -O LATEST_RELEASE.txt && \
    chromedriver_version=$(cat LATEST_RELEASE.txt | sed 's/\n//g' ) && \
    wget -q https://chromedriver.storage.googleapis.com/$chromedriver_version/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip LATEST_RELEASE.txt

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x chromedriver

CMD ["python", "main.py"]