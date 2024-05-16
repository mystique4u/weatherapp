document.addEventListener("DOMContentLoaded", function() {
    getLocation();
});

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    // Send location data to Flask backend
    fetch('/update_location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ latitude, longitude })
    }).then(response => {
        // console.log('Location sent to Flask backend.');

        // Redirect to another page after allowing location access
        window.location.href = '/result?lat=' + latitude + '&lon=' + longitude;
    }).catch(error => {
        console.error('Error sending location:', error);
    });
}
    
    