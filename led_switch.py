import argparse
from tuya_connector import (
	TuyaOpenAPI,    
	TuyaOpenPulsar,
	TuyaCloudPulsarTopic,
)

DEVICE_ID ="eb1aeabb37c62584f7ke0s"
ACCESS_ID = "rhppxs9m9gxkprknfvx3"
ACCESS_KEY = "da9fa76c78dc4bd08564b0b048b8be79"
API_ENDPOINT = "https://openapi.tuyaus.com"
MQ_ENDPOINT = "wss://mqe.tuyaus.com:8285/"
BULB_MODEL_NAME = "LED BULB W509Z2"

# Init OpenAPI and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()   

def main():    
    # Create a parser
    parser = argparse.ArgumentParser(description="Turns the bulb {}'s light on(True) or off(False).".format(BULB_MODEL_NAME))

    # Add the argument you want to accept
    parser.add_argument(
        'boolean_argument',  # The name of the argument in the command line
        choices=['True', 'False'],  # Valid choices for the argument
        help="Specify 'True' or 'False'."
    )

    # Parse the arguments
    args = parser.parse_args()

    response = openapi.get('/v1.0/iot-03/devices/{}/status'.format(DEVICE_ID))
    status = next((item for item in response['result'] if item["code"] == "switch_led"), None)
    
    if status is not None:
        switch_led_status = status['value']    
        if (switch_led_status) == False:
            if (f"{args.boolean_argument}" == "True"):
              turn_on = {'commands': [{'code': 'switch_led', 'value': True}]}
              openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), turn_on)
              print(BULB_MODEL_NAME, "was turned on.")          
            else:
              print(BULB_MODEL_NAME,"was already turned off.")
        elif (switch_led_status) == True:
            if (f"{args.boolean_argument}" == "False"):
              turn_off = {'commands': [{'code': 'switch_led', 'value': False}]}
              openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), turn_off)
              print(BULB_MODEL_NAME, "was turned off.")          
            else:
               print(BULB_MODEL_NAME,"was turned off.")
        else:
            print("Unknown status: ", switch_led_status)
    else:
      print("switch_led not found in the device status")

if __name__ == '__main__':
    main()

