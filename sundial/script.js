const latInput = document.getElementById('latitude');
const lonInput = document.getElementById('longitude');
const setLocationBtn = document.getElementById('setLocation');
const hand = document.getElementById('hand');
const solarTimeDisplay = document.getElementById('solarTime');

let latitude = 0;
let longitude = 0;

const map = L.map('map').setView([latitude, longitude], 1);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let marker = L.marker([latitude, longitude]).addTo(map);

map.on('click', e => {
    latitude = e.latlng.lat;
    longitude = e.latlng.lng;
    latInput.value = latitude.toFixed(4);
    lonInput.value = longitude.toFixed(4);
    marker.setLatLng(e.latlng);
    update();
});

function toRadians(deg) {
    return deg * Math.PI / 180;
}

function dayOfYear(date) {
    const start = new Date(date.getFullYear(), 0, 0);
    const diff = date - start + (start.getTimezoneOffset() - date.getTimezoneOffset()) * 60000;
    return Math.floor(diff / 86400000);
}

function solarTime(date, lat, lon) {
    const N = dayOfYear(date);
    const gamma = 2 * Math.PI / 365 * (N - 1 + (date.getUTCHours() - 12) / 24);

    const EoT = 229.18 * (0.000075 + 0.001868 * Math.cos(gamma)
        - 0.032077 * Math.sin(gamma)
        - 0.014615 * Math.cos(2 * gamma)
        - 0.040849 * Math.sin(2 * gamma));

    const totalMinutes = date.getUTCHours() * 60 + date.getUTCMinutes();
    const LSTMins = totalMinutes + EoT + 4 * lon;
    let LST = (LSTMins / 60) % 24;
    if (LST < 0) LST += 24;
    return LST;
}

function update() {
    const now = new Date();
    const LST = solarTime(now, latitude, longitude);
    const angle = (LST % 12) * 30; // 30 degrees per hour
    hand.style.transform = `rotate(${angle}deg)`;
    const hours = Math.floor(LST);
    const minutes = Math.floor((LST - hours) * 60);
    solarTimeDisplay.textContent = `Solar Time: ${hours.toString().padStart(2,'0')}:${minutes.toString().padStart(2,'0')}`;
}

setLocationBtn.addEventListener('click', () => {
    latitude = parseFloat(latInput.value) || 0;
    longitude = parseFloat(lonInput.value) || 0;
    marker.setLatLng([latitude, longitude]);
    map.setView([latitude, longitude], 4);
    update();
});

setInterval(update, 60000);
update();
