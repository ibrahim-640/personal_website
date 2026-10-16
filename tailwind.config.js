module.exports = {
  content: [
    './portfolio_site/templates/**/*.html',
    './portfolio_site/main/templates/**/*.html',
    './portfolio_site/static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        bg: '#070F1D', surface: '#0C182F', fg: '#EBF2FA',
        primary: '#00D3F2', glow: '#6192F8', muted: '#95A3BB',
        chip: '#151F32', danger: '#F4514F',
        panel: 'rgba(255,255,255,.06)', 'panel-strong': 'rgba(255,255,255,.09)',
        line: 'rgba(255,255,255,.10)', 'line-strong': 'rgba(255,255,255,.18)',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'Inter', 'sans-serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
      },
      maxWidth: { page: '1152px' },
      borderRadius: { base: '15px', card: '24px', 'card-lg': '33px' },
      fontSize: { hero: ['clamp(2.5rem, 7vw, 4.5rem)', { lineHeight: '1.02' }] },
      letterSpacing: { tightest: '-0.03em', label: '0.15em' },
      keyframes: {
        drift: { '0%': { transform: 'translate(0,0) rotate(-6deg)' }, '100%': { transform: 'translate(40px,-30px) rotate(8deg)' } },
        floaty: { '0%,100%': { transform: 'translateY(-10px)' }, '50%': { transform: 'translateY(10px)' } },
        dot: { '0%,100%': { opacity: 1, transform: 'scale(1)' }, '50%': { opacity: 0.4, transform: 'scale(.7)' } },
      },
      animation: {
        'drift-a': 'drift 16s ease-in-out infinite alternate',
        'drift-b': 'drift 21s ease-in-out infinite alternate-reverse',
        floaty: 'floaty 7s ease-in-out infinite',
        dot: 'dot 2.4s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}