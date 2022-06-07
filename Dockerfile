# TODO: rewrite the docker file -> https://stackoverflow.com/questions/46245844/pass-arguments-to-python-argparse-within-docker-container

FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#WORKDIR /root/app
WORKDIR /app

# Install python dependencies
COPY app/requirements.txt ./
RUN pip install --no-cache-dir --no-cache --no-input --disable-pip-version-check -r requirements.txt

# Copy sourcecode into docker image
COPY app/ ./

ENTRYPOINT ["python", "main.py"]
