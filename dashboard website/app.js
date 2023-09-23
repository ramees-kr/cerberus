// JavaScript code for handling button click events and toggling the status

var statusButtons = document.querySelectorAll(".status-toggle");
statusButtons.forEach(function(button) {
    button.addEventListener("click", function() {
        var currentStatus = button.classList.contains("unblocked") ? "Unblocked" : "Blocked";
        var newStatus = currentStatus === "Unblocked" ? "Blocked" : "Unblocked";
        button.textContent = newStatus;
        button.classList.toggle("unblocked");
        button.classList.toggle("blocked");
    });
});