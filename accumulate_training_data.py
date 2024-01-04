# This program records data for the machine learning model
from sound_sensor import detect_sound
from motion_sensor import detect_motion
from water_heater_api import light_status
import concurrent.futures
import time
import csv

datafile = 'sensor_data.csv'

while True:
    partial_detect_sound = partial(detect_sound, 5)
    partial_detect_motion = partial(detect_motion, 5)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        sound_sensor = executor.submit(partial_detect_sound)
        motion_sensor = executor.submit(partial_detect_motion)

        concurrent.futures.wait([sound_sensor, motion_sensor])

        sound_result = sound_sensor.result()
        motion_result = motion_sensor.result()

    current_time = time.time()
    heater_status = light_status()

    with open(datafile, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([sound_result, motion_result, current_time, heater_status])

    if input("Quit?: ") != "":
        break