# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim


# Install manually all the missing libraries
RUN apt-get update
RUN apt-get install -y wget

# Install Chrome

RUN pip install chromedriver-binary==90.0.4430.24

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

WORKDIR /usr/src/app

COPY /app .

RUN pip install -r requirements.txt

CMD python3 main.py