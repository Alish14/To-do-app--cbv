# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/




# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN pip3 install --upgrade pip
RUN python3 -m pip install -r requirements.txt

COPY ./core /app/
