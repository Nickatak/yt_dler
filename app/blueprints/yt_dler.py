from celery.result import AsyncResult
from flask import Blueprint, render_template, request, send_file

from app.forms.yt_dler import YoutubeURLForm
from app.tasks.yt_dler import download_video

# from flask_login import login_required

yt_dler = Blueprint("yt_dler", __file__)


@yt_dler.route("/", methods=["GET", "POST"])
def start_upload():
    """Handles rendering of the home page/starting a new download.

    When a GET request is sent, this route acts like a standard
    server-side rendering route and simply returns ta template.  If
    a POST request is sent, this route will start a celery Task and
    then return JSON.  It should be noted that there's JS client-side
    that sends POST requests (not just a basic form submit).

    returns:
        :JSON: - An object with the newly generated Task ID on POST request.
        :String: - A rendered template on GET request.
    """
    form = YoutubeURLForm()

    if form.validate_on_submit():
        res = download_video.delay(form.yt_url.data)

        return {"success": True, "task_id": res.id}
    elif request.method == "POST":
        return {
            "success": False,
        }
    return render_template("yt_dler/upload.html", form=form)


@yt_dler.route("/status/<id>")
def get_status(id):
    """Fetches a task status given a Task ID.

    When a GET response is sent to this route, including a valid
    Task ID, we'll fetch the corresponding Task from celery and return
    some information about its state.  On completion of a download, the
    client-side JS should stop repeatedy requesting, but we need to send
    back the original filename, so that way it can be renamed for download
    in the browser.

    Args:
        :id: String - A valid task ID, it should be an auto-generated UUID4 from
        celery.

    returns:
        :JSON: - An object with the a ready boolean, a state-name string, and if
        the Task has completed, a completed filename for our JS script.
    """
    result = AsyncResult(id)

    return {
        "ready": result.ready(),
        "state": result.state,
        "filename": result.result["orig_name"] if result.ready() else None,
    }


@yt_dler.route("/file/<task_id>")
def get_file(task_id):
    """Gets a file from a Task.

    On-disk the Task will save the downloaded video with the same name as the Task's
    ID.  We can simply lookup the file in our temp directory, and then send it back as
    a blob.

    returns:
        :Blob: - A binary blob of the on-disk file with the same Task ID.
    """
    result = AsyncResult(task_id)

    return send_file(
        result.result["file_path"],
        as_attachment=True,
    )
