'''
--------------------------------------------------------------------------
------- JUEGO PDI ARKANOID ------------------------------------------
------- Conceptos básicos de PDI ------------------------------------------
------- Por: Jonathan Valencia Sanchez  jonathana.valencia@udea.edu.co  ----
-------------Ana María Velasco          ana.velasco@udea.edu.co  ----   
-------------Estudiantes de ingenieriía electrónica UdeA  ----------------
------- Procesamiento digital de imagenes -----
------- Agosto 2022 -------------------------------------------------
--------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------
--1. Importar librerias necesarias e inicializar pygame ------------------
--------------------------------------------------------------------------
'''
import cv2
import numpy as np
import pygame, sys

pygame.init()

'''
--------------------------------------------------------------------------
--2. Iniciar variables y objetos principales -----------------------------
--------------------------------------------------------------------------
'''

size = (600,500)
#crear ventana
screen = pygame.display.set_mode(size)
#reloj para controlar FPS del juego
clock = pygame.time.Clock()

#estados iniciales del juego
start = False
pause = False
campeon = False
gameover = False
#posicion inicial de plataforma
posx=265
posy=420
x=0
y=0
#valores iniciales de disparo
bala = pygame.image.load("imgs/bala.png")
#posición inicial
pbalax = posx+50
pbalay = posy-22
mbalay = 8
cantidadBalas = 3
#condición de disparo
disparar  = False
#posicion inicial de bola
bola = pygame.image.load("imgs/bola.png")
pbx = posx+50
pby = posy-22
#velocidad de la bola
mbx = 6
mby = 6
wb,hb=22,22  #ancho y alto de la bola

#se carga la imagen de fondo
fondo = pygame.image.load("imgs/fondo_es.jpg")
#Definir colores
black = (0  ,0  ,0  )
white = (255,255,255)
blue  = (0  ,0  ,255)


#iniciamos el proceso de captura del video
cap = cv2.VideoCapture(0)


#Se determina el rango en el cual se trabajará en HSV
azulBajo = np.array([100, 100, 20], np.uint8)
azulAlto = np.array([125, 255, 255], np.uint8)
amarilloBajo = np.array([25, 100, 20], np.uint8)
amarilloAlto = np.array([35, 255, 255], np.uint8)
listaBloques=[]
player = pygame.image.load("imgs/plataforma.png")

#funcion para cargar y guardar las posiciones de cada bloque a romper
def crearCuadrados():
    #ancho y alto del bloque
    w = 64
    h = 32
    #posición inicial de la primera fila
    px  = 30
    py  = 20
    #bucle para configurar la cantidad de filas y su posición
    for i in range(3):
        ruta = "imgs/bloque_"+str(i+1)+".png"  #carga ruta de la imagen
        #bucle para configurar las columnas y su posición
        for j in range(8):
            listaBloques.append([pygame.image.load(ruta),[px,py]]) #se guarda junto con la posicion
            px += w+5
        py += h + 10
        px = 30

#funcion para mostrar bloques en pantalla
def dibujarBloques():  
    for i in listaBloques:
        screen.blit(i[0],i[1])
            
#función para detectar la colisión de la bola con la plataforma
def colisionPlataforma(bx,by,px,py):
    #Estado de colisión 
    col = False
    #delimita la zona de colisión de acuerdo a la posición de la bola y la plataforma
    if bx+18 > px and (bx+wb-11) < px+104:
        if (by + hb) >  py:
            col = True
    return col       
#función para detectar colisión de la bola con los bloques
def colisionBloques(bx,by):
    i=0 #posición del bloque dentro de la lista
    for n in listaBloques:
        l = False #Estado de colisión
        #se almacenan la posición (x, y) de cada bloque 
        xb = n[1][0]
        yb = n[1][1]
        #Zona de colisión para poder determinar con cual bloque colisionó
        if by < (yb + 32) and (bx > xb and bx < (xb+ 64)):
            l = True
            #Se elimina de la lista de bloques y se rompe el ciclo
            listaBloques.pop(i)
            break
        i+=1    
    return l

#se generan los cuadrados una unica vez
crearCuadrados()

'''
--------------------------------------------------------------------------
--3. Bucle principal del juego -------------------------------------------
--------------------------------------------------------------------------
'''

while True:
    ### ----- ZONA DETECCIÓN DE EVENTOS ----- ###
    #capturamos la imagen con la que vamos a trabajar
    ret,frame = cap.read() 
     #ret es igual a true si se esta capturando una imagen
    if ret == True:
        #se invierte la camara 
        frame=cv2.flip(frame,1)
        #se pasa de BGR a HSV
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #Se genera una mascara con lo rangos especificados para poder detectar el color
        mask = cv2.inRange(frameHSV, azulBajo, azulAlto)  #mascara color azul
        mask2=cv2.inRange(frameHSV, amarilloBajo, amarilloAlto) #mascara color amarillo
        #con la funcion findContours nos ayuda a definir los contornos del color detectado
        contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contornos2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.line(frame, [0,320], [700,320], (255,0,0), 2) 

        #Se recorre cada uno de los contornos encontrados para el color azul 
        for c in contornos:
            #determina el area en pixeles
            area = cv2.contourArea(c)
            if area > 2000:
                #se define un rectangulo de acuerdo al contorno que cumpla con el area
                x,y,w,h = cv2.boundingRect(c)
                #se dibuja el contorno de acuerdo a los valores retornados de la función anterior
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2) 
        #se recorre cada unos de los contornos encontrados para el color amarillo
        for c2 in contornos2:
            #determina el area en pixeles
            area = cv2.contourArea(c2)
            if area > 2000:
                #se define un rectangulo de acuerdo al contorno que cumpla con el area
                x2,y2,w2,h2 = cv2.boundingRect(c2)
        
                cv2.rectangle(frame,(x2,y2),(x2+w2,y2+h2),(255,255,0),2)
                #delimitar la zona donde debe detectar el color amarillo
                if x2 > 260 and x2 + w2 < 400:
                    if y2 > 175 and y2 +h2 < 275:
                        #detectar el Continue
                        if gameover or campeon:
                            #condiciones y valores de reinicio
                            pause = False
                            start = True
                            campeon = False
                            gameover = False
                            posx=265
                            posy=420
                            x=0
                            y=0
                            cantidadBalas = 3
                            pbx = posx+50
                            pby = posy-22
                            listaBloques.clear()
                            crearCuadrados()
                        #detectar el Start    
                        else:    
                            start = True
                            pause = False
                            gameover = False
                        
                        
                elif x2 > 460 and x2+w2 <600:
                    #detectar el Pause
                    if y2 > 50 and y2+h2<150:
                        pause = True
                        start = False
                    #detectar el Disparo
                    elif y2 > 200 and y2+h2<300:
                        if cantidadBalas > 0:
                            disparar = True    
                  
        ### ----- ZONA DETECCIÓN DE EVENTOS ----- ###


        ### ----- ZONA DE DIBUJO ----- ###     
        font = cv2.FONT_HERSHEY_SIMPLEX    #se define la fuente
        #condicionales para dibujar las zonas para dectectar el amarillo
        if not(start):       
            if gameover or campeon:
                cv2.rectangle(frame, (260,175) , (400,275) ,(0,255,255),2)
                cv2.putText(frame, 'Continue?',(280,230), font, 0.75,(0,255,255),2,cv2.LINE_AA)
            else:    
                cv2.rectangle(frame, (260,175) , (400,275) ,(0,255,255),2)
                cv2.putText(frame, 'Start',(295,230), font, 1,(0,255,255),3,cv2.LINE_AA)
        elif not(pause):
            cv2.rectangle(frame, (460,50) , (600,150) ,(0,255,255),2)
            cv2.putText(frame, 'Pause',(490,110), font, 0.8,(0,255,255),2,cv2.LINE_AA)

            cv2.rectangle(frame, (460,200) , (600,300) ,(0,255,255),2)
            cv2.putText(frame, 'Shoot',(480,250), font, 0.8,(0,255,255),2,cv2.LINE_AA)
       
        
        #Visualizamos el video
        cv2.imshow('frame',frame)
        #cv2.imshow('azul',mask)
        #cv2.imshow('amarillo',mask2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
 
               

    #----------------- Juego ----------------
    #añadir fondo a la ventana del juego
    screen.blit(fondo,(0,0))
    #añadir bola a la ventana del juego
    screen.blit(bola,[pbx,pby])
    #añadir bloques 
    dibujarBloques()
    ### ----- ZONA DE DIBUJO ----- ### 
    ### ----- ZONA LOGICA DEL JUEGO ----- ### 
    #se verifica si el juego ha iniciado
    if start:
        #delimita la zona en el eje x de la plataforma 
        if x < 496:
            if y > 320:
                posx = x
        #Condición para la terminación del juego por perdida
        if pby > posy:
            gameover = True 
            start = False  
        #Cambio de posición de la bola con valores constantes 
        pbx += mbx
        pby -= mby

        #Rebote de la bola en los limites del juego (izquierda - derecha)
        if pbx < 0 or pbx > size[0]-wb:
            mbx*=-1
        #Rebote de la bola en los limites del juego (abajo - arriba)        
        if pby < 0 or pby > size[1]-hb:
            mby*=-1

        #Rebote con la plataforma
        if(colisionPlataforma(pbx,pby,posx,posy)):
            mby*=-1      

        #Detectar colisión de la bola con los bloques
        a=colisionBloques(pbx,pby)

        #Condición para ganar el juego 
        if len(listaBloques) == 0:
            start = False   
            campeon = True
        #En caso de que se detecte colisión se cambia la dirección en 'y' de la bola
        if a:
            mby*=-1
        # se verifica si la condición de disparo esta activa(True)
        if disparar:
            screen.blit(bala,[pbalax,pbalay]) #Se añade la bala
            pbalay -= mbalay #Movimiento de la bala solo en dirección 'y'
            #Se dectecta la colisión con los bloques
            if colisionBloques(pbalax,pbalay):
                #Se reinicia condiciones y se disminuye la cantidad de balas disponibles 
                disparar = False
                cantidadBalas -= 1
                #se cambia la posición de la bala   
                pbalax = posx+50 
                pbalay = posy-22

        #se añade la bola principal        
        screen.blit(player,[posx,posy])
    #Se verifica si el juego esta en pausa    
    elif pause:
        #Dibujar texto de 'Pause' en pantalla del juego
        fuente = pygame.font.SysFont("arial", 40, bold=True, italic=False)
        texto = fuente.render("Pause",True,white)
        screen.blit(texto,[265,280])  
    
        screen.blit(player,[posx,posy])
        #screen.blit(black,[0,0])

    else:
        #Verifica si el jugador ha ganado
        if campeon:
            win = pygame.image.load("imgs/win2.png")
            screen.blit(win,(0,0))
           
        #Verifica si el jugador a perdido    
        elif gameover:
            fo_d = pygame.image.load("imgs/gameoverphrase.jpg")
            screen.blit(fo_d,(0,0))
        else:  
            #Se añade texto 'Start' en la pantalla de inicio 
            fuente = pygame.font.SysFont("arial", 40, bold=True, italic=False)
            texto = fuente.render("Start",True,white)
            screen.blit(texto,[265,280])  
            screen.blit(player,[posx,posy])

    #actualizar pantalla del juego a 60 FPS
    pygame.display.flip()
    clock.tick(60)
    ### ----- ZONA LOGICA DEL JUEGO ----- ###    
cap.release()
cv2.destroyAllWindows()
