import os


# ✅ Completely hide TensorFlow Lite + MediaPipe backend logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'



from flask import Flask, render_template, Response, jsonify
import cv2
from gesture_controller import detect_gestures, get_brightness

app = Flask(__name__)

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

@app.route('/')
def index():
    return render_template('index.html')  # Your HTML page to show webcam + gesture info

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            success, frame = cap.read()
            if not success:
                print("❌ Failed to read frame.")
                break

            try:
                # Process gestures and brightness
                frame = detect_gestures(frame)
                get_brightness(frame)
            except Exception as e:
                print(f"❌ Error in processing frame: {e}")
                continue

            # Encode frame as JPEG and stream
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    # API for JS to get gesture & brightness
    return jsonify({
        'gesture': getattr(detect_gestures, 'last_gesture', 'None'),
        'brightness': getattr(get_brightness, 'last_brightness', 0)
    })

if __name__ == '__main__':
    app.run(debug=True)
