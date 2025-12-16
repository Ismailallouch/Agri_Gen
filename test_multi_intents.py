
import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from gemini_service import extract_with_fallback, SYSTEM_PROMPT
from firmware_compiler import compile_firmware

def test_compound_command():
    print("Testing Compound Command with Typo...")
    
    prompt = "Turn on fan when too hot and turn of light"
    print(f"Prompt: {prompt}")
    
    intent = extract_with_fallback(prompt)
    
    print("\nExtracted Intent:")
    print(json.dumps(intent, indent=2))
    
    if not intent['is_valid'] or len(intent.get('intents', [])) < 2:
        print("FAILED: Did not extract multiple intents.")
        return
        
    intent2 = intent['intents'][1]
    if intent2['action'] == 'turn_off' and intent2['device'] == 'light':
        print("\nSUCCESS: 'turn of' correctly interpreted as 'turn_off' light.")
    else:
        print(f"\nFAILED: 'turn of' interpreted as {intent2['action']} {intent2['device']}")

if __name__ == "__main__":
    test_compound_command()
