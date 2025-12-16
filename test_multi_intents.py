
import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from gemini_service import extract_with_fallback

def test_context_carryover():
    print("Testing Context Carry-Over...")
    
    prompt = "turn of light and fan and sprinkler"
    print(f"Prompt: {prompt}")
    
    intent = extract_with_fallback(prompt)
    
    print("\nExtracted Intent:")
    print(json.dumps(intent, indent=2))
    
    intents = intent.get('intents', [])
    if len(intents) < 3:
        print("FAILED: Did not extract 3 intents.")
        return

    actions = [i['action'] for i in intents]
    print(f"Actions found: {actions}")
    
    if all(a == 'turn_off' for a in actions):
        print("\nSUCCESS: All actions are 'turn_off'.")
    else:
        print("\nFAILED: Some actions defaulted incorrectly.")

    # Test switching back to ON
    print("\n\nTesting switching actions...")
    prompt2 = "turn off light and fan but turn on sprinkler"
    intent2 = extract_with_fallback(prompt2)
    actions2 = [i['action'] for i in intent2.get('intents', [])]
    print(f"Prompt: {prompt2}")
    print(f"Actions: {actions2}")
    
    if actions2 == ['turn_off', 'turn_off', 'turn_on']:
         print("SUCCESS: Context switched correctly.")
    else:
         print("FAILED: Context switch failed.")

if __name__ == "__main__":
    test_context_carryover()
