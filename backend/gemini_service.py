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

# Advanced System Prompt - More flexible and intelligent (il faut l'ameliorer )
SYSTEM_PROMPT = """You are an expert IoT Automation Architect specializing in smart agriculture systems.

Your task is to understand natural language commands about farm automation and extract structured data.
You must be FLEXIBLE and INTELLIGENT in understanding user intent, even with:
- Incomplete sentences
- Different languages (English, French, Spanish, etc.)
- Informal language
- Typos or abbreviations

## IMPORTANT RULES:
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

5. Extract threshold values from any format:
   - "below 30%", "under 30", "< 30", "moins de 30" → threshold: 30

## OUTPUT FORMAT (JSON only):
{
    "action": "turn_on" | "turn_off" | "monitor" | "alert",
    "device": "sprinkler" | "fan" | "heater" | "light" | "pump" | "siren",
    "sensor": "temperature" | "humidity" | "moisture" | "light_level" | "water_level" | null,
    "condition": "above" | "below" | "equals" | null,
    "threshold": <number or null>,
    "unit": "celsius" | "fahrenheit" | "percent" | null,
    "confidence": <0.0 to 1.0>,
    "interpretation": "<brief explanation of how you understood the command>"
}

## EXAMPLES:

Input: "allumer le ventilateur si temp > 25"
Output: {"action": "turn_on", "device": "fan", "sensor": "temperature", "condition": "above", "threshold": 25, "unit": "celsius", "confidence": 0.95, "interpretation": "French command to turn on fan when temperature exceeds 25°C"}

Input: "water plants when dry"
Output: {"action": "turn_on", "device": "sprinkler", "sensor": "moisture", "condition": "below", "threshold": 30, "unit": "percent", "confidence": 0.8, "interpretation": "Interpreted 'dry' as low moisture, defaulted threshold to 30%"}

Input: "its too hot"
Output: {"action": "turn_on", "device": "fan", "sensor": "temperature", "condition": "above", "threshold": 28, "unit": "celsius", "confidence": 0.7, "interpretation": "Inferred fan activation for cooling, default threshold 28°C"}

Input: "turn off everything"
Output: {"action": "turn_off", "device": "fan", "sensor": null, "condition": null, "threshold": null, "unit": null, "confidence": 0.5, "interpretation": "Ambiguous command, defaulting to fan. User should specify device."}

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
            intent = json.loads(response_text)
            print(f"[Ollama] Extracted: {intent}")
            return intent
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
        
        intent = json.loads(response.text)
        print(f"[Gemini] Extracted: {intent}")
        return intent
        
    except Exception as e:
        print(f"[Gemini] Error: {e}")
        return None


def extract_with_fallback(prompt: str) -> dict:
    """Intelligent keyword-based fallback parser with multi-language support"""
    print("[Fallback] Using intelligent keyword parser")
    
    prompt_lower = prompt.lower()
    
    # Detect action (multi-language)
    action = "turn_on"
    off_keywords = ["turn off", "stop", "disable", "off", "éteindre", "arrêter", "désactiver", "apagar", "parar"]
    monitor_keywords = ["monitor", "check", "surveiller", "vérifier", "verificar"]
    
    for kw in off_keywords:
        if kw in prompt_lower:
            action = "turn_off"
            break
    for kw in monitor_keywords:
        if kw in prompt_lower:
            action = "monitor"
            break
    
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
    
    # Default device
    if not device:
        device = "fan"
    
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
        "unit": unit,
        "confidence": 0.6,
        "interpretation": f"Parsed using keyword matching: {action} {device}" + (f" when {sensor} {condition} {threshold}" if condition else "")
    }


def extract_intent(prompt: str) -> dict:
    """
    Extract structured IoT intent from natural language.
    Uses a cascade: Ollama → Gemini → Intelligent Fallback
    """
    intent = None
    
    # Try Ollama first (local, free)
    if USE_OLLAMA:
        print("[AI Service] Trying Ollama...")
        intent = extract_with_ollama(prompt)
    
    # Try Gemini as fallback
    if not intent and GEMINI_API_KEY:
        print("[AI Service] Trying Gemini...")
        intent = extract_with_gemini(prompt)
    
    # Use intelligent fallback
    if not intent:
        print("[AI Service] Using intelligent fallback...")
        intent = extract_with_fallback(prompt)
    
    # Remove fields we don't need for compilation
    if intent:
        intent.pop('confidence', None)
        intent.pop('interpretation', None)
    
    return intent


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
