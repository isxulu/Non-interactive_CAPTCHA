/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
 
    // Or if using `src` directory:
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundImage:{
        'github': "url('/github.png')",
        'loading': "url('/loading.png')",
        'pass': "url('/pass.png')",
        'fail': "url('/fail.png')",
      }
    },
  },
  plugins: [],
}