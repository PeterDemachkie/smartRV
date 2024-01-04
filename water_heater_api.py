import requests

def get_light_status(esp32_ip="192.168.4.149"):

    url = f"http://{esp32_ip}/"
    response = requests.get(url)
    if response.status_code == 200:
        # returns true if "heater" is on, false if not
        return bool(response.json()['green'])
    else:
        return None
    
def set_light(esp32_ip="192.168.4.149", activate=False):
    url = f"http://{esp32_ip}/"
    if activate:
        url+= "heaterOn"
    else:
        url+= "heaterOff"
    response = requests.get(url)
    if response.status_code != 200:
        return False
    return True