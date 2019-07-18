FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN pip install pipenv

RUN pipenv sync

# Make port 80 available to the world outside this container
EXPOSE 80

# In reality, we usually set parameters with Environment Variables from k8s.
# https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/#define-an-environment-variable-for-a-container
ENTRYPOINT ["pipenv", "run", "python", "server.py", "--port=80", "--datafile=/data/transactions.json"]