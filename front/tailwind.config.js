/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './nuxt.config.{js,ts}',
    './app.vue',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Overpass', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      colors: {
        primary: {
          50: '#f4f0ff',
          100: '#ebe4ff',
          200: '#d9ccff',
          300: '#bfa6ff',
          400: '#BA7408',
          500: '#BA7408',
          600: '#6D29D9',
          700: '#5c1fb8',
          800: '#4d1a96',
          900: '#3f1577',
          950: '#2a0d52',
        },
        'background-primary': '#FBFAF9',
        'background-secondary': '#E3E1DD',
        'text-primary': '#171717',
        'text-secondary': 'hsl(217.9, 10.6%, 64.9%)',
        'border-primary': 'hsl(215, 27.9%, 16.9%)',
        'text-orange': '#BA7408',
        // Dashboard sidebar colors
        'sidebar-bg': '#FBFAF9',
        'sidebar-text-primary': '#171717',
        'sidebar-text-secondary': '#666666',
        'sidebar-orange': '#BA7408',
        'sidebar-orange-bg': '#BA74081A',
        'sidebar-border': '#E3E1DD',
        // Card colors
        'card-text-primary': '#171717',
        'card-text-secondary': '#666666',
        'card-bg': '#FFFFFF',
        'card-border': '#E3E1DD',
      },
    },
  },
  plugins: [],
}
