// --- Map Initialization ---
let map = L.map('map').setView([20.5937, 78.9629], 5); // Centered on India
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
let routeLayer = null; // To hold the route layer

// --- Main Form Submission Logic ---
document.getElementById("traffic-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const start = document.getElementById("start").value;
    const destination = document.getElementById("destination").value;
    const status = document.getElementById("status").value;

    document.getElementById("recommendation").innerHTML = "";
    document.getElementById("loader").classList.remove("hidden");

    try {
        const response = await fetch("/get_recommendation", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ start, destination, status })
        });
        const data = await response.json();

        document.getElementById("loader").classList.add("hidden");
        document.getElementById("recommendation").innerText = data.recommendation;

        if (data.geometry) {
            if (routeLayer) map.removeLayer(routeLayer);

            routeLayer = L.geoJSON({
                "type": "Feature",
                "geometry": data.geometry
            }, {
                style: { color: "#00F5A0", weight: 5, opacity: 0.8 }
            }).addTo(map);
            map.fitBounds(routeLayer.getBounds());
        }

    } catch (error) {
        document.getElementById("loader").classList.add("hidden");
        document.getElementById("recommendation").innerText = "Error: Could not get recommendation.";
        console.error(error);
    }
});

// --- Voice Input (Speech-to-Text) ---
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-US';

    document.querySelectorAll('.mic-icon').forEach(mic => {
        mic.addEventListener('click', () => {
            const targetInput = document.getElementById(mic.dataset.target);
            recognition.start();
            targetInput.placeholder = "Listening...";
            
            recognition.onresult = (event) => {
                targetInput.value = event.results[0][0].transcript;
                targetInput.placeholder = "";
            };
            
            recognition.onerror = (event) => {
                console.error("Speech recognition error", event.error);
                targetInput.placeholder = "Sorry, I couldn't hear you.";
            };
        });
    });
} else {
    document.querySelectorAll('.mic-icon').forEach(mic => mic.style.display = 'none');
}

// --- Voice Output (Text-to-Speech) ---
document.getElementById('speaker-btn').addEventListener('click', () => {
    const textToSpeak = document.getElementById('recommendation').innerText;
    if (textToSpeak && 'speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(textToSpeak);
        window.speechSynthesis.speak(utterance);
    }
});

// --- Events Dropdown with Traffic Impact ---
const eventsDropdown = document.getElementById("events-dropdown");
document.getElementById("find-events-btn").addEventListener("click", async () => {
    try {
        const mockEvents = [
            { name: "Hyderabad Tech Fest", location: "Hyderabad, Telangana", venue: "HITEX", impact: "High" },
            { name: "Mumbai Music Concert", location: "Mumbai, Maharashtra", venue: "NCPA", impact: "Moderate" },
            { name: "Delhi Sports Meet", location: "New Delhi, Delhi", venue: "Jawaharlal Stadium", impact: "Low" }
        ];

        eventsDropdown.innerHTML = '<option value="">-- Select an Event --</option>';

        mockEvents.forEach(ev => {
            const option = document.createElement("option");
            option.value = ev.location;
            option.textContent = `${ev.name} @ ${ev.venue} (Traffic: ${ev.impact})`;
            option.setAttribute("data-impact", ev.impact);
            eventsDropdown.appendChild(option);
        });

        eventsDropdown.classList.remove("hidden");

    } catch (err) {
        console.error("Error fetching events:", err);
    }
});

// Autofill destination when event is selected
eventsDropdown.addEventListener("change", () => {
    if (eventsDropdown.value) {
        document.getElementById("destination").value = eventsDropdown.value;
    }
});


