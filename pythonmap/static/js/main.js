// import Chart from 'chart.js/auto';
const socket = io();
const ChartUpdateInterval = 500;

// initialize map
// let pathCoords = []; // Initialize pathCoords as an empty array

// document.addEventListener("DOMContentLoaded", function () {
//   var defaultLat = 47.9876571657164;
//   var defaultLon = -81.84886222782406;
//   var defaultZoom = 15;
//   var map = L.map("map").setView([defaultLat, defaultLon], defaultZoom);
//   L.tileLayer("/tiles/{z}/{x}/{y}.png", {
//     maxZoom: 17,
//     minZoom: 0,
//     tms: false,
//   }).addTo(map);

//   const customIcon = L.icon({
//     iconUrl: "static/icon.png",
//     iconSize: [40, 40],
//     iconAnchor: [12, 12],
//     popupAnchor: [1, -34],
//     shadowSize: [41, 41],
//   });

//   L.marker([defaultLat, defaultLon], { icon: customIcon }).addTo(map);

//   pathLine = L.polyline(pathCoords, { color: "red" }).addTo(map);
// });

const labels = [
  '-20 units',
  '-19 units',
  '-18 units',
  '-17 units',
  '-16 units',
  '-15 units',
  '-14 units',
  '-13 units',
  '-12 units',
  '-11 units',
  '-10 units',
  '-9 units',
  '-8 units',
  '-7 units',
  '-6 units',
  '-5 units',
  '-4 units',
  '-3 units',
  '-2 units',
  '-1 units',
  'start',
];

function updateChart(chart, newData) {
  chart.data.datasets.forEach((dataset, index) => {
    dataset.data = newData[index];
  });
  chart.update();
}

function updateLabels(chart, newLabels) {
  chart.data.labels = newLabels;
  chart.update();
}

const acc_data = {
  labels: labels,
  datasets: [{
    label: 'X Acceleration',
    backgroundColor: 'rgba(255, 99, 132, 0.5)',
    borderColor: 'rgb(255, 99, 132)',
    data: Array(21).fill(0),
  }, {
    label: 'Y Acceleration',
    backgroundColor: 'rgba(54, 162, 235, 0.5)',
    borderColor: 'rgb(54, 162, 235)',
    data: Array(21).fill(0),
  }, {
    label: 'Z Acceleration',
    backgroundColor: 'rgba(75, 192, 192, 0.5)',
    borderColor: 'rgb(75, 192, 192)',
    data: Array(21).fill(0),
  }]
}

const acc_config = {
  type: 'line',
  data: acc_data,
  options: {
    animation: false,
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Acceleration Data'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  },
};

let buffered_data = {
    accelerationx: 0,
    accelerationy: 0,
    accelerationz: 0,
};

function updateBufferedData(newData) {
  Object.keys(buffered_data).forEach((key) => {
    if (newData[key] !== undefined) {
      buffered_data[key] = newData[key];
    }
  });
}

const accChart = new Chart(
  document.getElementById('accChart'),
  acc_config
);

// Update chart every second with latest buffered data
let chart_updates_interval_id;

function startChartUpdates() {
  if (chart_updates_interval_id) return; // Already running
  chart_updates_interval_id = setInterval(() => {
      const newAccData = [
          acc_data.datasets[0].data.slice(1).concat([buffered_data.accelerationx]),
          acc_data.datasets[1].data.slice(1).concat([buffered_data.accelerationy]),
          acc_data.datasets[2].data.slice(1).concat([buffered_data.accelerationz]),
      ];
      const now = new Date();
      updateLabels(accChart, accChart.data.labels.slice(1).concat([now.toLocaleTimeString() + `.${now.getMilliseconds()}`]));
      updateChart(accChart, newAccData);
  }, ChartUpdateInterval);
}

// Stop chart updates when needed
function stopChartUpdates() {
  clearInterval(chart_updates_interval_id);
  chart_updates_interval_id = null;
}

// ports
// Populate baud rates (optional if static)
const baudRates = [9600, 19200, 38400, 57600, 115200];
const baudSelect = document.getElementById("baudSelect");
var ids = {};

// Fetch the IDs once and store them globally
async function fetchIds() {
  try {
    const response = await fetch("/ids");
    ids = await response.json(); // Assign the fetched data to the global variable
    console.log("Fetched IDs:", ids);
  } catch (error) {
    console.error("Error fetching IDs:", error);
  }
}

// Call the function to fetch IDs when the script loads
fetchIds();
console.log(ids);

// Fetch available serial ports (this depends on your backend API)
async function fetchPorts() {
  const res = await fetch("/ports");
  const j = await res.json();
  const portSelect = document.getElementById("portSelect");
  portSelect.innerHTML = '<option value="">-- Select Port --</option>';
  j.ports.forEach((p) => {
    // Display p
    console.log("Available port:", p);
    const opt = document.createElement("option");
    opt.value = p;
    opt.textContent = p;
    portSelect.appendChild(opt);
  });
}
fetchPorts();

// Update data from parsed serial feed
function updateParsedData(data) {
  // Update chart data
  updateBufferedData(data);
  if (data.ids == ids.id.temperature) {
    document.getElementById("temp").textContent =
      data.temperature;
    document.getElementById("pressure").textContent =
      data.pressure;
  } else if (data.ids == ids.id.acceleration) {
    document.getElementById("accX").textContent =
      data.accelerationx;
    document.getElementById("accY").textContent =
      data.accelerationy;
    document.getElementById("accZ").textContent =
      data.accelerationz;
  } else if (data.ids == ids.id.gyroscope) {
    document.getElementById("gyrox").textContent =
      data.gyroscopex;
    document.getElementById("gyroy").textContent =
      data.gyroscopey;
    document.getElementById("gyroz").textContent =
      data.gyroscopez;
  } else if (data.ids == ids.id.quaternion) {
    const [r, p, y] = convertQuatOrient(
      data.quaternionx,
      data.quaterniony,
      data.quaternionz,
      data.quaternionw
    );
    document.getElementById("roll").textContent = r;
    document.getElementById("pitch").textContent = p;
    document.getElementById("yaw").textContent = y;
  } else if (data.ids == ids.id.gps) {
    document.getElementById("lat").textContent = data.lat;
    document.getElementById("lon").textContent = data.lon;
    document.getElementById("alt").textContent = data.alt;
    document.getElementById("gpsfix").textContent =
      getGpsFix(data.gpsfix);
    document.getElementById("nsats").textContent = data.nsats;
  } else if (data.ids == ids.id.strain) {
    document.getElementById("strain1").textContent = data.strain1;
    document.getElementById("strain2").textContent = data.strain2;
  }

  // const newPoint = [data.lat, data.lat];
  // pathCoords.push(newPoint);
  // pathLine.setLatLngs(pathCoords);

  // marker.setLatLng([data.lat, data.lon]);
  // map.panTo([data.lat, data.lon]);
}

// Convert strain gauge raw data to readable format
function convertStrainGauge(raw) {
  if (raw === undefined || raw === null) return "--";
  // Example: assuming raw ADC counts from a 24-bit ADC
  const maxADC = 8388607; // for 24-bit signed
  const strainValue = (raw / maxADC) * 1000; // example scaling to microstrain
  return strainValue.toFixed(2) + " µε";
}

function convertQuatOrient(x, y, z, w) {
  // Roll (x-axis rotation)
  const sinr_cosp = 2 * (w * x + y * z);
  const cosr_cosp = 1 - 2 * (x * x + y * y);
  const roll = Math.atan2(sinr_cosp, cosr_cosp) * (180 / Math.PI);

  // Pitch (y-axis rotation)
  const sinp = 2 * (w * y - z * x);
  let pitch;
  if (Math.abs(sinp) >= 1) {
    pitch = Math.sign(sinp) * 90; // Use 90 degrees if out of range
  } else {
    pitch = Math.asin(sinp) * (180 / Math.PI);
  }

  // Yaw (z-axis rotation)
  const siny_cosp = 2 * (w * z + x * y);
  const cosy_cosp = 1 - 2 * (y * y + z * z);
  const yaw = Math.atan2(siny_cosp, cosy_cosp) * (180 / Math.PI);

  return [roll.toFixed(2), pitch.toFixed(2), yaw.toFixed(2)];
}

function getGpsFix(fix) {
  const modes = { 0: "No Fix", 1: "2D Fix", 2: "3D Fix" };
  return modes[fix] || "No Fix";
}

document.getElementById("connect").onclick = () => {
  const portSelect = document.getElementById("portSelect");
  const baudSelect = document.getElementById("baudSelect");

  const port = portSelect.value;
  const baud = baudSelect.value || "115200";
  
  if (!port) {
    alert("Please select a serial port first.");
    return;
  }
  
  startChartUpdates();
  socket.emit("start_serial", { port, baudrate: baud });
};

document.getElementById("disconnect").onclick = () => {
  stopChartUpdates();
  socket.emit("stop_serial");
};

const log = document.getElementById("log");

socket.on("serial_data", (data) => {
  log.textContent = JSON.stringify(data) + "\n" + log.textContent;
  updateParsedData(data);
});

socket.on("serial_started", (d) => {
  log.textContent =
    "[started] " + JSON.stringify(d) + "\n" + log.textContent;
});

socket.on("serial_stopped", () => {
  log.textContent = "[stopped]\n" + log.textContent;
});