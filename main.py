# Import model libraries
import torch
import numpy as np
from model import predict

# Import sensor functions
from sound_sensor import detect_sound
from motion_sensor import detect_motion
import water_heater_api
import time

# Other libraries
import concurrent.futures
from functools import partial


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
    new_data = np.array([sound_result, motion_result, time.time])
    new_tensor = torch.FloatTensor(new_data)
    heater_prediction = predict(new_tensor)

    if heater_prediction > .7:
        water_heater_api.setlight("On")
    if heater_prediction < .3
        water_heater_api.setlight("Off")

    time.sleep(10)