setInterval(() => {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            const gestureElem = document.getElementById('gesture');
            const brightnessElem = document.getElementById('brightness');

            if (gestureElem && brightnessElem) {
                gestureElem.textContent = data.gesture || 'None';
                brightnessElem.textContent = data.brightness || 0;
            }
        })
        .catch(error => {
            console.error("❌ Error fetching status:", error);
        });
}, 1000);
