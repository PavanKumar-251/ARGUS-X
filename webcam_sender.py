
import cv2
import socket
import struct
import numpy as np
import threading
import time

HOST = "0.0.0.0"
PORT = 5000

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 15)

latest_frame = None
running = True

def capture_camera():
    global latest_frame, running

    while running:
        ret, frame = camera.read()

        if ret:
            latest_frame = cv2.resize(frame, (640, 480))
        else:
            time.sleep(0.02)

thread = threading.Thread(target=capture_camera, daemon=True)
thread.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print("ARGUS-X OPTIMIZED WEBCAM SENDER READY")

conn = None

try:
    conn, address = server.accept()
    print("Kali connected:", address)

    while True:
        if latest_frame is None:
            continue

        frame = latest_frame.copy()

        success, encoded = cv2.imencode(
            ".jpg",
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 65]
        )

        if not success:
            continue

        message = encoded.tobytes()
        packet = struct.pack("!I", len(message)) + message

        conn.sendall(packet)
        time.sleep(0.08)

except (ConnectionError, OSError):
    print("Kali receiver disconnected")

finally:
    running = False
    camera.release()

    if conn:
        conn.close()

    server.close()
    print("Webcam sender stopped")
