
from jinja2 import Environment, FileSystemLoader
import os

# Sensors (Input)
SENSOR_PIN_MAP = {
    "temperature": 0,    # PIN_TEMP = 0
    "water_level": 1,    # PIN_WATER = 1
    "humidity": 2,       # PIN_HUMID = 2
    "moisture": 2,       # Alias for humidity sensor
}

# Actuators (Output)
DEVICE_PIN_MAP = {
    "sprinkler": 3,      # PIN_SPRINKLER = 3
    "heater": 4,         # PIN_HEATER = 4
    "fan": 5,            # PIN_FAN = 5
    "siren": 6,          # PIN_SIREN = 6
    "light": 7,          # PIN_LIGHT = 7
    "pump": 3,           # Alias for sprinkler
}


LCD_PIN = 8  # PIN_LCD = 8


def get_template_dir():
    """Get the templates directory path"""
    return os.path.join(os.path.dirname(__file__), 'templates')


def compile_firmware(data: dict) -> str:
    """
    Compile structured intent(s) into Python firmware code
    
    Args:
        data: structured data from AI service.
              Format: { "is_valid": true, "intents": [ ... ] }
    
    Returns:
        str: Generated Python firmware code for Cisco Packet Tracer SBC
    """
    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(get_template_dir()),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    template = env.get_template('iot_master.py.jinja')
    
    # Normalize input to list of intents
    intents = data.get('intents', [])
    if not intents and 'action' in data:
        # Fallback for old single-intent format if needed
        intents = [data]
        
    # Process all intents to identify used devices and sensors
    rules = []
    used_devices = set()
    used_sensors = set()
    
    for intent in intents:
        device = (intent.get('device') or 'fan').lower()
        sensor = intent.get('sensor')
        if sensor:
            sensor = sensor.lower()
            used_sensors.add(sensor)
            
        used_devices.add(device)
        
        # Determine pins
        device_pin = DEVICE_PIN_MAP.get(device, 5)
        sensor_pin = SENSOR_PIN_MAP.get(sensor, 0) if sensor else None
        
        rules.append({
            'action': intent.get('action', 'turn_on'),
            'device': device,
            'device_pin': device_pin,
            'sensor': sensor,
            'sensor_pin': sensor_pin,
            'condition': intent.get('condition'),
            'threshold': intent.get('threshold'),
            'unit': intent.get('unit'),
            'has_condition': intent.get('condition') is not None and intent.get('threshold') is not None
        })
    
    # Unique lists for pin definitions
    unique_devices = []
    for device in used_devices:
        unique_devices.append({
            'name': device,
            'pin': DEVICE_PIN_MAP.get(device, 5)
        })
        
    unique_sensors = []
    for sensor in used_sensors:
        unique_sensors.append({
            'name': sensor,
            'pin': SENSOR_PIN_MAP.get(sensor, 0)
        })

    # Prepare template context
    context = {
        'rules': rules,
        'devices': unique_devices,
        'sensors': unique_sensors,
        'lcd_pin': LCD_PIN,
    }
    
    firmware_code = template.render(**context)
    
    return firmware_code


if __name__ == "__main__":
    # Test the compiler
    test_intent = {
        "action": "turn_on",
        "device": "sprinkler",
        "sensor": "moisture",
        "condition": "below",
        "threshold": 30,
        "unit": "percent"
    }
    
    code = compile_firmware(test_intent)
    print(code)
