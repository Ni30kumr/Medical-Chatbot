import requests
import json
from datetime import datetime


response= requests.get('https://clchatagentassessment.s3.ap-south-1.amazonaws.com/queries.json')



final =response.json()[3]
with open('4.json', 'w', encoding='utf-8') as outfile:
    json.dump( final, outfile, indent=4, ensure_ascii=False)
    
