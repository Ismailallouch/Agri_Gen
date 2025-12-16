"""
AI Service - Advanced Intent Extraction
Uses Ollama (Llama 3) or Google Gemini for intelligent IoT intent parsing
Supports multiple languages and flexible prompt structures
"""

import json
import os
import re
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3')
USE_OLLAMA = os.getenv('USE_OLLAMA', 'true').lower() == 'true'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Advanced System Prompt - More flexible and intelligent
SYSTEM_PROMPT = """You are an expert IoT Automation Architect specializing in smart agriculture systems.

Your task is to understand natural language commands about farm automation and extract structured data.
You must be FLEXIBLE and INTELLIGENT in understanding user intent, even with:
- Incomplete sentences
- Different languages (English, French, Spanish, etc.)
- Informal language
- Typos or abbreviations
- **Compound commands (e.g. "turn on fan AND turn off light")**

## CRITICAL: VALIDATE RELEVANCE FIRST
Before extracting intent, you MUST check if the prompt is related to:
- Smart agriculture / farming automation
- IoT devices (sensors, actuators, sprinklers, fans, heaters, lights, pumps, alarms)
- Environmental monitoring (temperature, humidity, moisture, light levels, water levels)
- Device control (turn on/off, activate, monitor, alert)

If the prompt is NOT related to agriculture/IoT automation (e.g., general questions, greetings, unrelated topics like weather, math, personal questions, coding questions, etc.), return:
{
    "is_valid": false,
    "error_message": "This request is not related to agricultural IoT automation. Please describe an action for your smart farm, such as controlling sprinklers, fans, heaters, lights, or setting up sensor-based automation."
}

## IMPORTANT RULES (only if prompt is valid):
1. ALWAYS infer the most logical device based on the sensor mentioned:
   - temperature → heater (if cold) or fan (if hot)
   - moisture/humidity → sprinkler or pump
   - light level → light
   
2. If no explicit condition, infer from context:
   - "too hot", "exceeds", "above", "plus de" → "above"
   - "too cold", "drops", "below", "moins de", "inférieur" → "below"
   
3. Understand common abbreviations and variants:
   - temp, température, temperatura → temperature
   - humidité, humidity, humid → humidity
   - arroseur, sprinkler, irrigation → sprinkler
   - ventilateur, fan, ventilo → fan
   - chauffage, heater, radiateur → heater
   - lumière, light, lampe → light
   - alarme, siren, sirène, alert → siren

4. Handle simple commands without conditions:
   - "Turn on the fan" → action: turn_on, device: fan, no condition
   - "Éteindre la lumière" → action: turn_off, device: light
   - "Turn of the light" → action: turn_off (handle "turn of" as typo for "turn off")

5. EXTRACT MULTIPLE COMMANDS:
   - Split compound sentences connected by "and", "et", "then", ",".
   - Example: "Turn on fan AND turn off light" -> 2 intents.

6. Extract threshold values from any format:
   - "below 30%", "under 30", "< 30", "moins de 30" → threshold: 30

## OUTPUT FORMAT (JSON only):

For VALID agriculture/IoT prompts, return an object with an "intents" array:
{
    "is_valid": true,
    "intents": [
        {
            "action": "turn_on" | "turn_off" | "monitor" | "alert",
            "device": "sprinkler" | "fan" | "heater" | "light" | "pump" | "siren",
            "sensor": "temperature" | "humidity" | "moisture" | "light_level" | "water_level" | null,
            "condition": "above" | "below" | "equals" | null,
            "threshold": <number or null>,
            "unit": "celsius" | "fahrenheit" | "percent" | null,
            "summary": "Turn on fan when temperature > 25"
        },
        ... (more intents if compound command)
    ]
}

For INVALID/unrelated prompts:
{
    "is_valid": false,
    "error_message": "<helpful message explaining what Agri-Gen does and asking for a valid command>"
}

## EXAMPLES:

Input: "allumer le ventilateur si temp > 25 et éteindre la lumière"
Output: {
    "is_valid": true,
    "intents": [
        {"action": "turn_on", "device": "fan", "sensor": "temperature", "condition": "above", "threshold": 25, "unit": "celsius", "summary": "Turn on fan > 25C"},
        {"action": "turn_off", "device": "light", "sensor": null, "condition": null, "threshold": null, "unit": null, "summary": "Turn off light"}
    ]
}

Input: "water plants when dry"
Output: {
    "is_valid": true,
    "intents": [
        {"action": "turn_on", "device": "sprinkler", "sensor": "moisture", "condition": "below", "threshold": 30, "unit": "percent", "summary": "Water when dry"}
    ]
}

Input: "What is the weather today?"
Output: {"is_valid": false, "error_message": "This request is not related to agricultural IoT automation..."}

RESPOND WITH JSON ONLY. NO MARKDOWN. NO EXPLANATIONS OUTSIDE JSON."""


def extract_with_ollama(prompt: str) -> dict:
    """Extract intent using Ollama (Llama 3)"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": f"{SYSTEM_PROMPT}\n\nUser command: {prompt}\n\nJSON output:",
                "stream": False,
                "format": "json"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '')
            
            # Parse JSON from response
            data = json.loads(response_text)
            print(f"[Ollama] Extracted: {data}")
            
            # Backwards compatibility/normalization
            if "intents" not in data and "action" in data:
                # Converted old format to new format
                data = {"is_valid": True, "intents": [data]}
                
            return data
        else:
            print(f"[Ollama] Error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("[Ollama] Connection failed - is Ollama running?")
        return None
    except json.JSONDecodeError as e:
        print(f"[Ollama] JSON parse error: {e}")
        return None
    except Exception as e:
        print(f"[Ollama] Error: {e}")
        return None


def extract_with_gemini(prompt: str) -> dict:
    """Extract intent using Google Gemini API"""
    if not GEMINI_API_KEY:
        print("[Gemini] No API key configured")
        return None
        
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.2,
            }
        )
        
        response = model.generate_content(
            f"{SYSTEM_PROMPT}\n\nUser command: {prompt}"
        )
        
        data = json.loads(response.text)
        print(f"[Gemini] Extracted: {data}")
        
        # Backwards compatibility
        if "intents" not in data and "action" in data:
            data = {"is_valid": True, "intents": [data]}
            
        return data
        
    except Exception as e:
        print(f"[Gemini] Error: {e}")
        return None


def extract_with_fallback(prompt: str) -> dict:
    """
    Intelligent keyword-based fallback parser with multi-language support.
    Supports basic compound splitting by 'and', 'et', etc.
    """
    print("[Fallback] Using intelligent keyword parser")
    
    prompt_lower = prompt.lower()
    
    # First check if the prompt contains ANY IoT-related keywords
    all_iot_keywords = [
        # Devices
        "sprinkler", "arroseur", "irrigation", "fan", "ventilateur", "ventilo",
        "heater", "chauffage", "radiateur", "light", "lumière", "lampe",
        "siren", "sirène", "alarm", "alarme", "pump", "pompe",
        # Sensors
        "temperature", "temp", "température", "humidity", "humidité",
        "moisture", "soil", "sol", "terre", "light level", "luminosity",
        "water level", "niveau eau",
        # Actions
        "turn on", "turn off", "activate", "activer", "allumer", "éteindre",
        "start", "stop", "enable", "disable", "monitor", "surveiller",
        # Conditions
        "hot", "cold", "chaud", "froid", "dry", "sec", "wet", "humide",
        "bright", "dark", "sombre", "clair",
        # Agriculture terms
        "plant", "plante", "farm", "ferme", "greenhouse", "serre",
        "garden", "jardin", "crop", "culture", "field", "champ"
    ]
    
    has_iot_keyword = any(kw in prompt_lower for kw in all_iot_keywords)
    
    if not has_iot_keyword:
        return {
            "is_valid": False,
            "error_message": "This request doesn't seem related to agricultural IoT automation. Please describe an action for your smart farm."
        }
    
    # Split prompt into potential multiple commands
    # Split by ' and ', ' et ', ' then ', ' puis ', ',', ' but ', ' mais '
    splitters = [" and ", " et ", " then ", " puis ", ",", " but ", " mais "]
    
    # Normalize with temporary placeholder
    temp_prompt = prompt
    for s in splitters:
        temp_prompt = temp_prompt.replace(s, " ||| ")
    
    sub_prompts = [p.strip() for p in temp_prompt.split(" ||| ") if p.strip()]
    
    intents = []
    
    last_action = "turn_on" # Default start
    
    for sub_prompt in sub_prompts:
        # Pass the last seen action as default for this chunk
        intent = parse_single_intent(sub_prompt, default_action=last_action)
        if intent:
            intents.append(intent)
            # Update last_action for the next chunk if this one had a specific action detected
            # We need to know if the action was EXPLICITLY in this chunk or just defaulted.
            # Ideally parse_single_intent returns metadata, but for now let's just trust the result
            last_action = intent['action']
            
    if not intents:
         return {
            "is_valid": False,
            "error_message": "Could not understand commands."
        }
        
    return {
        "is_valid": True,
        "intents": intents
    }


def parse_single_intent(prompt: str, default_action: str = "turn_on") -> dict:
    """Helper to parse a single command string"""
    prompt_lower = prompt.lower()
    
    # Detect action (multi-language)
    action = None
    off_keywords = ["turn off", "turn of", "stop", "disable", "off", "éteindre", "arrêter", "désactiver", "apagar", "parar"]
    monitor_keywords = ["monitor", "check", "surveiller", "vérifier", "verificar"]
    on_keywords = ["turn on", "start", "enable", "activate", "allumer", "activer"]

    for kw in off_keywords:
        if kw in prompt_lower:
            action = "turn_off"
            break
    if not action:
        for kw in monitor_keywords:
            if kw in prompt_lower:
                action = "monitor"
                break
    if not action:
        for kw in on_keywords:
            if kw in prompt_lower:
                action = "turn_on"
                break
            
    # If no explicit action found, use the inherited default
    if not action:
        action = default_action
    
    # Detect device (multi-language with aliases)
    device_map = {
        "sprinkler": ["sprinkler", "arroseur", "irrigation", "water", "eau", "riego"],
        "fan": ["fan", "ventilateur", "ventilo", "cooling", "refroidir", "ventilador", "cool"],
        "heater": ["heater", "chauffage", "radiateur", "heating", "chauffer", "calentador", "heat", "warm"],
        "light": ["light", "lumière", "lampe", "lamp", "éclairage", "luz"],
        "siren": ["siren", "sirène", "alarm", "alarme", "alert", "alerte"],
        "pump": ["pump", "pompe", "bomba"]
    }
    
    device = None
    for dev, keywords in device_map.items():
        for kw in keywords:
            if kw in prompt_lower:
                device = dev
                break
        if device:
            break
    
    # Detect sensor (multi-language)
    sensor_map = {
        "temperature": ["temperature", "temp", "température", "degree", "degré", "celsius", "hot", "cold", "chaud", "froid", "caliente", "frio"],
        "humidity": ["humidity", "humidité", "humid", "humedad"],
        "moisture": ["moisture", "soil", "sol", "terre", "dry", "sec", "wet", "humide"],
        "light_level": ["light level", "luminosity", "luminosité", "bright", "dark", "sombre", "clair"],
        "water_level": ["water level", "niveau eau", "water sensor"]
    }
    
    sensor = None
    for sens, keywords in sensor_map.items():
        for kw in keywords:
            if kw in prompt_lower:
                sensor = sens
                break
        if sensor:
            break
    
    # Infer device from sensor if not specified
    if not device and sensor:
        sensor_device_map = {
            "temperature": "heater" if any(w in prompt_lower for w in ["cold", "froid", "below", "moins", "under"]) else "fan",
            "humidity": "sprinkler",
            "moisture": "sprinkler",
            "light_level": "light",
            "water_level": "pump"
        }
        device = sensor_device_map.get(sensor, "fan")
    
    # Default device if we have IoT context but no specific device
    if not device:
        # If we can't find a device, this single intent might just be noise or "and", skip it
        # But for fallback we'll default to fan to be safe? 
        # Better: return None if essentially empty/nonsense
        return None
    
    # Detect condition
    condition = None
    below_keywords = ["below", "under", "less", "drops", "moins", "inférieur", "sous", "bajo", "<"]
    above_keywords = ["above", "over", "exceed", "more", "plus", "supérieur", "dépasse", "sobre", ">"]
    
    for kw in below_keywords:
        if kw in prompt_lower:
            condition = "below"
            break
    if not condition:
        for kw in above_keywords:
            if kw in prompt_lower:
                condition = "above"
                break
    
    # Detect threshold (any number in the prompt)
    threshold = None
    numbers = re.findall(r'\d+\.?\d*', prompt)
    if numbers:
        threshold = float(numbers[0]) if '.' in numbers[0] else int(numbers[0])
    
    # Default thresholds if condition but no number
    if condition and not threshold:
        default_thresholds = {
            "temperature": 25 if condition == "above" else 15,
            "humidity": 60 if condition == "above" else 30,
            "moisture": 60 if condition == "above" else 30,
            "light_level": 50 if condition == "above" else 20,
        }
        threshold = default_thresholds.get(sensor, 30)
    
    # Detect unit
    unit = None
    if sensor == "temperature":
        unit = "fahrenheit" if "fahrenheit" in prompt_lower or "°f" in prompt_lower else "celsius"
    elif sensor in ["humidity", "moisture", "light_level"]:
        unit = "percent"
    
    return {
        "action": action,
        "device": device,
        "sensor": sensor,
        "condition": condition,
        "threshold": threshold,
        "unit": unit
    }


def extract_intent(prompt: str) -> dict:
    """
    Extract structured IoT intent from natural language.
    Uses a cascade: Ollama → Gemini → Intelligent Fallback
    """
    result = None
    
    # Try Ollama first (local, free)
    if USE_OLLAMA:
        print("[AI Service] Trying Ollama...")
        result = extract_with_ollama(prompt)
    
    # Try Gemini as fallback
    if not result and GEMINI_API_KEY:
        print("[AI Service] Trying Gemini...")
        result = extract_with_gemini(prompt)
    
    # Use intelligent fallback
    if not result:
        print("[AI Service] Using intelligent fallback...")
        result = extract_with_fallback(prompt)
    
    return result


if __name__ == "__main__":
    # Test with various prompts
    test_prompts = [
        "Turn on the fan if temperature exceeds 25 degrees",
        "allumer le ventilateur si la température dépasse 28°C",
        "water the plants when soil is dry",
        "it's too hot",
        "éteindre la lumière",
        "temperature below 13 turn heater on",
        "activer arrosage humidité < 30",
    ]
    
    for prompt in test_prompts:
        print(f"\n{'='*60}")
        print(f"Prompt: {prompt}")
        result = extract_intent(prompt)
        print(f"Result: {json.dumps(result, indent=2)}")
