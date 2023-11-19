import './App.css';
import { Outlet } from 'react-router-dom';

function App() {
  return (
    <>
      <div className="navbar bg-base-100">
        <a className="btn btn-ghost text-xl">Ferma in the Air</a>
      </div>
      <main className="h-[calc(100%-64px)] w-full p-2">
        <Outlet />
      </main>
    </>
  );
}

export default App;
