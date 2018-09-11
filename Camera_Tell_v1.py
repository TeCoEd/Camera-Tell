# https://www.nkallfa.com/2017/11/05/tutorial-using-googles-cloud-vision-api-with-python/
#http://docs.pimoroni.com/buttonshim/_modules/buttonshim.html#on_release
#pip install gTTS text to speech - use google to turn text to speech
#sudo apt-get install mpg321 -  to play the audio

import io
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '1234.json'
from time import sleep
from picamera import PiCamera
camera = PiCamera()

# Pimoroni SHIM
import signal
import buttonshim
from subprocess import check_call # for shutdown
from gpiozero import LED
led = LED(4)
led.on()

# time delay to connect to the Internet ###
sleep(10)

# Google text to speech
from gtts import gTTS
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()


#############################
## set up camera ############
#############################

def take_a_photo():
    #camera = PiCamera()
    camera.resolution = (1024, 768)
    #maybe resize?
    #camera.start_preview()
    #sleep(2)
    os.system("mpg321 shutter.mp3")
    sleep(0.5)
    camera.capture('image1.jpg')
    camera.stop_preview()
    #return ('image1.jpg')

#######################################
## Image content from Google Vision ###
#######################################
    
def image_content():
    content_list = []
    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        'image1.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)

        # append to the list
        content_list.append(label.description)

    # controls text to voice, reads out contents of image 
    #print (content_list)
    tts = gTTS(text= str(content_list), lang='en')
    tts.save("image_content.mp3")
    led.off()
    os.system("mpg321 contains.mp3")
    sleep(0.1)
    os.system("mpg321 image_content.mp3")
    
#########################
## Landmark detetcion ###
#########################

def detect_landmarks(path):
    """Detects landmarks in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude {}'.format(lat_lng.latitude))
            print('Longitude {}'.format(lat_lng.longitude))

    # controls text to voice, reads out landmark
    tts = gTTS(text= landmark.description, lang='en')
    tts.save("landmark.mp3")
    led.off()
    os.system("mpg321 lm.mp3") # the landmark is
    sleep(0.2)
    os.system("mpg321 landmark.mp3")
         
#########################
##        Emotions    ###
#########################            

def detect_faces(path):
    face_emotions = []
    
    """Detects faces in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY LIKELY')
    print('Faces:')

    for face in faces:
        
        anger = ('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        joy = ('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        surprise = ('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        sadness = ('sadness: {}'.format(likelihood_name[face.sorrow_likelihood]))
        headwear = ('headwear: {}'.format(likelihood_name[face.headwear_likelihood]))   

        face_emotions = [anger, joy, surprise, sadness, headwear]
        print (face_emotions)

        # reads out the emotions
        tts = gTTS(text = str(face_emotions), lang='en')
        tts.save("emotions.mp3")
        led.off()
    os.system("mpg321 person.mp3")
    os.system("mpg321 emotions.mp3")
    
#########################
##        Logos       ###
#########################         

def detect_logos(path):
    """Detects logos in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)

        logo_ID = str(logo.description)
        #print (logo_ID)
        
        tts = gTTS(text = logo_ID, lang='en')
        tts.save("name_of_logo.mp3")
        led.off()
        os.system("mpg321 logo_is.mp3")
        os.system("mpg321 name_of_logo.mp3")
    
###############################################################
# select an option ############################################
# a = Image content #
# b = landmark #
# c =  emotions #        

os.system("mpg321 /home/pi/CameraTell/welcome.mp3")
sleep(3)
os.system("mpg321 intro.mp3")

led.off()

#################################################################
@buttonshim.on_press(buttonshim.BUTTON_A) ### content of image###
def button_a(button, pressed):
    print ("Button CONTENT of image")
    buttonshim.set_pixel(0, 255, 0)
    take_a_photo()
    led.on()
    os.system("mpg321 ana.mp3")
    image_content()

#############################################################
@buttonshim.on_press(buttonshim.BUTTON_B) ### landmarks #####
def button_b(button, pressed):
    print ("Button LANDMARKS")
    buttonshim.set_pixel(0, 255, 0)
    take_a_photo()
    led.on()
    os.system("mpg321 ana.mp3")
    detect_landmarks('/home/pi/CameraTell/image1.jpg')
    
############################################################
@buttonshim.on_press(buttonshim.BUTTON_C)  ### face ########
def button_c(button, pressed):
    print ("Button EMOTIONS")
    buttonshim.set_pixel(0, 255, 0)
    take_a_photo()
    led.on()
    os.system("mpg321 ana.mp3")
    detect_faces('/home/pi/CameraTell/image1.jpg')

############################################################
@buttonshim.on_press(buttonshim.BUTTON_D) ### logo ########
def button_d(button, pressed):
    print ("Button LOGOS")
    buttonshim.set_pixel(0, 255, 0)
    take_a_photo()
    led.on()
    os.system("mpg321 ana.mp3")
    detect_logos('/home/pi/CameraTell/image1.jpg')
    
################################################################
@buttonshim.on_hold(buttonshim.BUTTON_E) #### shutdown ########
def button_e(button, hold_time=2):
    print ("Button E SHUTDOWN")
    buttonshim.set_pixel(255, 0, 0) #'''ADD THE SHUT DOWN FROM GPIO ZERO '''   
    os.system("mpg321 bye.mp3")
    sleep(2)
    buttonshim.set_pixel(255, 0, 0)    
    check_call(['sudo', 'poweroff'])
    
@buttonshim.on_release()
def buttons(buttons, pressed):
    sleep(1)
    buttonshim.set_pixel(0, 0, 0)    

signal.pause()    
    

