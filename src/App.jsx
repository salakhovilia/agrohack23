import './App.css';
import { Navbar, NavbarBrand, NavbarContent } from '@nextui-org/react';
import { Outlet } from 'react-router-dom';

function App() {
  return (
    <>
      <Navbar className={'bg-indigo-600'} isBlurred={true} position={'sticky'}>
        <NavbarContent>
          <NavbarBrand>
            <p className="font-bold text-white">Agrocode</p>
          </NavbarBrand>
        </NavbarContent>
      </Navbar>
      <main className="h-full w-full bg-indigo-950">
        <Outlet />
      </main>
    </>
  );
}

export default App;
