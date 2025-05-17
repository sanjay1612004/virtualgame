import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key

# Initialize video capture and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.7, maxHands=2)
keyboard = Controller()

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture video frame.")
        break

    hands, img = detector.findHands(img)

    # Movement flags
    move_up, move_down, move_left, move_right = False, False, False, False

    # Check if exactly two hands are detected
    if len(hands) == 2:
        # Identify left and right hands
        left_hand = None
        right_hand = None
        for hand in hands:
            if hand["type"] == "Left":
                left_hand = hand
            elif hand["type"] == "Right":
                right_hand = hand

        if left_hand and right_hand:
            fingers_left = detector.fingersUp(left_hand)
            fingers_right = detector.fingersUp(right_hand)

            # Interpret gestures
            if fingers_left == [1, 1, 1, 1, 1] and fingers_right == [1, 1, 1, 1, 1]:
                move_up = True
            elif fingers_left == [0, 0, 0, 0, 0] and fingers_right == [0, 0, 0, 0, 0]:
                move_down = True
            elif fingers_left == [0, 0, 0, 0, 0] and fingers_right == [1, 1, 1, 1, 1]:
                move_right = True
            elif fingers_left == [1, 1, 1, 1, 1] and fingers_right == [0, 0, 0, 0, 0]:
                move_left = True

    # Release all keys before applying new input
    keyboard.release(Key.up)
    keyboard.release(Key.down)
    keyboard.release(Key.left)
    keyboard.release(Key.right)

    # Apply detected movement
    if move_up:
        keyboard.press(Key.up)
    if move_down:
        keyboard.press(Key.down)
    if move_left:
        keyboard.press(Key.left)
    if move_right:
        keyboard.press(Key.right)

    # Show the webcam feed with hand annotations
    cv2.imshow("Virtual Game Controller", img)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
