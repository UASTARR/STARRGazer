if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register("/sw.js").then(function(registration) {
      console.log('ServiceWorker registration successful with scope: ', registration.scope);
    }, function(err) {
      console.log('ServiceWorker registration failed: ', err);
    });
  });
}

const btn = document.getElementById('connect-bluetooth');
const connStatus = document.getElementById('connection-status');

btn.addEventListener('click', async () => {
  if (!navigator.bluetooth) {
    connStatus.textContent = 'Web Bluetooth not supported.';
    return;
  }
  try {
    const device = await navigator.bluetooth.requestDevice({ acceptAllDevices: true });
    connStatus.textContent = `Connected to ${device.name}`;
    // Further: await device.gatt.connect();
  } catch (err) {
    connStatus.textContent = `Error: ${err}`;
  }
});
