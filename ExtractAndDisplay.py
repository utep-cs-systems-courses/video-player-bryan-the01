#!/usr/bin/env python3

import threading
from ExtractFrames import extract_frames
from ConvertToGrayscale import convert_to_grayscale
from DisplayFrames import display_frames

#globals
BUFFER_SIZE = 10
MAX_FRAMES = 72
CLIP_FILE = 'clip.mp4'

def main():
    print("[MAIN] Program started.")
    
    # For input buffer (between extractor and grayscale)
    buffer1 = []
    empty1 = threading.Semaphore(BUFFER_SIZE)
    full1  = threading.Semaphore(0)
    mutex1 = threading.Lock()
    
    # For output buffer (between grayscale and display)
    buffer2 = []
    empty2 = threading.Semaphore(BUFFER_SIZE)
    full2  = threading.Semaphore(0)
    mutex2 = threading.Lock()

    # Create thread for each function
    t1 = threading.Thread(target=extract_frames, args=(CLIP_FILE, buffer1, empty1, full1, mutex1, MAX_FRAMES))
    t2 = threading.Thread(target=convert_to_grayscale, args=(buffer1, full1, empty1, mutex1, buffer2, full2, empty2, mutex2))
    t3 = threading.Thread(target=display_frames, args=(buffer2, full2, empty2, mutex2))
    
    # Start frames concurrently
    t1.start()
    t2.start()
    t3.start()

    # Wait for thread 1 to finish, then thread 2, then thread 3
    t1.join()
    t2.join()
    t3.join()
    print("Threads finished successfully")

    
if __name__ == "__main__":
    main()
