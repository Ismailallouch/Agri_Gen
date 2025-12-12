# 🌱 Agri-Gen

**No-Code IoT Firmware Generator for Smart Agriculture**

Transform natural language into Python firmware for Cisco Packet Tracer IoT simulations.

---

## ✨ Features

### 🧠 Intelligent AI Understanding
- **Multi-language**: English, Français, Español
- **Flexible syntax**: "temp > 30 fan on" works!
- **Smart inference**: "it's too hot" → activates fan
- **Default values**: Missing threshold? AI picks logical defaults

### 📚 Preset Templates
| Category | Examples |
|----------|----------|
| 🌡️ Climate Control | Cooling, Heating, Thermostat |
| 💧 Irrigation | Moisture, Humidity, Drought protection |
| 💡 Lighting | Auto lights, Grow lights |
| 🔔 Alerts | Heat, Frost, Flood warnings |

### 📜 Command History
- Auto-saves last 20 compilations
- Persists in browser (localStorage)
- One-click restore
- Visual tags for device & condition

### 🎨 Premium UI
- Organic Futurism design
- Animated topographic background
- Glassmorphism panels
- VS Code-style code display
- Syntax highlighting
- Copy & Download buttons

---

## 📡 Supported Hardware

| Sensors (Input) | Actuators (Output) |
|-----------------|-------------------|
| 🌡️ Temperature (Pin 0) | 💦 Sprinkler (Pin 3) |
| 🚰 Water Level (Pin 1) | � Heater (Pin 4) |
| � Humidity (Pin 2) | ❄️ Fan (Pin 5) |
| | 🔔 Siren (Pin 6) |
| | 💡 Light (Pin 7) |
| | 📺 LCD (Pin 8) |

---

## 🚀 Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open: **http://localhost:5173**

---

## ⚙️ Configuration

Create `backend/.env`:

```env
# Use Ollama (local, free)
USE_OLLAMA=true
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Or use Gemini (cloud)
# USE_OLLAMA=false
# GEMINI_API_KEY=your_key_here
```

---

## 💬 Example Commands

```
Turn on the fan when temperature exceeds 28°C
Allumer l'arroseur si humidité < 30%
Water plants when soil is dry
it's too hot → AI infers: fan + temp above 28
éteindre la lumière
Alert if temperature exceeds 40 degrees
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + Vite + Tailwind CSS |
| Backend | Flask + Jinja2 |
| AI | Ollama (Llama 3) / Google Gemini |
| Target | Cisco Packet Tracer SBC |

---

## 📁 Project Structure

```
Agri_Gen/
├── backend/
│   ├── app.py              # Flask API
│   ├── gemini_service.py   # AI intent extraction
│   ├── firmware_compiler.py # Jinja2 code generation
│   └── templates/
│       └── iot_master.py.jinja
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main component
│   │   ├── components/
│   │   │   └── CodeDisplay.jsx
│   │   └── index.css       # Styles
│   └── package.json
└── README.md
```

---


