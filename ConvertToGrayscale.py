#!/usr/bin/env python3

import cv2
import threading

def convert_to_grayscale(buffer1, full1, empty1, mutex1, buffer2, full2, empty2, mutex2):
    count = 0
    print("[Grayscale] Thread started.")
    
    while True:

        # Wait for frame in input buffer, lock full1  mutex
        full1.acquire() 
        mutex1.acquire()

        # pop frame, release empty mutex (for ExtractFrames.py)
        frame = buffer1.pop(0)
        mutex1.release()
        empty1.release()

        # If case for end of stream, append None to output buffer
        if frame is None:
            print("All frames converted to grayscale")
            empty2.acquire()
            mutex2.acquire()
            buffer2.append(None)
            mutex2.release()
            full2.release()
            break

        # convert to grayscale
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print(f"Converted frame {count} to grayscale")
        count += 1

        # Wait for space in output buffer, lock mutex, append frame
        # release full2 (for DisplayFrames.py)
        empty2.acquire()
        mutex2.acquire()
        buffer2.append(grayscale_frame)
        mutex2.release()
        full2.release()


    
    
