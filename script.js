function fetchLiveData() {
    Promise.all([
        fetch('/detect_anomaly').then(res => res.ok ? res.json() : Promise.reject("Failed to fetch Anomaly Data")),
        fetch('/predict_maintenance').then(res => res.ok ? res.json() : Promise.reject("Failed to fetch Predictive Maintenance Data")),
        fetch('/calculate_oee').then(res => res.ok ? res.json() : Promise.reject("Failed to fetch OEE Data"))
    ])
    .then(([anomalyData, predictiveData, oeeData]) => {
        // ✅ Update Live Sensor Readings
        if (anomalyData.data) {
            updateLiveReadings(anomalyData.data);
            updateCharts(anomalyData.data);
        }

        // ✅ Update Anomaly Detection Status
        document.getElementById("anomaly-status").innerText = `Anomaly Status: ${anomalyData.status || "No Data"}`;

        // ✅ Update Predictive Maintenance Status
        document.getElementById("predictive-status").innerText = `Predictive Maintenance Status: ${predictiveData.status || "No Data"}`;

        // ✅ Update OEE Calculation
        document.getElementById("oee-result").innerText = `OEE: ${oeeData.OEE !== undefined ? oeeData.OEE.toFixed(2) : "No Data"}`;
    })
    .catch(error => console.error("API Error:", error));
}

// ✅ Update live sensor readings dynamically
function updateLiveReadings(data) {
    Object.keys(data).forEach(key => {
        let element = document.getElementById(key);
        if (element) {
            element.innerText = data[key] !== undefined ? data[key].toFixed(2) : "--";
        }
    });
}

// ✅ Update all charts with the latest data
function updateCharts(data) {
    updateChart(zAxisVelocityChart, "Z-Axis Peak Velocity (mm/sec)", data["Z-Axis Peak Velocity (mm/sec)"]);
    updateChart(xAxisAccelerationChart, "X-Axis Peak Acceleration (G)", data["X-Axis Peak Acceleration (G)"]);
    updateChart(xAxisVelocityChart, "X-Axis RMS Velocity (in/sec)", data["X-Axis RMS Velocity (in/sec)"]);
    updateChart(zAxisAccelerationChart, "Z-Axis Peak Acceleration (G)", data["Z-Axis Peak Acceleration (G)"]);
    updateChart(zAxisRMSVelocityChart, "Z-Axis RMS Velocity (in/sec)", data["Z-Axis RMS Velocity (in/sec)"]);
}

// ✅ Function to update a specific chart
function updateChart(chart, label, value) {
    if (value === undefined) return; // Prevent updating with undefined values
    let now = new Date().toLocaleTimeString();
    chart.data.labels.push(now);
    chart.data.datasets[0].data.push(value);
    if (chart.data.labels.length > 10) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    chart.update();
}

// ✅ Fetch live data every 5 seconds
setInterval(fetchLiveData, 5000);
fetchLiveData();

// ✅ Function to create charts dynamically
function createChart(canvasId, label, color) {
    return new Chart(document.getElementById(canvasId), {
        type: 'line',
        data: { labels: [], datasets: [{ label: label, data: [], borderColor: color }] },
        options: { 
            responsive: true, 
            maintainAspectRatio: false,
            scales: { 
                x: { title: { display: true, text: 'Time' } }, 
                y: { title: { display: true, text: label } } 
            } 
        }
    });
}

// ✅ Create all charts
const zAxisVelocityChart = createChart('zAxisVelocityChart', 'Z-Axis Peak Velocity (mm/sec)', 'blue');
const xAxisAccelerationChart = createChart('xAxisAccelerationChart', 'X-Axis Peak Acceleration (G)', 'red');
const xAxisVelocityChart = createChart('xAxisVelocityChart', 'X-Axis RMS Velocity (in/sec)', 'orange');
const zAxisAccelerationChart = createChart('zAxisAccelerationChart', 'Z-Axis Peak Acceleration (G)', 'green');
const zAxisRMSVelocityChart = createChart('zAxisRMSVelocityChart', 'Z-Axis RMS Velocity (in/sec)', 'purple');

const oeeChart = new Chart(document.getElementById('oeeChart'), {
    type: 'doughnut',
    data: { labels: ['OEE'], datasets: [{ label: 'OEE', data: [], backgroundColor: 'green' }] },
});
