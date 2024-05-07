import argparse
from tuya_connector import (
	TuyaOpenAPI,    
	TuyaOpenPulsar,
	TuyaCloudPulsarTopic,
)

# Initiate connection to Tuya device
ACCESS_ID = "<access_id>"
ACCESS_KEY = "<access_key>"
API_ENDPOINT = "https://openapi.tuyaus.com"
MQ_ENDPOINT = "wss://mqe.tuyaus.com:8285/"

DEVICE_ID ="<device_id>"

BULB_MODEL_NAME = "<rgb_model_name>"


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

