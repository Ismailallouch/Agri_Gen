/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Organic Futurism - Premium Palette
                soil: {
                    50: '#1a1f1c',
                    100: '#161a17',
                    200: '#121614',
                    300: '#0F1210', // Main background
                    400: '#0b0e0c',
                    500: '#080a09',
                    900: '#030403',
                },
                bio: {
                    50: '#f4ffe6',
                    100: '#e5ffc9',
                    200: '#d4ff99',
                    300: '#C1FF72', // Bio-luminescent green accent
                    400: '#a8e85c',
                    500: '#8fd446',
                    600: '#6bb32e',
                    700: '#4f8c22',
                },
                data: {
                    50: '#eff6ff',
                    100: '#dbeafe',
                    200: '#bfdbfe',
                    300: '#93c5fd',
                    400: '#60a5fa',
                    500: '#3B82F6', // Data blue
                    600: '#2563eb',
                    700: '#1d4ed8',
                },
                glass: {
                    light: 'rgba(255, 255, 255, 0.05)',
                    medium: 'rgba(255, 255, 255, 0.08)',
                    border: 'rgba(193, 255, 114, 0.15)',
                }
            },
            fontFamily: {
                display: ['Clash Display', 'system-ui', 'sans-serif'],
                body: ['Satoshi', 'system-ui', 'sans-serif'],
                mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'gradient-mesh': 'linear-gradient(135deg, #0F1210 0%, #1a2f1c 25%, #0F1210 50%, #0f1a25 75%, #0F1210 100%)',
            },
            animation: {
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'glow': 'glow 2s ease-in-out infinite alternate',
                'scan': 'scan 2s linear infinite',
                'float': 'float 6s ease-in-out infinite',
                'topo-move': 'topo-move 20s linear infinite',
                'fade-in-up': 'fade-in-up 0.5s ease-out forwards',
                'typing': 'typing 0.05s steps(1) forwards',
            },
            keyframes: {
                glow: {
                    '0%': { boxShadow: '0 0 20px rgba(193, 255, 114, 0.1), inset 0 0 20px rgba(193, 255, 114, 0.05)' },
                    '100%': { boxShadow: '0 0 40px rgba(193, 255, 114, 0.2), inset 0 0 40px rgba(193, 255, 114, 0.1)' },
                },
                scan: {
                    '0%': { transform: 'translateY(-100%)' },
                    '100%': { transform: 'translateY(100%)' },
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-10px)' },
                },
                'topo-move': {
                    '0%': { transform: 'translateX(0) translateY(0)' },
                    '100%': { transform: 'translateX(-50px) translateY(-50px)' },
                },
                'fade-in-up': {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
            },
            backdropBlur: {
                xs: '2px',
                '2xl': '40px',
                '3xl': '64px',
            },
        },
    },
    plugins: [],
}
