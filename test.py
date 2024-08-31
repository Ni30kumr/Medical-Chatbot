import requests
import json
from datetime import datetime




def find_closest_time(time_list):
    # Get current time
    current_time = datetime.now().time()

    # Convert current time to a comparable format (minutes since midnight)
    current_minutes = current_time.hour * 60 + current_time.minute

    closest_dict = None
    smallest_diff = float('inf')

    for time_dict in time_list:
        # Parse the time string
        time_str = time_dict['timings']
        time_obj = datetime.strptime(time_str, '%I:%M %p').time()

        # Convert to minutes since midnight
        time_minutes = time_obj.hour * 60 + time_obj.minute

        # Calculate the difference
        diff = abs(current_minutes - time_minutes)

        # Handle cases crossing midnight
        if diff > 720:  # More than 12 hours difference
            diff = 1440 - diff  # 24 hours = 1440 minutes

        if diff < smallest_diff:
            smallest_diff = diff
            closest_dict = time_dict

    return closest_dict

# nearest_time_dict = find_closest_time(time_list)
# print(nearest_time_dict)








# print(type(response.json()))
# print(response.json())


# Save the message to a JSON file with proper indentation
# with open('output2.json', 'w', encoding='utf-8') as outfile:
#     json.dump( nearest_time_dict, outfile, indent=4, ensure_ascii=False)

# print(a.json()[0]['message'])