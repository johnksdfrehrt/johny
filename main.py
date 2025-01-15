from flask import Flask, Response
import cv2

app = Flask(__name__)

# Initialize the cameras
cameras = [cv2.VideoCapture(i) for i in range(10)]  # Adjust the range based on the number of cameras

def generate_frames(camera):
    while True:
        success, frame = camera.read()  # Read the camera frame
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed/<int:camera_id>')
def video_feed(camera_id):
    return Response(generate_frames(cameras[camera_id]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<h1>Camera Feeds</h1>" + "".join(
        f"<h2>Camera {i}</h2><img src='/video_feed/{i}'>" for i in range(len(cameras))
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
