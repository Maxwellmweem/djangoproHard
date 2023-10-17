const startCameraButton = document.getElementById('startCamera');
const cameraFeed = document.getElementById('cameraFeed');
const faceCanvas = document.getElementById('faceCanvas');
const captureFaceButton = document.getElementById('captureFace');

let mediaStream = null;

startCameraButton.addEventListener('click', async function() {
    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
        cameraFeed.srcObject = mediaStream;
    } catch (error) {
        console.error('Error accessing camera:', error);
    }
});

captureFaceButton.addEventListener('click', function() {
    if (!mediaStream) return;

    // Capture a frame from the camera and draw it on the canvas
    const context = faceCanvas.getContext('2d');
    context.drawImage(cameraFeed, 0, 0, faceCanvas.width, faceCanvas.height);

    // Convert the canvas content to a data URL (base64 encoded image)
    const capturedFaceData = faceCanvas.toDataURL('image/jpeg');

    // Set the captured data as a value in a hidden input field
    const capturedFaceDataInput = document.getElementById('capturedFaceData');
    capturedFaceDataInput.value = capturedFaceData;

    // Optionally, display the captured image on the page
    const capturedImageElement = document.getElementById('capturedImage');
    capturedImageElement.src = capturedFaceData;
});




