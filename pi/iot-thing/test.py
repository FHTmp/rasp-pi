from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
# For certificate based connection
myShadowClient = AWSIoTMQTTClient("my-iot-thing")
END_POINT="abzkvohbnb5hm-ats.iot.us-east-1.amazonaws.com"
myShadowClient.comfigureEndpoint(END_POINT, 8883)


# Configurations
# For TLS mutual authentication
myShadowClient.configureEndpoint("YOUR.ENDPOINT", 8883)
# The Endpoint can be found in the Interact part in the details of your Thing which showed above
# For Websocket
# myShadowClient.configureEndpoint("YOUR.ENDPOINT", 443)
# For TLS mutual authentication with TLS ALPN extension
# myShadowClient.configureEndpoint("YOUR.ENDPOINT", 443)

ROOT_CA_PATH = "/home/finau/env1/my-iot-thing/AmazonRootCA1.pem"
PRIV_KEY_PATH = "/home/finau/env1/my-iot-thing/efdb96c032239480625af974dc24ed868bf130073832a68d997e76ccd8b6520e-private.pem.key"
CERT_PATH = "/home/finau/env1/my-iot-thing/efdb96c032239480625af974dc24ed868bf130073832a68d997e76ccd8b6520e-certificate.pem.crt"
myShadowClient.configureCredentials(ROOT_CA_PATH,PRIV_KEY_PATH, CERT_PATH)
# The three files which we transferred earlier, get the path easily using the method above
# For Websocket, we only need to configure the root CA
myShadowClient.configureCredentials(ROOT_CA_PATH)
myShadowClient.configureConnectDisconnectTimeout(10) # 10 sec
myShadowClient.configureMQTTOperationTimeout(5) # 5 sec

def customShadowCallback_Update(payload, responseStatus,token):
 # payload is a JSON string ready to be parsed using json.loads(...)
 # in both Py2.x and Py3.x
 if responseStatus == "timeout":
    print("Update request " + token + " time out!")
 if responseStatus == "accepted":
    payloadDict = json.loads(payload)
    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("Update request with token: " + token + "accepted!")
    print("property: " + str(payloadDict["state"]["reported"]))
    print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
 if responseStatus == "rejected":
    print("Update request " + token + " rejected!")
    
def customShadowCallback_Delete(payload, responseStatus,token):
 if responseStatus == "timeout":
    print("Delete request " + token + " time out!")
 if responseStatus == "accepted":
    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("Delete request with token: " + token + "accepted!")
    print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
 if responseStatus == "rejected":
    print("Delete request " + token + " rejected!")


myShadowClient.connect()
# Create a device shadow instance using persistent subscription
myDeviceShadow = myShadowClient.createShadowHandlerWithName("my-iot-thing", True)
# The Thing Name is what we created initially, it should be “my-iot-thing” in the case above
# Delete shadow JSON doc
myDeviceShadow.shadowDelete(customShadowCallback_Delete, 15)
# Shadow operations
# This is the shadow message we want to update to the AWS
# NOTE: Don’t put these comment lines into the JSON area
# otherwise it will be wrong and update nothing
JSONPayload = """{ "state":
    { "reported":
        { "time":"08:10",
            "temperature":"17"
        }
    },
"message": "Hello from AWS IoT console"
}"""

# Update shadow JSON
myDeviceShadow.shadowUpdate(JSONPayload,customShadowCallback_Update, 5)