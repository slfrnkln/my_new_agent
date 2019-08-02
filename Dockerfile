FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip3 install -r requirements.txt

CMD ["python3", "/app/workdir/agent/demo_agent.py"]
