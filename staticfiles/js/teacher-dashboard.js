const countdownEl = document.getElementById("countdown");
const checkInTime = new Date();
checkInTime.setHours(8, 12, 0); // 8:12 AM

const targetTime = new Date(checkInTime.getTime() + 3 * 60 * 60 * 1000 + 20 * 60 * 1000);

function updateCountdown() {
  const now = new Date();
  const diff = targetTime - now;

  if (diff <= 0) {
    countdownEl.textContent = "Available now!";
    return;
  }

  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  countdownEl.textContent = `${hours}h ${minutes}m`;
}

setInterval(updateCountdown, 1000);
updateCountdown();

