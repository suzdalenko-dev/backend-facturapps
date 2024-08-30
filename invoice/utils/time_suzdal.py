from datetime import datetime
import time

def time_suzdal():
    # Get the current time
    current_time = datetime.now()
    # Format the time in the desired format
    formatted_time = str(current_time.strftime('%Y-%m-%d %H:%M:%S'))
    return formatted_time


def second_suzdal():
    current_time_seconds = int(time.time())
    return current_time_seconds
