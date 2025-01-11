document.addEventListener('DOMContentLoaded', function () {
    fetch('/articles')
        .then(response => response.json())
        .then(data => {
            const articlesContainer = document.getElementById('articles-container');
            data.forEach(article => {
                const articleElement = document.createElement('div');
                articleElement.innerHTML = `<h3><a href="${article.link}">${article.title}</a></h3>`;
                articlesContainer.appendChild(articleElement);
            });
        })
        .catch(error => {
            console.error('Error fetching articles:', error);
        });
});
