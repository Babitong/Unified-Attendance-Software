class AttendanceScanner {
    constructor() {
        this.videoElement = document.getElementById('scanner-view');
        this.canvasElement = document.getElementById('scanner-canvas');
        this.canvasContext = this.canvasElement.getContext('2d');
        this.initScanner();
    }

    initScanner() {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
            .then(stream => {
                this.videoElement.srcObject = stream;
                this.videoElement.play();
                this.scanFrame();
            });
    }

    scanFrame() {
        if (this.videoElement.readyState === this.videoElement.HAVE_ENOUGH_DATA) {
            this.canvasElement.hidden = false;
            
            this.canvasContext.drawImage(
                this.videoElement,
                0, 0,
                this.canvasElement.width,
                this.canvasElement.height
            );

            const imageData = this.canvasContext.getImageData(
                0, 0,
                this.canvasElement.width,
                this.canvasElement.height
            );

            const code = jsQR(imageData.data, imageData.width, imageData.height);
            
            if (code) {
                this.handleScan(code.data);
            }
        }
        requestAnimationFrame(() => this.scanFrame());
    }

    handleScan(data) {
        const [type, id] = data.split(':');
        
        fetch('/api/log-attendance/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                log_type: 'CLASS_START',  // or 'CLASS_END'
                classroom_id: id,
                latitude: currentLatitude,
                longitude: currentLongitude
            })
        }).then(response => {
            if (response.ok) {
                showSuccess('Attendance recorded!');
            }
        });
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    new AttendanceScanner();
});
