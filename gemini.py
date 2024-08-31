"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai

import requests
import json
from datetime import datetime
from test import find_closest_time

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

now =datetime.now().time()

# Extract the date, day of the week (number), and time
now = datetime.now()  # Define 'now' as the current date and time
today_date = now.date()
day_number = now.weekday()  # Add 1 because weekday() starts from 0 (Monday)
current_time = now.time()
response= requests.get('https://clchatagentassessment.s3.ap-south-1.amazonaws.com/queries.json')



diet_list=response.json()[0]["profile_context"]["diet_chart"]["meals_by_days"][day_number]["meals"]
diet_list=find_closest_time(diet_list)
patient_profile=response.json()[0]["profile_context"]["patient_profile"]
overall=response.json()[0]["profile_context"]["diet_chart"]["notes"]
program_name=response.json()[0]["profile_context"]["program_name"]
chat_context=response.json()[0]["chat_context"]
query=response.json()[0]["latest_query"]
ticket_id= response.json()[0]["chat_context"]["ticket_id"]
ideal_response=response.json()[0]["ideal_response"]

# diet_plan = f"\"diet plan\":{diet_list}"

diet_plan = f'"diet plan": {json.dumps(diet_list)}'






def prediction():
    generation_config = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )


    value = f"""You are a caretaker chatbot of patients who are suffering from conditions like PCOS, Preconception, and Pregnancy through multiple disciplinary care including dieticians, yoga instructors, mental health specialists, etc.
    You will be given a Patient Profile, an overall review of what kind of food he/she is supposed to eat, Program Name, His her diet Plan, his/her previous interaction, and his current query which can be the description of a food image that he/She is eating.

    "patient_profile": {patient_profile}\n
    "overall review": {overall}\n
    "program_name": {program_name}
    {diet_plan}
    "chat_context": {chat_context}

    "latest_query": {query}

    Based on all of his/her above data solve his query within 30 words
    output like "Great job for having methi water, continue having it daily, it will help boost your metabolism.\nVarsha, 
    but i also noticed that you are having figs and raisins but they are not presrcibed in the diet plan, can i know why you have added them ?"""
    chat_session = model.start_chat(
    history=[
    ]
    )
    output= chat_session.send_message(value)


    print(output.text)

    final_dict={
        "ticket_id":ticket_id,
        "latest_query":query,
        "generated_response":output.text,
        "ideal_response":ideal_response,
    }

    with open('output.json', 'w', encoding='utf-8') as outfile:
        json.dump( final_dict, outfile, indent=4, ensure_ascii=False)