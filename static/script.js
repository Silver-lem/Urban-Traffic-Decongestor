document.getElementById("traffic-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // stop page reload

    // get values
    const start = document.getElementById("start").value;
    const destination = document.getElementById("destination").value;
    const status = document.getElementById("status").value;

    // show "loading..." while waiting
    document.getElementById("recommendation").innerText = "Thinking... 🚦";

    try {
        // send data to Flask backend
        const response = await fetch("/get_recommendation", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ start, destination, status })
        });

        // get AI reply
        const data = await response.json();

        // update page
        document.getElementById("recommendation").innerText = data.recommendation;
    } catch (error) {
        document.getElementById("recommendation").innerText = "Error: Could not fetch recommendation.";
        console.error(error);
    }
});
