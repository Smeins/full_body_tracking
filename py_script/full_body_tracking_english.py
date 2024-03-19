import cv2
import mediapipe as mp

# start mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose

def main():
    cap = cv2.VideoCapture(0)
    
    with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands, \
         mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Couldn't read frame")
                break
            
            # Flip the frame
            frame = cv2.flip(frame, 1)
            
            # Uchange into RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Start hand detection
            hands_results = hands.process(frame_rgb)
            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    # Get the position of hand, thumb and other fingers
                    wrist_x = hand_landmarks.landmark[0].x
                    thumb_x = hand_landmarks.landmark[4].x
                    index_x = hand_landmarks.landmark[8].x

                    # Left or right hand
                    if wrist_x < 0.5:
                        hand_side = "left"
                    else:
                        hand_side = "right"

                    # Diffrence between the front and back view of the hand. using the points of the hand
                    if hand_side == "links":
                        if thumb_x < index_x and thumb_x < wrist_x:
                            hand_label = "back hand"
                        else:
                            hand_label = "Front hand"
                    else:
                        if thumb_x > index_x and thumb_x > wrist_x:
                            hand_label = "Back hand"
                        else:
                            hand_label = "Front hand"

                    # Drawing the hand
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    cv2.putText(frame, hand_side + " " + hand_label, (int(wrist_x * frame.shape[1]), int(hand_landmarks.landmark[0].y * frame.shape[0]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    # checking if the hand points down
                    wrist = hand_landmarks.landmark[0]
                    index_tip = hand_landmarks.landmark[8]
                    hand_points_down = index_tip.y > wrist.y

                    if hand_points_down:
                        text = hand_side.capitalize() + "Hand is looking down"
                        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Start Pose Detection 
            pose_results = pose.process(frame_rgb)
            if pose_results.pose_landmarks:
                # Drawing the body
                mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.imshow('Combined Detection', frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
