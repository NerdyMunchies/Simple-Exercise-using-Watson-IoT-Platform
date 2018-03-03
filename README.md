# Simple-Exercise-using-Watson-IoT-Platform

## Node-RED in IBM Cloud
Node-RED is an open source visual flow-based programming tool used for wiring not only Internet of Things (IoT) components, but also integrating an ensemble of service APIs, including ones provided by IBM Cloud.

This repository provides an example of a Node-RED application that is supposed to grab sensor data from DHT11 sensor connected to a Raspberry Pi and visualize this data. Based on the sensor data gathered, an alert signal could be sent to notify the user that the sensor data (ie. temperature and/or humidity) are out side a defined range. This is just a simple exercise to show how to use Watson IoT Platform services to publish events from and to send commands to the Raspberry Pi.

The application explored in this repository can be deployed into IBM Cloud via the simple steps explained below.


## How does the system work?
The Raspberry Pi 3 communicates with the DHT11 sensor to collect temperature and humidity data that is to be sent to IBM Cloud via MQTT. This process is simplified through the usage of the **Internet of Things Platform** service available on IBM Cloud. If values of the temperature and humidity are not within a particular range, a signal is sent through Watson IoT Platform service to alert the user through lighting up a LED. Both the sensor data are stored in a **Cloudant NoSQL database** to allow the convenient access to them at any point in time.

The connecting of the described components is made possible and simple through the deploying a Node-RED Node.js application instance.


## Architecture overview
An architecture overview of the system can be found below.

![architecture_overview]()


## Connecting connections to the Raspberry Pi

For the connection between the Raspberry Pi and the other components, check the schematic below.

![rpi_connections]()

You will find that there is a file called *rpi_iotf.py*, which you will need to copy onto the Raspberry Pi.

**Import iotf and dht11 files - To be added**


## Pre-requisite
An IBM Cloud account - A lite account, which is a free of charge account that doesn’t expire, can be created through going to [IBM Cloud]().


## Creating the Node-RED application and other components
There are three components to configure: <br/>
-	Node-RED application <br/>
-	Internet of Things Platform service <br/>
-	Cloudant NoSQL database <br/>

To simplify connecting these three, a boilerplate called **Internet of Things Platform Starter** is used. It can be found by going to Catalog followed by selecting **Boilerplates**, which can be seen on the menu available on the left-hand side. The user is then required a unique name for the application being created, which is also used as the hostname. If the user is using a lite account, the region is set to that chosen while applying for the account. After clicking on **create**, an instance of the Node-RED application is created to which both the **Internet of Things Platform** service and **Cloudant NoSQL database** are bound. It will take some time for the application status to change to awake, indicating that it is running.

![Alt Text]()


## Steps to configure the Node-RED application and other components
From the hamburger menu at the top left of the page, the user can access the dashboard, which will allow the user to see all the applications and services that have been created. Click on the name of the application to go to a window that provides more details about the application. If you click on **Connection** on the menu seen on the left hand-side, you will notice that there are two connections: <APP-NAME>-cloudantNoSQLDB and <APP-NAME>-iotf-service.

### Step 1: Setting up Internet of Things Platform service
If we click on <APP-NAME>-iotf-service, it will take us to the page with the details about the **Internet of Things Platform** service. Go to **Manage** and then click on **Launch**. This will take us to the page where we can configure devices we can connect to among other things. At the top right of the page, we see an ID, this is the organization ID and it is one of the things needed to configure the connection between a device and the **Internet of Things Platform** service.

Here, we are required to configure a device type to which we will be adding a device. Go to **Devices** from the menu on the left, and from the newly opened page, click on **Device Types** followed by **Add Device Type**. Here you will provide the name and metadata describing the device type to create the device type. Then, click **Register Devices** to add a device to that particular device type. Enter a Device ID, metadata describing the device and select an option to define the authentication token. After you are done, you will be directed to a page summarizing the device’s credentials. Copy the credentials into a notepad for later use (It will be used by both the Raspberry Pi to send data and the Node-RED application to get the data.

![Alt Text]()
![Alt Text]()

In order to communicate with **Internet of Things Platform** service, you will notice that, in the file we added to the Raspberry Pi, we have included the code snippets below to the appropriate locations, where you will change the organization, deviceType, deviceId, and authToken to that corresponding to the credentials we copied earlier.

**To be modified**
```python
organization = #add organisation from the IoT platform service
deviceType = #add device type from the IoT platform service
deviceId = #add device ID from the IoT platform service
appId = deviceId + "_receiver"
authMethod = "token"
authToken = #add authentication token from the IoT platform service

def myOnPublishCallback():
    print "Confirmed event received by IoTF\n"

# Initialize the device client.
deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
client = ibmiotf.device.Client(deviceOptions)
print "init successful"

# Connect and send a datapoint 
def send(data):
    success = client.publishEvent("data", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print "Not connected to IoTF"

client.connect()
send({'IR':INR, "US": USS, "X": X1, "Y": Y1, "Z": Z1 })
client.disconnect()
```

### Step 2: Setting up Cloudant NoSQL database
If we click on <APP-NAME>-cloudantNoSQLDB, it will take us to the page with the details about the Cloudant NoSQL DB service. Click on **Service Credentials** on the menu seen on the left hand-side.  If no service credentials are found, create a new credential. Go to the newly created credential and select **View credentials**. Then, copy both the content into a notepad for later use. The username and password will be used for authentication to allow us to communicate with the database.

![Alt Text]()

Next, go to **Manage** and then click on **Launch**. This will launch an interface through which we can interact with the **Cloudant NoSQL DB**. Click on the **Databases** from the menu available on the left. By default, a database named nodered can be found, which we are not going to touch. Now, click on **Create Database** at the top of the page to create a new Database and give it a name (here, we called it iotdb) and click **create**. Here, we will be saving any data we will be receiving. Whenever we want to store something, we store that data in a document in a NoSQL database.

![Alt Text]()


### Step 3: Setting up Node-RED application
Go back to the dashboard and click on the application you created earlier. In order to access the Node-RED editor used to build the application, click on **Visit App URL**. Follow the directions to access the Node-RED editor (you are encouraged to secure your Node-RED editor to ensure that only authorized users can access it). Click on **Go to your Node-RED flow editor**.

![Alt Text]()

A new Node-RED flow appears containing nodes representing a sample application. Select all the nodes and delete them as we will be importing our own flow. In this repository, go to the file called **Node-REDflow_Partial.json** and copy its content. In the Node-RED editor, go to the hamburger menu at the top right of the page after which select **Import Clipboard**. Paste the content of the JSON file and click on **Import**. This will mostly import the calculation part of the application and will be missing some nodes that we will be adding.

We will notice that we have an error saying that we imported unrecognized types. These are related to the dashboard nodes that we will be working with shortly. To work with these nodes, we need to install a module, which can be achieved by going to the hamburger menu again and clicking on **Manage palette**. In the **Install** tab, we will search for **node-red-dashboard** module and install it. If look at the node type menu on the left hand-side, we will notice that a number of nodes have been added under the **dashboard** node type.

We will add an **ibmiot** node, which can be seen under **input**, to allow us to consume any data received by the **IoT Platform** service. By double-clicking on the node, we can change its properties and set the **Authentication** to **Bluemix Service**, **Device Type** and **Device id** to the device type and device id that we defined in the IoT Platform service. We will connect it to a **debug node**, which can be found under **output** node type. Before we continue, we will check if our application can receive any data from the Raspberry PI, which should show as a JSON object under the **debug** tab on the right.

![config_ibmiot]()

