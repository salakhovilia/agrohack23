/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
    './node_modules/react-tailwindcss-datepicker/dist/index.esm.js',
  ],

  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
        mytheme: {
          primary: '#42080c',
          secondary: '#F7C0BE',
          accent: '#ef7e7a',
          neutral: '#D6D6E9',
          'base-100': '#ffffff',
          info: '#ffffff',
          success: '#22c55e',
          warning: '#FFD800',
          error: '#B71c1c',
        },
      },
    ],
  },
};
