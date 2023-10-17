document.addEventListener("DOMContentLoaded", function () {
    const videoElement = document.getElementById("camera-feed");
    const faceSquare = document.getElementById("face-square");
    const captureButton = document.getElementById("capture-button");
    const capturedFaceInput = document.getElementById("captured-face");

    // Initialize camera feed
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
            .getUserMedia({ video: true })
            .then(function (stream) {
                videoElement.srcObject = stream;
            })
            .catch(function (error) {
                console.log("Error accessing the camera: " + error);
            });
    }

    // Capture image when the "Capture" button is clicked
    captureButton.addEventListener("click", function () {
        const canvas = document.createElement("canvas");
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

        // Draw face detection square on the captured image
        faceSquare.classList.remove("hidden");
        faceSquare.style.width = "150px"; // Adjust the size as needed
        faceSquare.style.height = "150px"; // Adjust the size as needed
        faceSquare.style.left = "50%"; // Center horizontally
        faceSquare.style.top = "50%"; // Center vertically
        faceSquare.style.transform = "translate(-50%, -50%)"; // Center the square

        // Convert the canvas content to a data URL
        const capturedImage = canvas.toDataURL("image/jpeg");

        // Set the data URL as the value of the captured_face input
        capturedFaceInput.value = capturedImage;

        // Disable the "Capture" button after capturing
        captureButton.disabled = true;
    });
});
