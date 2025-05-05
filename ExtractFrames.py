#!/usr/bin/env python3

import cv2
import os
import threading


def extract_frames(clipFileName, buffer, empty, full, mutex, max_frames=72):
    count = 0
    vidcap = cv2.VideoCapture(clipFileName)

    # Read first frame
    data, frame = vidcap.read()
    print("[Extract] Thread started.")
    while data and count < max_frames:

        # Wait for input buffer, and lock empty mutex
        empty.acquire()
        mutex.acquire()

        # Push frame into shared buffer
        buffer.append(frame)
        print(f'Extracting frame {count}')

        # Unlock buffer, and release full semaphore (for ConvertToGrayscale.py)
        mutex.release()
        full.release()

        # Read frames until None
        count += 1
        data, frame = vidcap.read()

    vidcap.release()
    print('[Extractor] Done extracting frames')

    # Last acquire/release for end of stream frame
    empty.acquire()
    mutex.acquire()
    buffer.append(None)
    mutex.release()
    full.release()
