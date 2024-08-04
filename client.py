#importing modules
import cv2
import imutils
import socket
import time
from cryptography.fernet import Fernet


s = socket.socket(socket.AF_INET,
                socket.SOCK_STREAM)

s.bind(('', 5000))

s.listen(1)
c, addr = s.accept()

print("CONNECTION FROM:", str(addr))

hog = cv2.HOGDescriptor()

hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Reading the Image
#image = cv2.imread('img.jpg')
vid = cv2.VideoCapture(0)

center_coordinates = (40,40)
  
radius = 30

color = (0, 0, 255)

thickness = -1




def ped():
  c.send("green,pedestrain".encode())
  #Red green signal for pedestrain
  time.sleep(10)
  c.send("red,pedestrain".encode())

  # Send red signal for pedestrain

  hog = cv2.HOGDescriptor()
  hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
  car_cascade = cv2.CascadeClassifier('cars.xml')
  vid = cv2.VideoCapture(0)
  while(True):
      
    ret, image = vid.read()
    img = cv2.imread("car.png", cv2.IMREAD_COLOR)


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)
    print(len(cars))
    if len(cars)!=0:


        for (x,y,w,h) in cars:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        result=cv2.imwrite('pic.png', img)

        key = Fernet.generate_key()
         
        # string the key in a file
        with open('filekey.key', 'wb') as filekey:
           filekey.write(key)


        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()

        fernet = Fernet(key)

         
        # opening the original file to encrypt
        with open('pic.png', 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)
        print(cars)
        with open('pic_encrypted.png', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        c.send("car detected:image saved as new_pic.png ".encode())




    

    image = imutils.resize(image,
                        width=min(1000, image.shape[1]))

    (regions, _) = hog.detectMultiScale(image,
                                        winStride=(4, 4),
                                        padding=(4, 4),
                                        scale=1.05)

    #print(regions)  
    if len(regions)==0:
        #cv2.release()
        break
    elif len(regions)!=0:
            # msg="red"
            image = cv2.circle(image, center_coordinates, radius, color, thickness)
            # c.send(msg.encode())
            # time.sleep(10)


    for (x, y, w, h) in regions:
        cv2.rectangle(image, (x, y),(x + w, y + h),(255, 0, 0), 2)

        # Showing the output Image
        #print(regions)
    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
  vid.release()
  cv2.destroyAllWindows()
  
def vechiles():
  #Red green signal for vehicles

  c.send("green,vehicles".encode())
  time.sleep(9)

  c.send("orange,vehicles".encode())
  #siganal pampali
  time.sleep(2)

  c.send("red,vehicles".encode())
  #red signal pamapli

  
while True:
  ped()
  vechiles()