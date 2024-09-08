// tailwind.config.js
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#FF0000', // Red for accents
        },
        dark: {
          DEFAULT: '#1a1a1a', // Almost black for background
          light: '#2d2d2d', // Lighter dark for UI elements
        },
        gray: {
          DEFAULT: '#8a8a8a', // Text color on dark background
        },
      },
    },
  },
  plugins: [],
};