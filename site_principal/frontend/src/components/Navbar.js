import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav>
      <ul>
        <li><Link to="/">Accueil</Link></li>
        <li><Link to="/PIG">Rubrique PIG</Link></li>
        <li><Link to="/ProjetFederateurIA">Rubrique IA</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;
