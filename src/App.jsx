import './App.css';
import { Outlet } from 'react-router-dom';

function App() {
  return (
    <>
      <div className="navbar bg-base-100">
        <a className="btn btn-ghost text-xl">Ferma in the Air</a>
      </div>
      <main className="h-full w-full">
        <Outlet />
      </main>
    </>
  );
}

export default App;
