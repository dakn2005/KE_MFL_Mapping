/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{html, svelte, js, ts}"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  purge: ["./index.html",'./src/**/*.{svelte,js,ts}'], // for unused CSS

}

