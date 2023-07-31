FROM python:3.9-alpine

WORKDIR /app

RUN python3 -m pip install --upgrade requests

COPY sessionSimulator.py sessionSimulator.py

CMD ["python3", "sessionSimulator.py"]
