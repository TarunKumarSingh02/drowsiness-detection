# 👁 DrowseGuard — Driver Drowsiness Detection System

> A real-time computer vision system that monitors drivers for signs of drowsiness using facial landmark analysis and Eye Aspect Ratio (EAR) computation — before fatigue turns fatal.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square) ![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey?style=flat-square) ![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green?style=flat-square) ![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-orange?style=flat-square)

---

## 🧠 Problem Statement

Drowsy driving is one of the leading causes of road fatalities worldwide. In India alone, fatigue-related accidents account for thousands of deaths annually. Unlike drunk driving, drowsiness is silent and hard to self-detect.

**DrowseGuard** uses computer vision to continuously monitor a driver's eyes in real time and raises an alert the moment signs of drowsiness are detected — giving drivers time to pull over safely.

---

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 🎥 **Real-time webcam monitoring** | Continuous live feed with overlay annotations. |
| 📐 **EAR-based detection** | Eye Aspect Ratio computed from 12 facial landmarks. |
| ⚠️ **Drowsiness alerts** | Visual + on-screen warning when eyes close for 20+ frames. |
| 🖼️ **Image upload testing** | Test detection on a static photo via the web UI. |
| 💻 **CLI mode** | Run headlessly on video files from the command line. |
| 📊 **Session statistics** | Tracks blink count, alert count, session timer, and EAR gauge. |
| 🔄 **Fallback mode** | Uses OpenCV Haar cascades if MediaPipe is unavailable. |

---

## 🛠️ Tech Stack

*   **Python 3.10**
*   **MediaPipe**: Utilized for Face Mesh to achieve 468-point facial landmark detection.
*   **OpenCV**: Handles frame capture, visual annotation, and Haar cascade fallback.
*   **Flask**: Acts as a lightweight web server and REST API.
*   **NumPy**: Powers the EAR computation via Euclidean distance.

---

## 📁 Project Structure

```text
drowsiness-detection/
│
├── app.py                  # Flask web application (main entry point)
├── cli.py                  # Command-line interface for video/webcam
├── requirements.txt        # Python dependencies
│
├── utils/
│   ├── __init__.py
│   └── detector.py         # Core DrowsinessDetector class (EAR logic)
│
└── templates/
    └── index.html          # Web UI (dark dashboard)


    ⚙️ Setup & Installation
Prerequisites
Python 3.8–3.11 (Required for MediaPipe compatibility).

A working webcam (for live mode).

pip package manager.

Installation Steps
Clone the repository:

Bash


git clone [https://github.com/alphabetaheisenberg/drowsiness-detection.git](https://github.com/alphabetaheisenberg/drowsiness-detection.git)
cd drowsiness-detection
Create and activate a virtual environment (recommended):

Bash


python -m venv venv

# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
Install dependencies:

Bash


pip install -r requirements.txt
Note: If MediaPipe fails to import with AttributeError: module 'mediapipe' has no attribute 'solutions', this is a known issue with newer releases. This project pins mediapipe==0.10.14, which is a stable version confirmed to work.

🚀 Usage Guide
Option A: Web App (Recommended)
Start the application by running:

Bash


python app.py
Then open your browser and navigate to http://localhost:5000.

Note for WSL / VM users: If localhost doesn't resolve, run python app.py --host 0.0.0.0 and visit http://127.0.0.1:5000.

Dashboard Highlights:

Live webcam feed with facial landmark overlay.

Real-time EAR gauge and driver status.

Event log displaying blinks and drowsy events.

Upload tab to test the model on a static image.

Option B: Command Line Interface
Bash


# Use default webcam
python cli.py

# Use a specific video file
python cli.py --source path/to/video.mp4

# Save annotated output
python cli.py --source path/to/video.mp4 --output result.mp4

# Run headless (no display window, prints stats to terminal)
python cli.py --no-display
🔬 How It Works
Eye Aspect Ratio (EAR)
EAR is a scalar value that measures how open the eye is, computed from 6 landmarks per eye:

EAR = (‖p2 - p6‖ + ‖p3 - p5‖) / (2 × ‖p1 - p4‖)

Where p1 through p6 represent the six 2D eye landmark coordinates.

EAR ≥ 0.3: Eye is open (Awake).

EAR < 0.25: Eye is closing (Potential drowsiness).

EAR < 0.25 for 20+ consecutive frames: DROWSY — Alert triggered.

Processing Pipeline
Capture Frame: Read input from the webcam stream.

Landmark Detection: Apply MediaPipe Face Mesh to extract 468 landmarks.

Eye Isolation: Extract the 6 left-eye and 6 right-eye landmarks.

Compute EAR: Calculate the EAR for each eye and average the results.

Evaluate: Check if the average EAR drops below the 0.25 threshold.

Trigger Alert: If the threshold is breached for 20+ frames, trigger the drowsiness alarm.

📸 Screenshots
Run the application and visit http://localhost:5000 to interact with the live dashboard.

The UI includes:

Dark HUD-style camera feed with corner frame decorations.

Real-time EAR bar gauge with a visual threshold marker.

Session stats including blinks, alerts, and total session time.

Color-coded status chips (Green = Awake, Red = Drowsy).

A scrolling event log with timestamps.

🎓 Core Concepts Applied
Concept	Application
Face Detection	MediaPipe Face Mesh and OpenCV Haar Cascades.
Facial Landmarks	468-point mesh mapping, specifically isolating 12 eye landmarks.
Image Processing	Frame capture, BGR to RGB color conversion, and visual annotation.
CNNs	Deep learning backbone powering MediaPipe's landmark predictions.
Object Detection	Fallback mechanism using Haar cascade eye detection.
Real-time Processing	Continuous OpenCV VideoCapture stream loop.

⚠️ Known Limitations
Lighting: Performance is highly dependent on ambient lighting conditions; ensure good frontal illumination.

Obscuration: Strong prescription glasses or sunglasses may negatively impact landmark detection accuracy.

Thresholding: The EAR threshold of 0.25 is generalized and may require fine-tuning for specific individuals.

Compatibility: MediaPipe requires Python 3.8–3.11; users on Python 3.12+ must rely on the fallback mode.

📄 License & Credits
MIT License — free to use, modify, and distribute.

Built as a Bring Your Own Project (BYOP) capstone for a Computer Vision course, motivated by the critical need to address India's road safety crisis.