import cv2 as cv
import time

# setup
fourcc = cv.VideoWriter_fourcc(*"XVID")
FRAMERATE = 15

print("Checking for camera...")
capture = cv.VideoCapture(0)


# check if it worked
if not capture.isOpened():
    print("! Cannot find/open camera")
    exit()

print("Camera found.")
# mode select
while ((mode := input("\nSelect mode: \n" +
             "------------- \n" +
             "v = Video \n" +
             "p = Photo \n" +
             "r = Record \n" +
             " -> ")) not in ["v", "p", "r"]): pass
print("\nEsc to exit")
if (mode == "v"):
    print("Spacebar to freeze for 3s")
elif (mode == "p"):
    print("Spacebar to display frame")
elif (mode == "r"):
    print("Spacebar to record for 3s")

cv.namedWindow("capture")
success = True
while success:
    if (mode == "v"):
        # read and show frame
        success, frame = capture.read()
        cv.imshow("capture", frame)
        # check for interrupt
        key = cv.waitKey(25)
        if key == 27: # Esc
            print("! Keyboard stop")
            break
        elif key == 32: # Spacebar
            print("3-second freeze frame")
            time.sleep(3)
    elif (mode == "p"):
        # check for interrupt
        key = cv.waitKey(25)
        if key == 27: # Esc
            print("! Keyboard stop")
            break
        elif key == 32: # Spacebar
            # read and show frame
            print("Display frame")
            success, frame = capture.read()
            cv.imshow("capture", frame)
    elif (mode == "r"):
        rec = False
        while (True):
            # read and show frame
            success, frame = capture.read()
            cv.imshow("capture", frame)
            # check for interrupt
            key = cv.waitKey(25)
            if key == 27: # Esc
                print("! Keyboard stop")
                break
            elif key == 32: # Spacebar
                print("Recording for 3s")
                rec = True
                break
        if (rec == False): break
        out = cv.VideoWriter("output.avi", fourcc, FRAMERATE, (640, 480))
        end_time = time.time() + 5
        frame_time = time.time()
        while (rec and time.time() < end_time):
            # read, write, and show grey frame
            success, frame = capture.read()
            if (time.time() > frame_time):
                out.write(frame)
                frame_time = time.time() + 1/FRAMERATE - 0.021
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            cv.imshow("capture", frame)
        out.release()
        print("Recorded")
            
capture.release()
cv.destroyWindow("capture")
