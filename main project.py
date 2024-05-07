import network
import time
import json
from machine import Pin
from umqtt.simple import MQTTClient



Trig = Pin(19, Pin.OUT, 0) # the pin 19 is an output which triggers the ultrasonic sensor. 
Echo = Pin(18, Pin.IN, 0)   # the pin 18 is an input which recieves echo signals from the sensor. .
ledPin = Pin(15,Pin. OUT)# the pin 15 is an output which controls the LED.
ledPin.value(0) # set led off


# You need to create a secrets.py file with the following variables
from my_secrets import ssid, password, hivemq_name, hivemq_pw, hivemq_id, hivemq_host

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")



distance = 0 # it is a variable that store the distance measure by the ultrasonic sensor
soundVelocity = 340 # sets the speed of sound. 

def getDistance(): # this is a function that measure the distance of the ultrasonic sensor.
     Trig.value(1) # the trig pin being high starts the ultrasonic transmision signal.
     time.sleep_us(10) # pause the program for 10 microseconds. this makes sure the transmisions run effectly.  
     Trig.value(0) # this sets the trig pin back to low which ends the ultrasonic transmision signal.
     while not Echo.value(): # this loop waits for the echo pin to go high. this start the return signal from the ultrasonic sensor.
         pass # the echo pin recieves the echo signal.
     pingStart = time.ticks_us() # the loop records the time in microseconds.when the echo pin goes high the echo signal starts.
     while Echo.value(): # this loops waits for the echo pin to go low. this ends the echo signal and indicates the end of the ultrasonic cycle.
         pass
     pingStop = time.ticks_us()  #the loop records the time in microseconds.when the echo pin goes low the echo signal ends.
     distanceTime = time.ticks_diff(pingStop, pingStart) // 2 # it calculates the distance on time taken for the ultrasonic sign to travel thier&back.
     distance = int(soundVelocity * distanceTime // 10000) # calulates the distance.
     return distance # return the distance calulated above.
    

    
# Your topic can be created in your device profile on thingsboardshu.cloud
mqtt_publish_topic = "distance"

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
        client_id=hivemq_id,
        server=hivemq_host,
        port=0,
        ssl=True,
        ssl_params={'server_hostname': hivemq_host},
        user=hivemq_name,
        password=hivemq_pw)

def message_recieved(topic, response): # defines the function message recieved 
    
    print("Message recieved!") # prints Message recieved
    ledPin.toggle() # turns LED off

mqtt_subscribe_topic = "led/topic" # sets the MQTT topic and subscribes to the topic "led/topic"
mqtt_client.connect() # conects MQTT to hive broker
mqtt_client.set_callback(message_recieved) # it uses a callback function that is call when a message is recieved on the topic "led/topic"
mqtt_client.subscribe(mqtt_subscribe_topic) # This line subscribes the MQTT client to the topic specified by mqtt_subscribe_topic.
print("client connected") # when MQTT is successfully connected print "client connect"

time.sleep(2)
while True:
     time.sleep_ms(500)
     mqtt_client.check_msg()
     distance = getDistance()
     print("Distance: ", distance, "cm") # gives/prints the result of the distance detected
     mqtt_client.publish('distance', str(distance))
     if distance <= 10: # if the distance is less that 10cm go to the next line
         ledPin.value(1) # turn the led on


