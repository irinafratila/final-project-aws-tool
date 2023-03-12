FROM python:3.9

RUN apt update
RUN apt install python3 -y
RUN pip install boto3

# copy file from machine to image
COPY JobTask.py ./

CMD ["python", "./JobTask.py"]