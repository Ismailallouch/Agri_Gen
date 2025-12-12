
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


def compile_firmware(intent: dict) -> str:
    """
    Compile structured intent into Python firmware code
    
    Args:
        intent: Structured IoT intent from AI
                {action, device, sensor, condition, threshold, unit}
    
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
    
    # Map device and sensor to GPIO pins (with safe defaults)
    device = (intent.get('device') or 'fan').lower()
    sensor = intent.get('sensor')
    if sensor:
        sensor = sensor.lower()
    
    device_pin = DEVICE_PIN_MAP.get(device, 5)  # Default to fan (pin 5)
    sensor_pin = SENSOR_PIN_MAP.get(sensor, 0) if sensor else None
    
    # Prepare template context
    context = {
        'action': intent.get('action', 'turn_on'),
        'device': device,
        'device_pin': device_pin,
        'sensor': sensor,
        'sensor_pin': sensor_pin,
        'condition': intent.get('condition'),
        'threshold': intent.get('threshold'),
        'unit': intent.get('unit'),
        'lcd_pin': LCD_PIN,
        'has_condition': intent.get('condition') is not None and intent.get('threshold') is not None
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
