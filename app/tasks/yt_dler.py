import pathlib
import time

from celery import shared_task
from flask import current_app
from youtube_dl import YoutubeDL


@shared_task(bind=True, ignore_result=False)
def download_video(self, url):
    """A celery task to download a video from youtube.

    We save the video in the temp folder as `{task_id}.mp4`.  Upon completion, we
    should have access to both the file_path (named as the Task ID) as well as the
    original video name from youtube.  The original name is only used on the front-end
    at the final step when we download with our JS directly.

    returns:
        :Dict: - Dictionary containing the downloaded file's path in the temp dir as well
        as the original video name.  This dictionary won't be available as `task.result`
        until `task.ready()` is `True`.
    """

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": f"{current_app.config['TEMP_DIR']}/{self.request.id}.%(ext)s",
    }
    with YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
        ydl.download([url])

    # cleanup_file.delay(file_path, 0.25) # Change this later. this isn't working with pathlib
    return {
        "file_path": str(
            pathlib.Path(
                current_app.config["TEMP_DIR"], f'{self.request.id}.{meta["ext"]}'
            )
        ),
        "orig_name": f'{meta["title"]}.{meta["ext"]}',
    }


@shared_task()
def cleanup_file(path, mins_delay):
    time.sleep(mins_delay * 60)
