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

def figName(contorno,width,height):
  #se hace una aproximacion de la cantidad de lados del contorno generado
  epsilon = 0.02*cv2.arcLength(contorno,True)
  approx = cv2.approxPolyDP(contorno,epsilon,True) 

  #de acuerdo a la cantidad de lados se retorna el tipo de figura
  if len(approx) == 3:
    namefig = 'Triangulo'
  if len(approx) == 4:
    aspect_ratio = float(width)/height
    if aspect_ratio == 1:
      namefig = 'Cuadrado'
    else:
      namefig = 'Rectangulo'
  if len(approx) == 5:
    namefig = 'Pentagono'
  if len(approx) == 6:
    namefig = 'Hexagono'
  if len(approx) > 10:
    namefig = 'Circulo'

  return namefig


while True:
  ret, frame = cap.read()
  if ret==True:
    frame = cv2.flip(frame,1)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)
    maskVerde = cv2.inRange(frameHSV, verdeBajo, verdeAlto)

    cAzul,_ = cv2.findContours(maskAzul, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    cVerde,_ = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 



    for c in cAzul:
        area = cv2.contourArea(c)
        if area > 2000:
            x, y, w, h = cv2.boundingRect(c)
            epsilon = 0.03*cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,epsilon,True)
            print(len(approx))
            sumaAzul+=len(approx)
            cantAzul+=1

            promedio = sumaAzul/cantAzul
   
            if promedio > 8 and promedio <= 11:
                namefig = 'Rectangulo'
                sumaAzul = 0
            if promedio >18 and promedio <= 21:
                namefig = 'Circulo' 
                sumaAzul = 0  
            else:
                namefig  = 'NO '
       
 
            cv2.putText(frame, namefig + ' Azul',(x,y-5),1,1.2,(0,255,0),2)


    for c in cVerde:
        area = cv2.contourArea(c)
        if area > 2000:
            x, y, w, h = cv2.boundingRect(c)

            cv2.putText(frame, ' Verde',(x,y-5),1,1.2,(0,255,0),2)

    cv2.imshow('frame', frame)
    #cv2.imshow('maskAzul', maskAzul)
    #cv2.imshow('maskVerde', maskVerde)
    if cv2.waitKey(1) & 0xFF == ord('s'):
      break
cap.release()
cv2.destroyAllWindows()