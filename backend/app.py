"""
Agri-Gen Backend - Flask API Server
Converts natural language to IoT firmware for Cisco Packet Tracer SBCs
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_service import extract_intent
from firmware_compiler import compile_firmware
import os

app = Flask(__name__)
CORS(app)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Agri-Gen API"})


@app.route('/api/compile', methods=['POST'])
def compile_endpoint():
    """
    Main endpoint: Converts natural language prompt to Python firmware
    
    Request Body:
        { "prompt": "Turn on the sprinkler if moisture is below 30%" }
    
    Response:
        { "success": true, "code": "...", "intent": {...} }
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'prompt' in request body"
            }), 400
        
        prompt = data['prompt']
        
        # Step 1: Extract intent from natural language using Gemini
        intent = extract_intent(prompt)
        
        if not intent:
            return jsonify({
                "success": False,
                "error": "Failed to extract intent from prompt"
            }), 500
        
        # Step 2: Check if the prompt is valid (related to agriculture/IoT)
        if intent.get('is_valid') == False:
            return jsonify({
                "success": False,
                "error": intent.get('error_message', "Cette demande n'est pas liée à l'automatisation IoT agricole."),
                "is_invalid_prompt": True
            }), 400
        
        # Step 3: Compile Python firmware using Jinja2
        # Now supporting multi-intent structure
        firmware_code = compile_firmware(intent)
        
        return jsonify({
            "success": True,
            "code": firmware_code,
            "intent": intent
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
