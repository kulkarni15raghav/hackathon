import streamlit as st
from streamlit_webrtc import WebRtcMode,webrtc_streamer
import cv2
import av
import time
from collections import Counter 

st.set_page_config(initial_sidebar_state="collapsed",layout = "centered")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX
#iniciate id counter
id = 0
# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Raghav', 'Sameer', 'Ilza', 'Z', 'W'] 

columns = st.columns([1,1,1])
with columns[0]:
     start_button = st.button('Start')

with columns[2]:     
    stop_button = st.button('Stop')
frame_placeholder = st.empty()

def main():
        
        cam = cv2.VideoCapture(0)
        cam.set(3, 960) # set video widht
        cam.set(4, 720) # set video height

        # Define min window size to be recognized as a face
        minW = 0.01*cam.get(3)
        minH = 0.01*cam.get(4)

        result = []

        while stop_button == False :

            ret, img =cam.read()
            img = cv2.flip(img, 1) # Flip vertically

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.7,
                minNeighbors = 10,
                minSize = (int(minW), int(minH)),
            )

            for(x,y,w,h) in faces:


                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 70):
                    id = names[id]
                    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
                    confidence = "  {0}%".format(round(100 - confidence))
                
                result.append(id)

                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
                
                print(len(result))

                     

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(img)
        else:
            print("\n [INFO] Exiting Program and cleanup stuff")
            cam.release()
            cv2.destroyAllWindows() 

        count = Counter(result)
        result_id = count.most_common()[0][0]

        if result_id == 'unknown':
             print(f"In unknown {id}")

        else:
            print(f"Not In unknown {id}")

             




if start_button:
     main()  

# class webrtc:
#     def __init__(self):
#         playing = st.checkbox("Playing", value=True)
#         webrtc_streamer(
#                 key="stream",
#                 desired_playing_state=playing ,
#                 video_processor_factory=FaceRecognition)
        
#    webrtc()
if __name__ =='__main__':
     main()



