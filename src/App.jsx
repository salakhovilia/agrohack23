import './App.css';
import { Navbar, NavbarBrand, NavbarContent } from '@nextui-org/react';
import { Outlet } from 'react-router-dom';

function App() {
  return (
    <>
      <Navbar className={'navbar bg-primary text-black'} isBlurred={true} position={'static'}>
        <NavbarContent>
          <NavbarBrand>
            <p className="font-bold text-white">Agrocode</p>
          </NavbarBrand>
        </NavbarContent>
      </Navbar>
      <main className="h-full w-full">
        <Outlet />
      </main>
    </>
  );
}

export default App;
