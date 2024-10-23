document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const resultDiv = document.getElementById('results');
    const modelList = document.getElementById('modelList');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        fetch('/train', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Erreur : ' + data.error);
            } else {
                displayResults(data.models);
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Une erreur est survenue lors de la requête.');
        });
    });

    function displayResults(models) {
        modelList.innerHTML = '';
        models.forEach(model => {
            const li = document.createElement('li');
            li.textContent = `${model.model_name}: Précision de ${(model.accuracy * 100).toFixed(2)}%`;
            modelList.appendChild(li);
        });
        resultDiv.classList.remove('hidden');
    }
});