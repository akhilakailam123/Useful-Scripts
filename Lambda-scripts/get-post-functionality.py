import json

def lambda_handler(event, context):
    #getperson functionality
    get_raw_path = "/example-stage/getPerson"
    print(event)
    if event['rawPath'] == get_raw_path:
        print("Started request for getPerson")
        personid = event['queryStringParameters']['personid']
        print("Person ID: " + personid)
        if personid == "123":
            return {'name':'Afreed','age':'20','email':'afreedhf@gmail.com'}

    #createperson functionality
    create_raw_path = "/example-stage/createPerson"
    if event['rawPath'] == create_raw_path:
        print("Event of createPerson")
        decode_event = json.loads(event['body'])
        print("Decoded event of createPerson")
        print(decode_event)
        print("Started request for createPerson")
        personid = event['queryStringParameters']['personid']
        print("Person ID: " + personid)
        print("Person name: " + decode_event['name'])
        return {'statusCode': 200,'body': json.dumps('Person created successfully')}

