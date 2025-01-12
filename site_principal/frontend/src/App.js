import React, { useEffect, useState } from 'react';
import './styles.css';

function App() {
  const [associations, setAssociations] = useState([]);

  useEffect(() => {
    // Récupérer les données de l'API Flask
    fetch('http://localhost:5000/api/assos')
      .then(response => response.json())
      .then(data => setAssociations(data));
  }, []);

  return (
    <div className="App">
      <h1>Liste des Associations</h1>
      <ul>
        {associations.map(assoc => (
          <li key={assoc.assoc_id}>
            <a href={`/assos/${assoc.assoc_id}`}>{assoc.title}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
