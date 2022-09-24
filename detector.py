from statistics import mean
import cv2
import numpy as np
cap = cv2.VideoCapture(0)


sumaAzul = 0
cantAzul = 0
azulBajo = np.array([100,100,20], np.uint8)
azulAlto = np.array([125,255,255], np.uint8)

verdeBajo = np.array([36, 100, 20], np.uint8)
verdeAlto = np.array([70, 255, 255], np.uint8)



while True:
  ret, frame = cap.read()
  if ret==True:
    frame = cv2.flip(frame,1)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)
    maskVerde = cv2.inRange(frameHSV, verdeBajo, verdeAlto)
    canny = cv2.Canny(maskAzul, 10,150)
        #Se aplica transformaciones morfologicas para poder mejorar la imagen binaria obtenida
    canny = cv2.dilate(canny,None,iterations=1)
    canny = cv2.erode(canny,None,iterations=1)


    cAzul,_ = cv2.findContours(canny, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    cVerde,_ = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 



    for c in cAzul:
        area = cv2.contourArea(c)
        if area > 2000:
            M = cv2.moments(c)
            if (M["m00"] == 0): M["m00"]=1
            x = int(M["m10"]/M["m00"]) #Getting the x coordinate
            y = int((M["m01"] / M["m00"])) 
            cv2.circle(frame, (x,y), 7, (0,255,0), -1) 
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, '{},{}'.format(x,y),(x+50,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)#Mostrar ubicación en la pantalla

            # epsilon = 0.01*cv2.arcLength(c,True)
            # approx = cv2.approxPolyDP(c,epsilon,True)
            # x, y, w, h = cv2.boundingRect(c)

            

            # cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2) 
          
            # print(len(approx))
            # sumaAzul+=len(approx)
            # cantAzul+=1

            # promedio = sumaAzul/cantAzul
   
       
 
            # cv2.putText(frame,  ' Azul',(x,y-5),1,1.2,(0,255,0),2)


    for c in cVerde:
        area = cv2.contourArea(c)
        if area > 2000:
            x, y, w, h = cv2.boundingRect(c)
            M = cv2.moments(c)
            if (M["m00"] == 0): M["m00"]=1
            x = int(M["m10"]/M["m00"]) #Getting the x coordinate
            y = int((M["m01"] / M["m00"])) 
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, '{},{}'.format(x,y),(x,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
            cv2.putText(frame, ' Verde',(x,y-5),1,1.2,(0,255,0),2)

    cv2.imshow('frame', frame)
    #cv2.imshow('maskAzul', maskAzul)
    #cv2.imshow('maskVerde', maskVerde)
    if cv2.waitKey(1) & 0xFF == ord('s'):
      break
cap.release()
cv2.destroyAllWindows()