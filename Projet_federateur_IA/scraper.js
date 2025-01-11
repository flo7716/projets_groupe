// Script de scraping avec spaCy (exemple en Python)
const { exec } = require('child_process');

// Commande pour exécuter un script Python de scraping
exec('python3 scraper.py', (error, stdout, stderr) => {
  if (error) {
    console.error(`Erreur lors de l'exécution du scraper: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`stderr: ${stderr}`);
    return;
  }
  console.log(`stdout: ${stdout}`);
});
