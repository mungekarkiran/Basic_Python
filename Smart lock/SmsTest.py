import time
from sinchsms import SinchSMS

for x in range(1):
    print(x)
    number = '+918108412112'
    message = '2 Hi, how are you today? Someone is trying to open your door now.'

    client = SinchSMS("75d2661a-dcb6-4bfc-bde1-4120b0170e12", "6DIOitwBj06qimw69CObVQ==")

    print("Sending '%s' to %s" % (message, number))
    response = client.send_message(number, message)
    message_id = response['messageId']

    response = client.check_status(message_id)
    while response['status'] != 'Successful':
        print(response['status'])
        time.sleep(1)
        response = client.check_status(message_id)
    print(response['status'])

