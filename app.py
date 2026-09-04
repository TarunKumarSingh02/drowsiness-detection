import cv2
import numpy as np
import base64
import time
from flask import Flask, render_template, Response, jsonify, request
from utils.detector import DrowsinessDetector

app = Flask(__name__)
detector = DrowsinessDetector()

# Global state
state = {
    "drowsy_count": 0,
    "alert_count": 0,
    "session_start": time.time(),
    "status": "Awake",
    "ear": 0.0,
    "blinks": 0,
}

def generate_frames():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, frame = cap.read()
        if not success:
            break

        result = detector.process_frame(frame)
        annotated = result["frame"]
        state["status"] = result["status"]
        state["ear"] = round(result["ear"], 3)
        state["blinks"] = result["blinks"]
        if result["status"] == "DROWSY":
            state["drowsy_count"] += 1
            if state["drowsy_count"] % 30 == 0:
                state["alert_count"] += 1

        ret, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stats')
def stats():
    elapsed = int(time.time() - state["session_start"])
    mins, secs = divmod(elapsed, 60)
    return jsonify({
        "status": state["status"],
        "ear": state["ear"],
        "blinks": state["blinks"],
        "alerts": state["alert_count"],
        "session_time": f"{mins:02d}:{secs:02d}"
    })

@app.route('/reset', methods=['POST'])
def reset():
    state["drowsy_count"] = 0
    state["alert_count"] = 0
    state["session_start"] = time.time()
    state["blinks"] = 0
    detector.reset()
    return jsonify({"success": True})

@app.route('/upload', methods=['POST'])
def upload():
    """Process uploaded image for drowsiness detection."""
    file = request.files.get('image')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    npimg = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    result = detector.process_frame(frame)

    _, buffer = cv2.imencode('.jpg', result["frame"])
    encoded = base64.b64encode(buffer).decode('utf-8')

    return jsonify({
        "image": f"data:image/jpeg;base64,{encoded}",
        "status": result["status"],
        "ear": round(result["ear"], 3),
        "blinks": result["blinks"]
    })


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    args, _ = parser.parse_known_args()
    app.run(debug=True, port=5000, host=args.host)