FROM python:3.9-slim

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app

RUN pip install -r requirements.txt
COPY . /opt/app

ENV WB_SELLER_TOKEN=<YOUR_TOKEN_STRING>
ENV TG_TOKEN=<YOUR_TOKEN_STRING>
ENV TG_CLIENT_ID=<YOUR_CHAT_ID_NUMBER>

CMD python main.py