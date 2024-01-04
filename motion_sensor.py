def detect_motion(duration=1):
    import cv2
    import time
    camera = cv2.VideoCapture(0)
    _, baseline_frame = camera.read()
    start = time.time()
    max_motion = 0
    while (time.time() - start < duration):
        _, current_frame = camera.read()
        delta_frame = cv2.absdiff(baseline_frame, current_frame)

        # Convert the difference frame to grayscale
        # Apply Gaussian blur to reduce noise and improve motion detection
        # Threshold the blurred frame to identify areas with significant changes
        # Dilate the thresholded image to fill in small holes and gaps
        # Find contours of the dilated image

        gray_frame = cv2.cvtColor(delta_frame, cv2.COLOR_BGR2GRAY)
        blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        _, thresh_frame = cv2.threshold(blurred_frame, 20, 255, cv2.THRESH_BINARY)
        dilated_frame = cv2.dilate(thresh_frame, None, iterations=2)
        contours, _ = cv2.findContours(dilated_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check for motion
        for contour in contours:
            if cv2.contourArea(contour) > max_motion:
                max_motion = cv2.contourArea(contour)
        # Update the baseline frame for the next iteration
        baseline_frame = current_frame.copy()

    camera.release()
    return max_motion
