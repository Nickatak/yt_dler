#syntax=docker/dockerfile:1

# Pretty modern release (Feb 18th, 2024).
FROM python:3.12.2-slim-bullseye
USER root
# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Install some basic dependencies
RUN apt-get update && apt-get install -y -q --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        libssl-dev \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Install ffmpeg.
RUN apt-get update -qq && apt-get install ffmpeg git -y


# At some point, we should use a normal user.  TODO: Implement user.
# Install nvm.
ENV NVM_DIR /root/.nvm
# Fine until Oct 2026.
ENV NODE_VERSION 20.11.1
RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default


RUN mkdir /app
WORKDIR /app

#Install Python requirements.
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install --upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git"

# All our app files.
COPY . /app
# For starting the celery worker.
COPY --chmod=765 ./scripts /app/scripts

# Build our frontend
RUN /app/scripts/build_fe

# We want debug on for now.
ENV FLASK_DEBUG 1
ENV FLASK_APP app
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 4000

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "4000", "--debug"]

#CMD ["gunicorn", "-b", "0.0.0.0:4000", "app:create_app()"]
