import cv2
import mediapipe as mp

# MediaPipe Initialisierung
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
            
            # Spiegeln des Frames
            frame = cv2.flip(frame, 1)
            
            # Umwandlung in RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Hand Detection ausführen
            hands_results = hands.process(frame_rgb)
            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    # Bestimme die Positionen von Handgelenk, Daumen und Zeigefinger
                    wrist_x = hand_landmarks.landmark[0].x
                    thumb_x = hand_landmarks.landmark[4].x
                    index_x = hand_landmarks.landmark[8].x

                    # Unterscheide zwischen linker und rechter Hand
                    if wrist_x < 0.5:
                        hand_side = "links"
                    else:
                        hand_side = "rechts"

                    # Verwende die Position des Handgelenks als Referenzpunkt für die Unterscheidung zwischen Handfläche und Handrücken
                    if hand_side == "links":
                        if thumb_x < index_x and thumb_x < wrist_x:
                            hand_label = "Handflaeche"
                        else:
                            hand_label = "Handruecken"
                    else:
                        if thumb_x > index_x and thumb_x > wrist_x:
                            hand_label = "Handflaeche"
                        else:
                            hand_label = "Handruecken"

                    # Visualisierung der Hand
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    cv2.putText(frame, hand_side + " " + hand_label, (int(wrist_x * frame.shape[1]), int(hand_landmarks.landmark[0].y * frame.shape[0]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    # Prüfung, ob die Hand nach unten zeigt
                    wrist = hand_landmarks.landmark[0]
                    index_tip = hand_landmarks.landmark[8]
                    hand_points_down = index_tip.y > wrist.y

                    if hand_points_down:
                        text = hand_side.capitalize() + " Hand zeigt nach unten"
                        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Pose Detection ausführen
            pose_results = pose.process(frame_rgb)
            if pose_results.pose_landmarks:
                # Visualisierung des Körpers
                mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.imshow('Combined Detection', frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


