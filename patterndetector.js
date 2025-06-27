// frontend/typing_detector.js
let typingTimes = [];
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("cardNumber");
    input.addEventListener("keydown", () => {
        typingTimes.push(Date.now());
    });
});

function getTypingSpeed() {
    let intervals = [];
    for (let i = 1; i < typingTimes.length; i++) {
        intervals.push(typingTimes[i] - typingTimes[i - 1]);
    }
    let avg = intervals.reduce((a, b) => a + b, 0) / intervals.length;
    return avg; // Lower avg = human, high = bot/script
}
