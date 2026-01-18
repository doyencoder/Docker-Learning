# base image
FROM python:3.9

# working directory
WORKDIR /app

# copy cmd
COPY . /app

# run cmd
RUN pip install -r requirements.txt

# port exposure
EXPOSE 5000

# command
CMD ["python", "app.py"]