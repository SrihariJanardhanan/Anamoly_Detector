document.addEventListener("DOMContentLoaded", function () {
    const videoInput = document.getElementById("video-input");
    const videoPlayer = document.getElementById("video-player");
    const predictButton = document.getElementById("predict-button");
    const submitButton = document.getElementById("submit-button");

    videoInput.addEventListener("change", function (event) {
        const selectedVideo = event.target.files[0];
        if (selectedVideo) {
            submitButton.click();
            const videoURL = URL.createObjectURL(selectedVideo);
            videoPlayer.src = videoURL;
            videoPlayer.style.display = "block";
            predictButton.style.display = 'inline-block';
        }
    });

    function predict() {
        // Replace with your code to send a notification or alert
        alert('entered predict!')
        data = {
            filename: "{{video_filename}}"
        }

        options = {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'post',
            body: JSON.stringify(data)
        }

        url = 'http://127.0.0.1:5000/predict'

        fetch(url, options).then(
            res => res.json()
        ).then(
            res => {
                if (res['output'] == 'Anomaly') {
                    alert("Alert🚨🚨🚨 Anomaly Detected🚨🚨🚨")
                }
            }
        ).catch(err => console.log(err))
    }

})

