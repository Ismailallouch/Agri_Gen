import { useState, useMemo } from 'react'
import { Copy, Check, Download, FileCode } from 'lucide-react'

// Custom syntax highlighting for Python
function highlightPython(code) {
    if (!code || typeof code !== 'string') {
        return [{ html: '', index: 0 }]
    }

    const lines = code.split('\n')

    return lines.map((line, index) => {
        // Skip empty processing for empty lines
        if (!line.trim()) {
            return { html: '', index }
        }

        let highlighted = line
            // Escape HTML first
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            // Comments first
            .replace(/(#.*)$/gm, '<span class="token-comment">$1</span>')
            // Strings (single and double quotes)
            .replace(/(&quot;(?:[^&]|\\.)*&quot;|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')/g, '<span class="token-string">$1</span>')
            // Keywords
            .replace(/\b(from|import|def|class|if|elif|else|while|for|in|return|True|False|None|and|or|not|try|except|finally|with|as|global|nonlocal|lambda|yield|break|continue|pass)\b/g, '<span class="token-keyword">$1</span>')
            // Built-in functions
            .replace(/\b(print|str|int|float|len|range|list|dict|tuple|set|open|type|isinstance|hasattr|getattr|setattr)\b(?=\()/g, '<span class="token-function">$1</span>')
            // Numbers
            .replace(/\b(\d+\.?\d*)\b/g, '<span class="token-number">$1</span>')

        return { html: highlighted, index }
    })
}

function CodeDisplay({ code }) {
    const [copied, setCopied] = useState(false)

    // Debug log
    console.log('[CodeDisplay] Received code:', code ? `${code.length} chars` : 'empty')

    const highlightedLines = useMemo(() => {
        try {
            return highlightPython(code || '')
        } catch (e) {
            console.error('[CodeDisplay] Highlight error:', e)
            return code ? code.split('\n').map((line, index) => ({ html: line, index })) : []
        }
    }, [code])

    const handleCopy = async () => {
        await navigator.clipboard.writeText(code)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
    }

    const handleDownload = () => {
        const blob = new Blob([code], { type: 'text/plain' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'agrigen_firmware.py'
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
    }

    // Show placeholder if no code
    if (!code) {
        return (
            <div className="terminal-window">
                <div className="terminal-header">
                    <div className="terminal-dot red" />
                    <div className="terminal-dot yellow" />
                    <div className="terminal-dot green" />
                    <div className="terminal-title">No code generated</div>
                </div>
                <div className="terminal-body p-8 text-center text-gray-500">
                    Waiting for firmware compilation...
                </div>
            </div>
        )
    }

    return (
        <div className="terminal-window">
            {/* Terminal Header */}
            <div className="terminal-header">
                <div className="terminal-dot red" />
                <div className="terminal-dot yellow" />
                <div className="terminal-dot green" />
                <div className="terminal-title">
                    <FileCode className="w-3 h-3 inline mr-2" />
                    agrigen_firmware.py — Cisco Packet Tracer SBC
                </div>

                {/* Action Buttons */}
                <div className="flex gap-2 ml-auto">
                    <button
                        onClick={handleCopy}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-bio-300/10 hover:bg-bio-300/20 text-bio-300 text-xs font-medium transition-all"
                    >
                        {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                        {copied ? 'Copied!' : 'Copy'}
                    </button>
                    <button
                        onClick={handleDownload}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-data-500/10 hover:bg-data-500/20 text-data-400 text-xs font-medium transition-all"
                    >
                        <Download className="w-3.5 h-3.5" />
                        Download
                    </button>
                </div>
            </div>

            {/* Terminal Body with Line Numbers */}
            <div className="terminal-body">
                <table className="w-full border-collapse">
                    <tbody>
                        {highlightedLines.map(({ html, index }) => (
                            <tr
                                key={index}
                                className="code-line"
                                style={{ animationDelay: `${Math.min(index * 0.02, 0.5)}s` }}
                            >
                                <td className="pr-4 text-right text-gray-600 select-none w-12 align-top font-mono text-sm">
                                    {index + 1}
                                </td>
                                <td className="border-l border-gray-800 pl-4">
                                    <pre
                                        className="whitespace-pre font-mono text-sm text-gray-300"
                                        dangerouslySetInnerHTML={{ __html: html || '&nbsp;' }}
                                    />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default CodeDisplay
