document.addEventListener('DOMContentLoaded', () => {
    const guideContainer = document.getElementById('guide-container');

    // Fetch the generated guide using an absolute path from the server root.
    // This is more reliable than a relative path.
    fetch('/output/hcim_guide.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok (Status: ${response.status})`);
            }
            return response.json();
        })
        .then(guideData => {
            guideContainer.innerHTML = ''; // Clear loading message
            renderGuide(guideData, guideContainer);
        })
        .catch(error => {
            console.error('Error fetching the guide:', error);
            guideContainer.innerHTML = `<p class="error">Could not load the guide. Make sure the file exists at /output/hcim_guide.json and you are running a local server from the project root. Check the browser console (F12) for more details.</p>`;
        });
});

function renderGuide(guide, container) {
    if (guide.length === 0) {
        container.innerHTML = `<p class="loading">Guide generated, but it's empty. Time to build the core logic!</p>`;
        return;
    }

    guide.forEach((trip, index) => {
        const tripElement = document.createElement('div');
        tripElement.className = 'trip';

        tripElement.innerHTML = `
            <h2>Chapter ${index + 1}: ${trip.title}</h2>
            <p><strong>Goal:</strong> ${trip.goal}</p>
            <h3>Inventory Setup:</h3>
            <ul>
                ${trip.inventory_setup.map(item => `<li>${item}</li>`).join('')}
            </ul>
            <h3>Steps:</h3>
            <ol>
                ${trip.steps.map(step => `<li><input type="checkbox"> ${step.text}</li>`).join('')}
            </ol>
        `;
        container.appendChild(tripElement);
    });
}