#Create a ubuntu base image with python 3 installed.
FROM python:3-slim
ENV PYTHONUNBUFFERED 1

#Set the working directory
RUN mkdir /app
WORKDIR /app

#Copy requirements
COPY requirements.txt /app
RUN pip install -r requirements.txt

#copy all the files
COPY . /app

#Expose the required port
EXPOSE 3000

#Run the command
CMD python3 app.py