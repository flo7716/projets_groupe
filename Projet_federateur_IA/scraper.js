const axios = require('axios');
const cheerio = require('cheerio');

// Fonction pour scraper un article
async function scrapeArticle(url) {
    try {
        const { data } = await axios.get(url);
        const $ = cheerio.load(data);

        // Extraction des informations
        const title = $('h1').text().trim() || 'Titre non trouvé';
        const date = $('time').text().trim() || 'Date non trouvée';
        const paragraphs = $('p').map((i, el) => $(el).text().trim()).get();
        const articleText = paragraphs.join(' ');

        return {
            url,
            title,
            date,
            articleText
        };
    } catch (error) {
        console.error(`Erreur lors de la récupération de l'article: ${url}`, error);
        return null;
    }
}

// Exemple d'utilisation
const articleUrl = 'https://www.computerworld.com/';
scrapeArticle(articleUrl).then(data => console.log(data));
