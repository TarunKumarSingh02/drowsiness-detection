"""
cli.py — Run drowsiness detection on a video file or webcam from the command line.

Usage:
    python cli.py --source 0                  # Webcam (default)
    python cli.py --source path/to/video.mp4  # Video file
    python cli.py --source 0 --no-display     # Headless (prints stats only)
"""

import argparse
import cv2
import time
import sys
from utils.detector import DrowsinessDetector


def run(source, display=True, output=None):
    cap = cv2.VideoCapture(int(source) if source.isdigit() else source)

    if not cap.isOpened():
        print(f"[ERROR] Cannot open source: {source}")
        sys.exit(1)

    detector = DrowsinessDetector()
    writer = None

    if output:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = cap.get(cv2.CAP_PROP_FPS) or 20
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(output, fourcc, fps, (w, h))
        print(f"[INFO] Saving output to: {output}")

    print("[INFO] Starting detection. Press 'q' to quit.")
    frame_count = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[INFO] End of stream.")
            break

        result = detector.process_frame(frame)
        frame_count += 1

        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps_actual = frame_count / elapsed
            print(f"[{elapsed:.1f}s] Status: {result['status']:8s} | EAR: {result['ear']:.3f} | "
                  f"Blinks: {result['blinks']} | FPS: {fps_actual:.1f}")

        if writer:
            writer.write(result["frame"])

        if display:
            cv2.imshow("DrowseGuard - Press Q to quit", result["frame"])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[INFO] User quit.")
                break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()

    elapsed = time.time() - start_time
    print(f"\n[SUMMARY] Processed {frame_count} frames in {elapsed:.1f}s")
    print(f"[SUMMARY] Total blinks: {result['blinks']}")
    print(f"[SUMMARY] Final status: {result['status']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DrowseGuard - Driver Drowsiness Detection CLI"
    )
    parser.add_argument(
        "--source", default="0",
        help="Video source: '0' for webcam, or path to video file (default: 0)"
    )
    parser.add_argument(
        "--no-display", action="store_true",
        help="Run headless (no OpenCV window, useful for servers)"
    )
    parser.add_argument(
        "--output", default=None,
        help="Optional path to save annotated output video (e.g., output.mp4)"
    )
    args = parser.parse_args()
    run(args.source, display=not args.no_display, output=args.output)