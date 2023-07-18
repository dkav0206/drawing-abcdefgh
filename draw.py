import cv2 
import mediapipe as mp
from math import hypot, ceil
import numpy as np
try: 
    from cvzone.HandTrackingModule import HandDetector
    import cvzone
except:
    from HandTrackingModule import HandDetector
from pynput.keyboard import Controller
from time import sleep
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()           
drive = GoogleDrive(gauth)  


#######################
brushThickness = 25
eraserThickness = 100
########################


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
    
mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils

drawColor = (255, 0, 255)
color_yeet = (255, 0, 255)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
detector = HandDetector(detectionCon=0.7)

xp, yp = 0, 0
startDist = None
scale = 0
cx, cy = 500,500
tipIds = [4, 8, 12, 16, 20]

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", "DEL"],
        ["Z", "X", "C", "V", "B", "N", "M", " ", ".", ","]]





menu = cv2.imread("Slide1.PNG", cv2.IMREAD_COLOR)
menu = cv2.flip(menu,1)
painter = cv2.imread('Slide2.PNG', cv2.IMREAD_COLOR)
painter = cv2.flip(painter,1)
color = cv2.imread('Slide3.PNG', cv2.IMREAD_COLOR)
color = cv2.flip(color,1)
shape = cv2.imread('Slide4.PNG', cv2.IMREAD_COLOR)
shape = cv2.flip(shape,1)
zoom = cv2.imread('Slide5.PNG', cv2.IMREAD_COLOR)
zoom = cv2.flip(zoom,1)
textbox = cv2.imread('Slide6.PNG', cv2.IMREAD_COLOR)
textbox = cv2.flip(textbox,1)
download = cv2.imread('Slide7.PNG', cv2.IMREAD_COLOR)
download = cv2.flip(download,1)
clear = cv2.imread('Slide8.PNG', cv2.IMREAD_COLOR)
clear = cv2.flip(clear,1)

overlayList = [menu, painter, color, shape, zoom, textbox, download, clear]
header = overlayList[0]

a = 0
b = 0

finalText = ""
function = 0 

keyboard = Controller()

text_x = 60
text_y = 430
data_to_send = []
 
 
def drawAll(img, buttonList):
    img = cv2.flip(img,1)
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (192, 192, 192), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    img = cv2.flip(img,1)
    return img
 
 
class Button():
    def __init__(self, pos, text, size=[90, 90]):
        self.pos = pos
        self.size = size
        self.text = text
        

buttonList = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

size_w = 241
size_h =500

while True:    
    success,img = cap.read()
    hands, img = detector.findHands(img)
    if a != 0:
         img2 = cv2.imread("Picture6.png")
         img1= cv2.flip(img2,1)

    
    #fingersUp()
    if len(hands) == 2:
         if detector.fingersUp(hands[0]) == [0, 1, 0, 0, 0] and detector.fingersUp(hands[1]) == [0, 0, 0, 0, 0]:
             menu_pos = hands[1]["center"]
             
             header = cv2.resize (header, (size_w,size_h))
             lmList_menu = hands[0]["lmList"]
             x_menu, y_menu = lmList_menu[8][:2]
             
             try:
                 img[menu_pos[1]//2-50:menu_pos[1]//2-50+size_h, menu_pos[0]+80:menu_pos[0]+size_w+80]= header
             except:
                 pass
             
             cv2.circle(img, (x_menu, y_menu), 10, (255,250,250), cv2.FILLED)
             if menu_pos[0]+80 < x_menu < menu_pos[0]+241+80:
                 if menu_pos[1]//2-50 < y_menu < menu_pos[1]//2-50+size_h/7:
                     header = overlayList[1]
                     function = 1
                 if menu_pos[1]//2-50 + size_h/7 < y_menu < menu_pos[1]//2-50 + (size_h/7*2):
                     header = overlayList[2]
                     function = 2
                 if menu_pos[1]//2-50 + (size_h/7*2) < y_menu < menu_pos[1]//2-50 + (size_h/7*3):
                     header = overlayList[3]
                     function = 3
                     if a == 0:
                         img2 = cv2.imread("Picture6.png")
                         img1= cv2.flip(img2,1)
                     a = 1
                 if menu_pos[1]//2-50 + (size_h/7*3) < y_menu < menu_pos[1]//2-50 + (size_h/7*4):
                     header = overlayList[4]
                     function = 4
                 if menu_pos[1]//2-50 + (size_h/7*4) < y_menu < menu_pos[1]//2-50 + (size_h/7*5):
                     header = overlayList[5]
                     function = 5
                     b=1
                 if menu_pos[1]//2-50 + (size_h/7*5) < y_menu < menu_pos[1]//2-50 + (size_h/7*6):
                     header = overlayList[6]
                     function = 6
                 if menu_pos[1]//2-50 + (size_h/7*6) < y_menu < menu_pos[1]//2-50 + (size_h/7*7):
                     header = overlayList[7]
                     function = 7
                     
                 
             
             
         if detector.fingersUp(hands[0]) == [1, 1, 0, 0, 0] and detector.fingersUp(hands[1]) == [1, 1, 0, 0, 0] and function == 4:
            print("Zoom Gesture")
            
                
            lmList1 = hands[0]["lmList"]
            
            lmList2 = hands[1]["lmList"]

            if startDist is None:
                length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
 
                startDist = length

            length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
 
            scale = int((length - startDist) // 2)
            cx, cy = info[4:]
            print(scale)
        

         if detector.fingersUp(hands[0]) == [1, 0, 0, 0, 0] and detector.fingersUp(hands[1]) == [1, 0, 0, 0, 0]:
            function = 0
            header = overlayList[0]

 
    
    elif len(hands) == 1:
            startDist = None
            lmList2 = hands[0]["lmList"]
            lmList3 = hands[0]["lmList"]
            
            
            if len(lmList2) != 0: 
                x1, y1 = lmList2[8][:2]
                x2, y2 = lmList2[12][:2]
                x3, y3 = lmList2[8][:2]

                try:
                    if function == 5:
                            if detector.fingersUp(hands[0]) == [0, 1, 1, 1, 0]:
                                text_x = 1280 -x1
                                text_y = y1
                            else: 
                                img = drawAll(img, buttonList)
                                img = cv2.flip(img,1)
                                cv2.rectangle(img, (50, 350), (700, 450), (105,105,105), cv2.FILLED)
                               
                                for button in buttonList:
                                   
                                    x, y = button.pos
                                    x_alt, y_alt = button.pos
                                    w, h = button.size
                                    
                                    if 1280 - x_alt < lmList3[8][0] < 1280 - x_alt + w and y < lmList3[8][1] < y + h:
                                        
                                        cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (105,105,105), cv2.FILLED)
                                        cv2.putText(img, button.text, (x + 20, y + 65),
                                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                                        l = hypot(x2-x1,y2-y1)                                        
                         
                                        ## when clicked
                                        if l < 60:
                                            if button.text != 'DEL':                                            
                                                keyboard.press(button.text)
                                            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
                                            cv2.putText(img, button.text, (x + 20, y + 65),
                                                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                                            if button.text == 'DEL':
                                                finalText = finalText[:-1]
                                                
                                            else:
                                                finalText += button.text
                                            
                                            
                                img = cv2.flip(img,1)

                            
                    elif function == 1:
                        
                                        
                            if detector.fingersUp(hands[0]) == [0, 1, 1, 0, 0]:
                                    drawColor = (255, 255, 255)
                                    xp, yp = 0,0
                                    cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
                                    
                            elif detector.fingersUp(hands[0]) == [0, 1, 0, 0, 0]:
                                    if color_yeet == (255, 0, 255):
                                            drawColor = color_yeet
                                    else:
                                            drawColor = (int(color_yeet[0]), int(color_yeet[1]), int(color_yeet[2]))
                                            
                                    cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                                    if xp == 0 and yp == 0:
                                            xp, yp = x1, y1
                                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                                    xp, yp = x1, y1
                                   
                                    
                            elif detector.fingersUp(hands[0]) == [0, 1, 1, 1, 0]:
                                    if xp == 0 and yp == 0:
                                            xp, yp = x1, y1
                                    drawColor = (0, 0, 0)
                                    cv2.circle(img, (x1, y1), ceil(eraserThickness/2), drawColor, cv2.FILLED)
                                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                                    
                                    xp, yp = x1, y1

                    elif function == 2:
                            img_colorspec = cv2.imread("colorspec.png")
                            img_colorspec= cv2.flip(img_colorspec,1)
                            img[0:100, 0:1280] = img_colorspec
                            cv2.circle(img, (x3, y3), 5, (0,0,0), cv2.FILLED)
                            cv2.circle(img, (x3, y3), 2, (255,250,250), cv2.FILLED)
                            if 0 < y1 < 100:
                                colorsBGR = img_colorspec[y3, x3]
                                colorsRGB=tuple(reversed(colorsBGR)) #Reversing the OpenCV BGR format to RGB format
                            else:
                                color_yeet = tuple(colorsBGR)
                                

                except:
                    pass
                        
                        
    else:
        startDist = None

        
        
    
    try:
        h1, w1, _= img1.shape
        newH, newW = ((h1+scale)//2)*2, ((w1+scale)//2)*2
        img1 = cv2.resize(img1, (newW,newH))
        #imgCanvas[cy-newH//2:cy+ newH//2, cx-newW//2:cx+ newW//2] = img1
        if a != 0:
            img[cy-newH//2:cy+ newH//2, cx-newW//2:cx+ newW//2] = img1
    except:
        pass
    
    
        
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    try:
        imgInv[cy-newH//2:cy+ newH//2, cx-newW//2:cx+ newW//2] = img1
    except:
        pass
    
    try:
        if b != 0:
            img = cv2.flip(img,1)
            imgInv = cv2.flip(imgInv,1)
            cv2.putText(img, finalText, (text_x, text_y),
                        cv2.FONT_HERSHEY_PLAIN, 5, (0,0,0), 5)
            cv2.putText(imgInv, finalText, (text_x, text_y),
                        cv2.FONT_HERSHEY_PLAIN, 5, (0,0,0), 5)
            imgInv = cv2.flip(imgInv,1)
            img = cv2.flip(img,1)
    except:
        pass

    if function == 7:
        a=0
        b=0
        text_x = 60
        text_y = 430
        finalText = ""
        imgCanvas  = np.zeros((720, 1280, 3), np.uint8)
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img,imgInv)
        img = cv2.bitwise_or(img,imgCanvas)
    
    
    if function == 6:
        cv2.imwrite('savefile.png',imgInv)
        print(a)

        upload_file_list = ['savefile.png']
        for upload_file in upload_file_list:
                gfile = drive.CreateFile({'parents': [{'id': '125TK1vJ2nT5RY2q1SyrhIxAkUmI4Ze9H'}]})
                # Read file and set it as the content of this instance.
                gfile.SetContentFile(upload_file)
                gfile.Upload() # Upload the file.

        header = overlayList[0]
        function = 0
    
        
    cv2.imshow('Image',cv2.flip(img,1))
    cv2.imshow("Canvas",cv2.flip(imgInv,1))

    if cv2.waitKey(1) & 0xff==ord('q'):
        break




cap.release()



