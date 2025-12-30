function drawTemperatureChart(days, temps) {
    const ctx = document.getElementById("tempChart").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: days,
            datasets: [{
                label: "Temperature (°C)",
                data: temps,
                borderColor: "#667eea",
                backgroundColor: "rgba(102,126,234,0.2)",
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}
