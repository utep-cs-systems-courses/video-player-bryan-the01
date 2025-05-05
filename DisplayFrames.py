#!/usr/bin/env python3

import cv2
import time
import threading

def display_frames(buffer2, full2, empty2, mutex2, frame_delay=42):
    count = 0

    print("[DISPLAY] Thread started.")
    
    while True:
        
        # Wait for output buffer to be free, lock it, pop frame
        # release lock (for ConvertToGrayscale.py)
        full2.acquire()
        mutex2.acquire()
        frame = buffer2.pop(0)
        mutex2.release()
        empty2.release()

        # If frame is None (end of stream)
        if frame is None:
            print("All frames displayed!")
            break

        # Display frame
        print(f"[DISPLAY] Showing frame {count}")
        count += 1
        cv2.imshow("Video", frame)
        if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
            break

    # cleanup
    cv2.destroyAllWindows()
