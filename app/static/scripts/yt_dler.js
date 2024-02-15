"use strict";

class YoutubeDownloader {
    constructor() {
        this.form = document.getElementById("yt_dler");
        this.button = document.getElementById("download");
        this.form.addEventListener("submit", this.onSubmitHandler);

        this.__polling_interval_id = null;
        this.__input_locked = false;

        this.csrf_token = document.getElementById("csrf_token").value;
    }

    onSubmitHandler = (e) => {
        /**
         * On-submit handler for our youtube link form.
         * 
         *      Should send a POST request to our route to start a youtube download.  After
         *      the download has started, we should retrieve the Task ID associated with the
         *      download.  We can then long-poll against our status route to determine whether
         *      the download has finished or not.  This does handle the CSRF token directly and
         *      places it in the request header.
         * 
         *      Args:
         *          :e: Object - Event Listener object.
         */
        e.preventDefault();

        if (!this.__input_locked) {
            let yt_url = this.form.querySelector("input[name='yt_url'").value;
            this.update_output("Youtube Fetching started");

            fetch('/', {
                method: "POST",
                headers: {
                    "Content-type": "application/json; charset=UTF-8",
                    "X-CSRF-Token": this.csrf_token
                },
                body: JSON.stringify({"yt_url": yt_url}),
            })
                .then(data => data.json())
                .then((data) => {
                    if (data.success) {
                        this.update_output("Downloading youtube video");
                        this.__polling_interval_id = setInterval(
                            () => {
                                this.check_status(data.task_id);
                            }, 1000
                        )
                    }
                    else {
                        this.update_output("Error, try again.", false, false);
                        this.form.querySelector(".container").classList.add("url_error");
                    }
            });
        }
    }

    check_status = (task_id) => {
        /**
         * Poll function for checking the download status.
         * 
         *      Sends GET requests to our Task status route to determine whether the download
         *      has finished or not.  When the download completes, we simply stop polling and
         *      then download the file in the browser.
         */
        fetch(`/status/${task_id}`)
            .then(data => data.json())
            .then((data => {
                if (data.ready) {
                    clearInterval(this.__polling_interval_id);
                    this.update_output("Download.", false, false);
                    this.download_file(task_id, data.filename);
                }
            }))
    }

    download_file(task_id, filename) {
        /**
         * Downloads the file.
         * 
         *      This sends a GET request to our file-fetch route and then uses a pretty disguting
         *      trick.  It makes an invisible link, and then automates the click after assigning the
         *      download properties and the URL to the actual file blob we received back from our server.
         * 
         *      Args:
         *          :task_id: String - The UUID4 ID of our Task to download the video.
         *          :filename: String - The filename of the video (used to set the download filename).
         */
        fetch(`/file/${task_id}`)
            .then(res=> res.blob())
            .then(blob=>{
                let url = URL.createObjectURL(blob);
                let link = document.createElement("a");
                link.href = url;
                link.style.display = "none";
                link.download = filename;

                // Attach and click.
                document.body.appendChild(link);
                link.click();

                // Cleanup.
                URL.revokeObjectURL(url);
                document.body.removeChild(link);
                this.input_locked = false;

            }).catch(err=>console.log(err));
    }

    update_output = (message, animate_text = true, lock_state = true) => {
        /**
         * Sets the text inside the download button and updates the UI-locked flag.
         * 
         *      Args:
         *          :message: String - The string message to set.
         *          :animate_text: Boolean - Whether or not to animate the ellipsis in the button
         *          text.  If this is omitted, then the text will be animated.
         *          :lock_state: Boolean - the state to set the UI-locked flag to. If this is omitted
         *          then the state will be locked.

         */
        this.__lock_state = lock_state;
        if (lock_state) {
            this.button.classList.add("locked");
        } else {
            this.button.classList.remove("locked");
        }
        if (animate_text) {
            this.button.classList.add("loading");
        } else {
            this.button.classList.remove("loading");
        }

        this.button.innerText = message;
    }
}

// Put this back inside the onload later after debugging.
let downloader = null;

window.onload = () => {
    downloader = new YoutubeDownloader();
}



