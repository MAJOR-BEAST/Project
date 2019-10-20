from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import pandas as pc
import unicodedata
import os
import sys
import time
import re
import csv


# Add your Computer Vision subscription key to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
# Add your Computer Vision endpoint to your environment variables.
if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


'''
Recognize handwritten text - local
This example extracts text from a handwritten local image, then prints results.
This API call can also recognize printed text (not shown).
'''
print("===== Detect handwritten text - local =====")
# Get image of handwriting
local_image_handwritten_path = "100775.jpg"
# Open the image
local_image_handwritten = open(local_image_handwritten_path, "rb")

# Call API with image and raw response (allows you to get the operation location)
recognize_handwriting_results = computervision_client.batch_read_file_in_stream(local_image_handwritten, raw=True)
# Get the operation location (URL with ID as last appendage)
operation_location_local = recognize_handwriting_results.headers["Operation-Location"]
# Take the ID off and use to get results
operation_id_local = operation_location_local.split("/")[-1]

# Call the "GET" API and wait for the retrieval of the results
while True:
    recognize_handwriting_result = computervision_client.get_read_operation_result(operation_id_local)
    if recognize_handwriting_result.status not in ['NotStarted', 'Running']:
        break
    time.sleep(1)

#choice = int(input())
csv_data = {}
date = ""
sr=""
tot=10000

# Print results, line by line
if recognize_handwriting_result.status == TextOperationStatusCodes.succeeded:
    for text_result in recognize_handwriting_result.recognition_results:
        for line in text_result.lines:
            

            '''comp_name = re.match(r"^Computer ",line.text)
            if comp_name:
                print comp_name.string'''
            dates = re.match(r"(\b\d{1,2}\D{0,3})?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2})",line.text)
            if dates:
                date = str(dates.string)
                print dates.string

            srno = re.match(r"(\ASR. NO)",line.text)
            if srno:
                sr = str(srno.string)
                print srno.string
            total = re.match(r"(?:Rs\.?|INR)\s*(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s*(?:Rs\.?|INR)",line.text)
            if total:
                tot = float(total.string)
                print total.string
            csv_data = {'Date':date,'Serial No': sr,'Grand Total': tot}
            with open('test.csv', 'w') as f:
                for key in csv_data.keys():
                    f.write("%s,%s\n"%(key,csv_data[key]))


            '''dates = re.match(r"(\b\d{1,2}\D{0,3})?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2})",line.text)
            if dates:
                print dates.string
            srno = re.match(r"(\ABatch )",line.text)
            if srno:
                print srno.string
            total = re.match(r"(?:Rs\.?|INR)\s*(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s*(?:Rs\.?|INR)",line.text)
            if total:
                print total.string'''
            
            '''dates = re.match(r"^([0-2][0-9]|(3)[0-1])(\-)(((0)[0-9])|((1)[0-2]))(\-)\d{4}$",line.text)
            if dates:
                print dates.string
            srno = re.match(r"(\AS.No)",line.text)
            if srno:
                print srno.string
            total = re.match(r"(?:Rs\.?|INR)\s*(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s*(?:Rs\.?|INR)",line.text)
            if total:
                print total.string
            #comp_name = line.text[5]
           # print comp_name'''
            '''comp_name = re.match(r"\AVinayak",line.text)
            if comp_name:'''
                
            '''dates = re.match(r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$",line.text)
            if dates:
                print dates.string
            srno = re.match(r"(\ASerial.no )",line.text)
            if srno:
                print srno.string
            total = re.match(r"(?:Rs\.?|INR)\s*(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s*(?:Rs\.?|INR)",line.text)
            if total:
                print total.string'''

            #print(line.text)
            #po+=[line.text]
            #print(line.bounding_box)

    #pc.DataFrame(po).to_excel('output.xlsx', header=False, index=False)
#print()
'''
END - Recognize handwritten text - local
'''

