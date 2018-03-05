import RPi.GPIO as GPIO
import dht11
import time
import ibmiotf.device

organization = "" #add organisation from the IoT platform service
deviceType = "" #add device type from the IoT platform service
deviceId = "" #add device ID from the IoT platform service
authMethod = "token"
authToken = "" #add authentication token from the IoT platform service

LED_pin = 4
DHT11_pin = 22

temp = 0
hum = 0

# Initialize the device client.
deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
client = ibmiotf.device.Client(deviceOptions)
print("init successful")


DHT11_sensor = dht11.DHT11(pin = DHT11_pin)

# initialize GPIO
def init_GPIO():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    # set LED pin as output
    GPIO.setup(LED_pin, GPIO.OUT)
     
# get temperature and humidity from the sensor
def getTempHum():
    global temp
    global hum
    temp_hum = DHT11_sensor.read()
    if temp_hum.is_valid():
        temp = temp_hum.temperature
        hum =  temp_hum.humidity


def myOnPublishCallback():
    print("Confirmed event received by IoTF")

# Connect and send a datapoint 
def send(data):
    success = client.publishEvent("data", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not connected to IoTF")

# get a command from Watson IoT Platform
def myCommandCallback(cmd):
    print("Command received: %s\n" % cmd.data)
    if cmd.data['led_on'] == 1:
        GPIO.output(LED_pin, True)
    else:
        GPIO.output(LED_pin, False)
    

if __name__=='__main__':
    init_GPIO()
    client.connect()
    while True:
        try:
            getTempHum()

            send({"temp":temp, "hum": hum})
            
            client.commandCallback = myCommandCallback
            
            time.sleep(2)
            
        except KeyboardInterrupt:
            client.disconnect()
            GPIO.cleanup()
            break

