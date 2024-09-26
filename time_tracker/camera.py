import cv2

# Open your computer's default camera device.
camera = cv2.VideoCapture(0)

# Define the codec and create a VideoWriter object to write the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# You may want to adjust the frame size (640, 480) according to your camera's default resolution
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

while True:
    success, img = camera.read()
    if success:
        # Write the frame into the file 'output.mp4'
        out.write(img)

        # Show the frame
        cv2.imshow('Video', img)
    else:
        break

    # Exit on 'q' key press
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

# Release everything when job is finished
camera.release()
out.release()
cv2.destroyAllWindows()
