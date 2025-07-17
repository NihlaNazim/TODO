#this tell to docker- start from an official py image with version 3.10 already install

FROM python:3.10

#set working directory inside the container to /app
WORKDIR /app

#copies all files from my local app/ folder to /app in the container
COPY requirements.txt .

#install flask and psycopg2 inside the container
RUN pip install -r requirements.txt

COPY . .

#starts the flsk app when the container runs
CMD ["python", "app.py"]

#what happens when you build this dockerfile
#01.Docker setup a python 3.10 container
#02.creates a /app directory inside that container
#03.copies your app code into into
#04 install required python libraries
#05. runs my app with: python app.py