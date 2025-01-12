import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import PIGPage from './components/PIGPage';
import ProjetFederateurIA from './components/ProjetFederateurIA';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/PIG" element={<PIGPage />} />
          <Route path="/ProjetFederateurIA" element={<ProjetFederateurIA />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
