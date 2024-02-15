#syntax=docker/dockerfile:1

# Pretty modern release (Feb 18th, 2024).
FROM python:3.12.2-slim-bullseye

RUN apt-get update -qq && apt-get install ffmpeg git -y

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -r requirements.txt
RUN pip install --upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git"
COPY . /app
# For starting the celery worker.
COPY --chmod=765 ./compose /app/compose

# We want debug on for now.
ENV FLASK_DEBUG 1
ENV FLASK_APP app
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 4000

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "4000", "--debug"]

#CMD ["gunicorn", "-b", "0.0.0.0:4000", "app:create_app()"]
