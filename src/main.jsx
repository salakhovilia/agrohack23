import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import { NextUIProvider } from '@nextui-org/react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Index from './pages/index.jsx';
import { YMaps } from '@pbe/react-yandex-maps';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: <Index />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}>
      <NextUIProvider>
        <App />
      </NextUIProvider>
    </RouterProvider>
  </React.StrictMode>,
);
