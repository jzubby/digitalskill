FROM python:buster
# set Home Dir
ENV HOME=/digital_skill
# set environment variables, stop generation of pyc in container and write prints to stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir $HOME
WORKDIR  $HOME
RUN apt-get update && apt-get install -y --no-install-recommends python3-dev build-essential
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["/bin/bash"]