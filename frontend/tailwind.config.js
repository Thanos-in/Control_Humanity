module.exports = {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        'scroll-track': '#000',
        'scroll-thumb': '#333',
      },
      rotate: {
        '5': '5deg',
      },
      keyframes: {
        splash: {
          '0%': {
            transform: 'scale(1.1)',
          },
          '40%': {
            transform: 'scale(1)',
            background: '#22c55e',
            boxShadow:
              '0 -18px 0 -8px #22c55e, 16px -8px 0 -8px #22c55e, 16px 8px 0 -8px #22c55e, 0 18px 0 -8px #22c55e, -16px 8px 0 -8px #22c55e, -16px -8px 0 -8px #22c55e',
          },
          '100%': {
            background: '#22c55e',
            boxShadow:
              '0 -32px 0 -10px transparent, 28px -16px 0 -10px transparent, 28px 16px 0 -10px transparent, 0 32px 0 -10px transparent, -28px 16px 0 -10px transparent, -28px -16px 0 -10px transparent',
          },
        },
      },
      animation: {
        splash: 'splash 0.6s ease forwards',
      },
    }
  },
  plugins: [
    function({ addUtilities }) {
      addUtilities({
        '.scrollbar-black': {
          /* WebKit */
          '&::-webkit-scrollbar': { background: '#000', width: '8px' },
          '&::-webkit-scrollbar-thumb': { background: '#333', borderRadius: '4px' },
          '&::-webkit-scrollbar-track': { background: '#000' },
          /* Firefox */
          'scrollbar-width': 'thin',
          'scrollbar-color': '#333 #000',
        }
      })
    }
  ]
}
