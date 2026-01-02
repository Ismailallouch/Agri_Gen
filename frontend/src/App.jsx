import { useState, useEffect } from 'react'
import axios from 'axios'
import { Zap, Loader2, Cpu, Sprout, Terminal, ChevronRight, History, Bookmark, Trash2, RotateCcw,Download  } from 'lucide-react'
import CodeDisplay from './components/CodeDisplay'

// Professional preset templates
const PRESET_TEMPLATES = [
    {
        category: "🌡️ Climate Control",
        prompts: [
            { name: "Cooling System", prompt: "Turn on the fan when temperature exceeds 28°C", icon: "❄️" },
            { name: "Heating System", prompt: "Activate the heater if temperature drops below 15°C", icon: "🔥" },
            { name: "Smart Thermostat", prompt: "Turn on heater below 18°C and fan above 26°C", icon: "🌡️" },
        ]
    },
    {
        category: "💧 Irrigation",
        prompts: [
            { name: "Soil Moisture", prompt: "Turn on sprinkler when soil moisture is below 30%", icon: "💦" },
            { name: "Humidity Control", prompt: "Activate water pump if humidity drops under 40%", icon: "💧" },
            { name: "Drought Protection", prompt: "Emergency irrigation when moisture below 15%", icon: "🚨" },
        ]
    },
    {
        category: "💡 Lighting",
        prompts: [
            { name: "Auto Lights", prompt: "Switch on lights when light level is below 20%", icon: "💡" },
            { name: "Grow Lights", prompt: "Activate grow lights if light below 30% during day", icon: "🌱" },
        ]
    },
    {
        category: "🔔 Alerts",
        prompts: [
            { name: "Heat Alert", prompt: "Trigger siren if temperature exceeds 45°C", icon: "🚨" },
            { name: "Frost Warning", prompt: "Sound alarm when temperature drops below 2°C", icon: "❄️" },
            { name: "Flood Alert", prompt: "Activate siren if water level exceeds 80%", icon: "🌊" },
        ]
    }
]

function App() {
    const [prompt, setPrompt] = useState('')
    const [generatedCode, setGeneratedCode] = useState('')
    const [intent, setIntent] = useState(null)
    const [status, setStatus] = useState('idle')
    const [error, setError] = useState('')
    const [history, setHistory] = useState([])
    const [showPresets, setShowPresets] = useState(false)
    const [showHistory, setShowHistory] = useState(false)

    // Load history from localStorage
    useEffect(() => {
        const saved = localStorage.getItem('agrigen_history')
        if (saved) {
            setHistory(JSON.parse(saved))
        }
    }, [])

    // Save to history
    const saveToHistory = (prompt, intent, code) => {
        const newEntry = {
            id: Date.now(),
            prompt,
            intent,
            code,
            timestamp: new Date().toISOString()
        }
        const newHistory = [newEntry, ...history].slice(0, 20) // Keep last 20
        setHistory(newHistory)
        localStorage.setItem('agrigen_history', JSON.stringify(newHistory))
    }

    const clearHistory = () => {
        setHistory([])
        localStorage.removeItem('agrigen_history')
    }
    const downloadFile = () => {
      const link = document.createElement("a");
      link.href = "https://res.cloudinary.com/dqfpaqz2z/raw/upload/v1767278492/Projet_cisco_2_dsvpy7.pkt";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };

    const loadFromHistory = (entry) => {
        setPrompt(entry.prompt)
        setIntent(entry.intent)
        setGeneratedCode(entry.code)
        setStatus('success')
        setShowHistory(false)
    }

    const handleCompile = async () => {
        if (!prompt.trim()) return

        setStatus('compiling')
        setError('')
        setGeneratedCode('')
        setIntent(null)

        try {
            const response = await axios.post('/api/compile', { prompt })

            if (response.data.success) {
                setGeneratedCode(response.data.code)
                setIntent(response.data.intent)
                setStatus('success')
                saveToHistory(prompt, response.data.intent, response.data.code)
            } else {
                setError(response.data.error || 'Compilation failed')
                setStatus('error')
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Connection failed')
            setStatus('error')
        }
    }

    const applyPreset = (presetPrompt) => {
        setPrompt(presetPrompt)
        setShowPresets(false)
    }

    return (
        <div className="min-h-screen relative">
            {/* Animated Topographic Background */}
            <div className="topo-background">
                <div className="topo-lines" />
                <div className="gradient-overlay" />
            </div>

            {/* Main Content */}
            <div className="relative z-10 min-h-screen flex flex-col">
                {/* Header */}
                <header className="p-6 lg:p-8 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-bio-300 to-bio-600 flex items-center justify-center glow-bio">
                            <Sprout className="w-6 h-6 text-soil-300" />
                        </div>
                        <div>
                            <h1 className="font-display text-2xl lg:text-3xl font-bold text-gradient-bio">
                                Agri-Gen
                            </h1>
                            <p className="text-sm text-gray-500 font-body">
                                No-Code IoT Firmware OS
                            </p>
                        </div>
                    </div>

                    {/* Header Actions */}
                    <div className="flex items-center gap-3">
                        <button
                            onClick={downloadFile}
                            className={`flex items-center gap-2 px-4 py-2 rounded-xl border transition-all ${showHistory ? 'bg-data-500/20 border-data-500/50 text-data-400' : 'bg-transparent border-glass-border text-gray-400 hover:text-data-400 hover:border-data-500/30'}`}
                        >
                            <Download className="w-4 h-4" />
                            <span className="hidden sm:inline">Cisco Template</span>
                            {history.length > 0 && (
                                <span className="w-5 h-5 rounded-full bg-data-500/30 text-xs flex items-center justify-center">
                                    {history.length}
                                </span>
                            )}
                        </button> 
                        <button
                            onClick={() => setShowPresets(!showPresets)}
                            className={`flex items-center gap-2 px-4 py-2 rounded-xl border transition-all ${showPresets ? 'bg-bio-300/20 border-bio-300/50 text-bio-300' : 'bg-transparent border-glass-border text-gray-400 hover:text-bio-300 hover:border-bio-300/30'}`}
                        >
                            <Bookmark className="w-4 h-4" />
                            <span className="hidden sm:inline">Templates</span>
                        </button>
                        <button
                            onClick={() => setShowHistory(!showHistory)}
                            className={`flex items-center gap-2 px-4 py-2 rounded-xl border transition-all ${showHistory ? 'bg-data-500/20 border-data-500/50 text-data-400' : 'bg-transparent border-glass-border text-gray-400 hover:text-data-400 hover:border-data-500/30'}`}
                        >
                            <History className="w-4 h-4" />
                            <span className="hidden sm:inline">History</span>
                            {history.length > 0 && (
                                <span className="w-5 h-5 rounded-full bg-data-500/30 text-xs flex items-center justify-center">
                                    {history.length}
                                </span>
                            )}
                        </button>
                       
                    </div>
                </header>

                {/* Presets Panel */}
                {showPresets && (
                    <div className="mx-6 lg:mx-8 mb-6 glass-panel p-6 animate-fade-in">
                        <h3 className="font-display text-lg font-semibold text-white mb-4 flex items-center gap-2">
                            <Bookmark className="w-5 h-5 text-bio-300" />
                            Preset Templates
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                            {PRESET_TEMPLATES.map((category, idx) => (
                                <div key={idx} className="space-y-2">
                                    <h4 className="text-sm font-medium text-gray-400">{category.category}</h4>
                                    {category.prompts.map((preset, pidx) => (
                                        <button
                                            key={pidx}
                                            onClick={() => applyPreset(preset.prompt)}
                                            className="w-full text-left p-3 rounded-lg bg-soil-200/50 border border-glass-border hover:border-bio-300/30 hover:bg-bio-300/5 transition-all group"
                                        >
                                            <div className="flex items-center gap-2">
                                                <span>{preset.icon}</span>
                                                <span className="text-sm text-gray-300 group-hover:text-bio-300">{preset.name}</span>
                                            </div>
                                        </button>
                                    ))}
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* History Panel */}
                {showHistory && (
                    <div className="mx-6 lg:mx-8 mb-6 glass-panel p-6 animate-fade-in">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-display text-lg font-semibold text-white flex items-center gap-2">
                                <History className="w-5 h-5 text-data-400" />
                                Recent Commands
                            </h3>
                            {history.length > 0 && (
                                <button
                                    onClick={clearHistory}
                                    className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-red-400 hover:bg-red-500/10 transition-all text-sm"
                                >
                                    <Trash2 className="w-4 h-4" />
                                    Clear All
                                </button>
                            )}
                        </div>
                        {history.length === 0 ? (
                            <p className="text-gray-500 text-sm text-center py-8">No history yet. Start compiling!</p>
                        ) : (
                            <div className="space-y-2 max-h-60 overflow-y-auto">
                                {history.map((entry) => (
                                    <button
                                        key={entry.id}
                                        onClick={() => loadFromHistory(entry)}
                                        className="w-full text-left p-3 rounded-lg bg-soil-200/50 border border-glass-border hover:border-data-500/30 hover:bg-data-500/5 transition-all group"
                                    >
                                        <div className="flex items-center justify-between">
                                            <p className="text-sm text-gray-300 group-hover:text-data-400 truncate flex-1">
                                                {entry.prompt}
                                            </p>
                                            <div className="flex items-center gap-2 ml-4">
                                                <span className="text-xs text-gray-600">
                                                    {new Date(entry.timestamp).toLocaleTimeString()}
                                                </span>
                                                <RotateCcw className="w-4 h-4 text-data-400 opacity-0 group-hover:opacity-100" />
                                            </div>
                                        </div>
                                        {entry.intent && (
                                            <div className="flex gap-2 mt-2">
                                                <span className="text-xs px-2 py-0.5 rounded bg-bio-300/20 text-bio-300">
                                                    {entry.intent.device}
                                                </span>
                                                {entry.intent.threshold && (
                                                    <span className="text-xs px-2 py-0.5 rounded bg-data-500/20 text-data-400">
                                                        {entry.intent.condition} {entry.intent.threshold}
                                                    </span>
                                                )}
                                            </div>
                                        )}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>
                )}

                {/* Command Center - Split Layout */}
                <main className="flex-1 p-4 lg:p-8 lg:pt-0">
                    <div className="command-center flex flex-col lg:flex-row gap-6 h-full max-w-[1800px] mx-auto">

                        {/* Left Panel - Input */}
                        <div className="left-panel w-full lg:w-[45%] lg:sticky lg:top-8 lg:self-start">
                            <div className="command-interface-panel relative overflow-hidden">
                                {/* Animated border glow effect */}
                                <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-bio-300/20 via-transparent to-data-500/20 opacity-50 blur-xl animate-pulse-slow" />

                                <div className="relative glass-panel p-6 lg:p-8 h-full border-2 border-bio-300/10 hover:border-bio-300/20 transition-all duration-500">
                                    {/* Decorative corner accents */}
                                    <div className="absolute top-0 left-0 w-16 h-16 border-l-2 border-t-2 border-bio-300/30 rounded-tl-3xl" />
                                    <div className="absolute bottom-0 right-0 w-16 h-16 border-r-2 border-b-2 border-bio-300/30 rounded-br-3xl" />

                                    {/* Panel Header - Enhanced */}
                                    <div className="flex items-center justify-between mb-6">
                                        <div className="flex items-center gap-4">
                                            <div className="relative">
                                                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-bio-300/20 to-bio-300/5 flex items-center justify-center border border-bio-300/20">
                                                    <Terminal className="w-6 h-6 text-bio-300" />
                                                </div>
                                                {/* Pulse indicator */}
                                                <div className="absolute -top-1 -right-1 w-3 h-3 bg-bio-300 rounded-full animate-pulse shadow-glow-bio" />
                                            </div>
                                            <div>
                                                <h2 className="font-display text-xl font-bold text-gradient-bio">
                                                    Command Interface
                                                </h2>
                                                <div className="flex items-center gap-2 mt-1">
                                                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-bio-300/10 border border-bio-300/20 text-[10px] text-bio-300 font-medium">
                                                        <span className="w-1.5 h-1.5 bg-bio-300 rounded-full animate-pulse" />
                                                        AI-Powered
                                                    </span>
                                                    <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-data-500/10 border border-data-500/20 text-[10px] text-data-400 font-medium">
                                                        Multi-lang
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                        {/* Character count indicator */}
                                        {prompt.length > 0 && (
                                            <div className="text-xs text-gray-500 bg-soil-200/50 px-3 py-1.5 rounded-lg border border-glass-border">
                                                {prompt.length} <span className="text-bio-300/60">chars</span>
                                            </div>
                                        )}
                                    </div>

                                    {/* Supercomputer Input - Enhanced */}
                                    <div className="relative group">
                                        <div className="absolute inset-0 bg-gradient-to-r from-bio-300/5 to-data-500/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                                        <textarea
                                            value={prompt}
                                            onChange={(e) => setPrompt(e.target.value)}
                                            placeholder="Describe your automation in any language...

Examples:
• Turn on the fan when temperature exceeds 28°C
• Allumer l'arroseur si humidité < 30%
• Activar riego cuando humedad < 25%"
                                            className="supercomputer-input relative z-10"
                                            disabled={status === 'compiling'}
                                        />
                                    </div>

                                    {/* Quick Tips */}
                                    <div className="flex flex-wrap gap-2 mt-4">
                                        <span className="text-[10px] text-gray-500 uppercase tracking-wider">Try:</span>
                                        {['🌡️ Temperature', '💧 Humidity', '💡 Light'].map((tip, idx) => (
                                            <button
                                                key={idx}
                                                className="px-2.5 py-1 rounded-lg bg-soil-200/30 border border-glass-border text-xs text-gray-400 hover:text-bio-300 hover:border-bio-300/30 hover:bg-bio-300/5 transition-all"
                                                onClick={() => {
                                                    const tips = [
                                                        'Turn on fan when temperature > 28°C',
                                                        'Activate irrigation when humidity < 30%',
                                                        'Turn on lights when light level < 20%'
                                                    ];
                                                    setPrompt(tips[idx]);
                                                }}
                                            >
                                                {tip}
                                            </button>
                                        ))}
                                    </div>

                                    {/* Compile Button - Enhanced */}
                                    <button
                                        onClick={handleCompile}
                                        disabled={!prompt.trim() || status === 'compiling'}
                                        className={`compile-button mt-6 group ${status === 'compiling' ? 'compiling' : ''}`}
                                    >
                                        {status === 'compiling' ? (
                                            <>
                                                <Loader2 className="w-5 h-5 animate-spin" />
                                                <span>Processing with AI...</span>
                                                <span className="ml-2 text-xs opacity-70">analyzing intent</span>
                                            </>
                                        ) : (
                                            <>
                                                <div className="relative">
                                                    <Zap className="w-5 h-5 group-hover:scale-110 transition-transform" />
                                                    <div className="absolute inset-0 bg-white/20 rounded-full blur-md opacity-0 group-hover:opacity-100 transition-opacity" />
                                                </div>
                                                <span>Compile Firmware</span>
                                                <ChevronRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                                            </>
                                        )}
                                    </button>

                                    {/* Error Display - Enhanced with better design */}
                                    {status === 'error' && (
                                        <div className="mt-4 p-5 rounded-2xl bg-gradient-to-br from-amber-500/10 to-orange-500/5 border border-amber-500/30 backdrop-blur-sm relative overflow-hidden">
                                            {/* Decorative glow */}
                                            <div className="absolute top-0 right-0 w-24 h-24 bg-amber-500/10 rounded-full blur-2xl" />

                                            <div className="relative z-10">
                                                <div className="flex items-start gap-4">
                                                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-500/20 to-orange-500/20 flex items-center justify-center flex-shrink-0 border border-amber-500/20">
                                                        <span className="text-2xl">🌱</span>
                                                    </div>
                                                    <div className="flex-1">
                                                        <p className="text-sm font-semibold text-amber-400 mb-1">Not an IoT Command</p>
                                                        <p className="text-sm text-gray-300 leading-relaxed">{error}</p>
                                                    </div>
                                                </div>

                                                {/* Suggestions */}
                                                <div className="mt-4 pt-4 border-t border-amber-500/20">
                                                    <p className="text-xs text-gray-500 uppercase tracking-wider mb-3">Try these examples:</p>
                                                    <div className="flex flex-wrap gap-2">
                                                        {[
                                                            '🌡️ "Turn on fan if temp > 28°C"',
                                                            '💧 "Irrigate when moisture < 30%"',
                                                            '💡 "Lights on when dark"'
                                                        ].map((example, idx) => (
                                                            <button
                                                                key={idx}
                                                                onClick={() => {
                                                                    const prompts = [
                                                                        'Turn on the fan when temperature exceeds 28°C',
                                                                        'Activate sprinkler when soil moisture drops below 30%',
                                                                        'Turn on lights when light level is below 20%'
                                                                    ];
                                                                    setPrompt(prompts[idx]);
                                                                    setStatus('idle');
                                                                    setError('');
                                                                }}
                                                                className="px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300 hover:bg-amber-500/20 hover:border-amber-500/30 transition-all"
                                                            >
                                                                {example}
                                                            </button>
                                                        ))}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Right Panel - Output */}
                        <div className="right-panel w-full lg:w-[55%] flex flex-col gap-6">
                            {/* Scanning Status - Premium Animation */}
                            {status === 'compiling' && (
                                <div className="glass-panel p-8 relative overflow-hidden">
                                    {/* Scanning line animation */}
                                    <div className="absolute inset-0 overflow-hidden">
                                        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-bio-300 to-transparent animate-scan-horizontal" />
                                        <div className="absolute inset-0 bg-gradient-to-b from-bio-300/5 to-transparent animate-scan-vertical" />
                                    </div>

                                    {/* Main content */}
                                    <div className="relative z-10 flex flex-col items-center text-center">
                                        {/* Animated icon */}
                                        <div className="relative mb-6">
                                            {/* Outer ring */}
                                            <div className="w-24 h-24 rounded-full border-2 border-data-500/30 animate-spin-slow" />
                                            {/* Middle ring */}
                                            <div className="absolute inset-2 rounded-full border-2 border-bio-300/40 animate-spin-reverse" />
                                            {/* Inner core */}
                                            <div className="absolute inset-4 rounded-full bg-gradient-to-br from-data-500/20 to-bio-300/20 flex items-center justify-center">
                                                <Cpu className="w-8 h-8 text-bio-300 animate-pulse" />
                                            </div>
                                            {/* Orbiting dots */}
                                            <div className="absolute inset-0 animate-spin-slow">
                                                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-2 h-2 rounded-full bg-bio-300 shadow-glow-bio" />
                                            </div>
                                            <div className="absolute inset-0 animate-spin-reverse" style={{ animationDuration: '4s' }}>
                                                <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-2 h-2 rounded-full bg-data-500 shadow-glow-data" />
                                            </div>
                                        </div>

                                        {/* Text */}
                                        <h3 className="font-display text-xl font-semibold text-bio-300 mb-2">
                                            Analyzing Intent
                                            <span className="inline-flex ml-1">
                                                <span className="animate-bounce-dot">.</span>
                                                <span className="animate-bounce-dot" style={{ animationDelay: '0.2s' }}>.</span>
                                                <span className="animate-bounce-dot" style={{ animationDelay: '0.4s' }}>.</span>
                                            </span>
                                        </h3>
                                        <p className="text-gray-500 text-sm mb-4">
                                            AI is processing your natural language command
                                        </p>

                                        {/* Progress steps */}
                                        <div className="flex items-center gap-3 text-xs">
                                            <div className="flex items-center gap-2 text-bio-300">
                                                <div className="w-2 h-2 rounded-full bg-bio-300 animate-pulse" />
                                                <span>Parsing</span>
                                            </div>
                                            <div className="w-8 h-px bg-gray-700" />
                                            <div className="flex items-center gap-2 text-gray-500">
                                                <div className="w-2 h-2 rounded-full bg-gray-600" />
                                                <span>Extracting</span>
                                            </div>
                                            <div className="w-8 h-px bg-gray-700" />
                                            <div className="flex items-center gap-2 text-gray-500">
                                                <div className="w-2 h-2 rounded-full bg-gray-600" />
                                                <span>Compiling</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Intent Display */}
                            {intent && (
                                <div className="glass-panel p-6">
                                    <div className="flex items-center gap-3 mb-4">
                                        <div className="w-10 h-10 rounded-xl bg-data-500/10 flex items-center justify-center">
                                            <Cpu className="w-5 h-5 text-data-400" />
                                        </div>
                                        <h3 className="font-display font-semibold text-white">
                                            Extracted Intent
                                        </h3>
                                    </div>
                                    <div className="intent-grid">
                                        {Object.entries(intent).map(([key, value]) => (
                                            value !== null && (
                                                <div key={key} className="intent-card">
                                                    <p className="intent-label">{key}</p>
                                                    <p className="intent-value">{String(value)}</p>
                                                </div>
                                            )
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Code Output */}
                            {generatedCode && (
                                <div className="glass-panel-intense p-1">
                                    <CodeDisplay code={generatedCode} />
                                </div>
                            )}

                            {/* Empty State - Premium Design */}
                            {status === 'idle' && !generatedCode && (
                                <div className="empty-state-panel relative overflow-hidden">
                                    {/* Background effects */}
                                    <div className="absolute inset-0 bg-gradient-radial from-bio-300/5 via-transparent to-transparent" />
                                    <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-bio-300/10 rounded-full blur-3xl animate-pulse-slow" />
                                    <div className="absolute bottom-1/4 right-1/4 w-24 h-24 bg-data-500/10 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />

                                    {/* Floating particles */}
                                    <div className="absolute inset-0 overflow-hidden">
                                        <div className="floating-particle particle-1" />
                                        <div className="floating-particle particle-2" />
                                        <div className="floating-particle particle-3" />
                                    </div>

                                    <div className="glass-panel p-8 lg:p-12 flex flex-col items-center justify-center text-center min-h-[450px] relative z-10 border-2 border-bio-300/10">
                                        {/* Main icon with orbital animation */}
                                        <div className="relative mb-8">
                                            {/* Outer orbital ring */}
                                            <div className="absolute inset-[-20px] rounded-full border border-dashed border-bio-300/20 animate-spin-slow" style={{ animationDuration: '20s' }} />
                                            {/* Inner orbital ring */}
                                            <div className="absolute inset-[-10px] rounded-full border border-bio-300/10 animate-spin-reverse" style={{ animationDuration: '15s' }} />

                                            {/* Main icon container */}
                                            <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-bio-300/20 to-bio-300/5 border-2 border-bio-300/20 flex items-center justify-center animate-float shadow-glow-bio-soft">
                                                <Sprout className="w-12 h-12 text-bio-300" />
                                            </div>

                                            {/* Orbiting dot */}
                                            <div className="absolute inset-[-20px] animate-spin-slow" style={{ animationDuration: '8s' }}>
                                                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-2 h-2 bg-bio-300 rounded-full shadow-glow-bio" />
                                            </div>
                                        </div>

                                        {/* Status badge */}
                                        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-bio-300/10 border border-bio-300/20 mb-4">
                                            <span className="w-2 h-2 bg-bio-300 rounded-full animate-pulse" />
                                            <span className="text-sm font-medium text-bio-300">System Ready</span>
                                        </div>

                                        <h3 className="font-display text-2xl font-bold text-white mb-3">
                                            Ready to Compile
                                        </h3>
                                        <p className="text-gray-400 max-w-md mb-8 leading-relaxed">
                                            Enter a command or select a template to generate
                                            <span className="text-bio-300 font-medium"> Python firmware </span>
                                            for your Cisco Packet Tracer IoT simulation.
                                        </p>

                                        {/* Action buttons */}
                                        <div className="flex flex-col sm:flex-row gap-3">
                                            <button
                                                onClick={() => setShowPresets(true)}
                                                className="group flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-bio-300/20 to-bio-300/10 border border-bio-300/30 text-bio-300 hover:from-bio-300/30 hover:to-bio-300/20 hover:border-bio-300/50 transition-all duration-300"
                                            >
                                                <Bookmark className="w-5 h-5 group-hover:scale-110 transition-transform" />
                                                <span className="font-medium">Browse Templates</span>
                                            </button>
                                            <button
                                                onClick={() => setShowHistory(true)}
                                                className="group flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-soil-200/30 border border-glass-border text-gray-400 hover:text-data-400 hover:border-data-500/30 hover:bg-data-500/10 transition-all duration-300"
                                            >
                                                <History className="w-5 h-5 group-hover:scale-110 transition-transform" />
                                                <span className="font-medium">View History</span>
                                            </button>
                                        </div>

                                        {/* Quick stats */}
                                        <div className="flex items-center justify-center gap-6 mt-8 pt-8 border-t border-glass-border w-full max-w-sm">
                                            <div className="text-center">
                                                <p className="text-2xl font-bold text-bio-300">{history.length}</p>
                                                <p className="text-xs text-gray-500 uppercase tracking-wider">Compiled</p>
                                            </div>
                                            <div className="w-px h-8 bg-glass-border" />
                                            <div className="text-center">
                                                <p className="text-2xl font-bold text-data-400">4</p>
                                                <p className="text-xs text-gray-500 uppercase tracking-wider">Categories</p>
                                            </div>
                                            <div className="w-px h-8 bg-glass-border" />
                                            <div className="text-center">
                                                <p className="text-2xl font-bold text-white">11</p>
                                                <p className="text-xs text-gray-500 uppercase tracking-wider">Templates</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </main>

                {/* Footer */}
                <footer className="p-6 text-center">
                    <p className="text-xs text-gray-600">
                        Powered by AI • Multi-Language Support • Compatible with Cisco Packet Tracer SBCs
                    </p>
                </footer>
            </div>
        </div>
    )
}

export default App
