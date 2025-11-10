document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const emailInput = document.getElementById("email");
    const newPasswordInput = document.getElementById("new_password");
    const confirmPasswordInput = document.getElementById("confirm_password");


    // Create a message box dynamically if it doesn’t exist
    let messageBox = document.getElementById("messageBox");
    if (!messageBox) {
        messageBox = document.createElement("p");
        messageBox.id = "messageBox";
        messageBox.style.marginTop = "10px";
        messageBox.style.fontWeight = "bold";
        form.appendChild(messageBox);
    }

    // Handle form submission
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // stop default submission for validation

        const email = emailInput.value.trim();
        const newPassword = newPasswordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();

/* Is valid emial*/
form.addEventListener("submit", function (event) {
    event.preventDefault(); // stop default submission for validation

    const email = emailInput.value.trim();
    const newPassword = newPasswordInput.value.trim();
    const confirmPassword = confirmPasswordInput.value.trim();

    // --- Validation checks ---
    if (!isValidEmail(email)) {
        showMessage("❌ Please enter a valid email address.", "error");
        return;
    }

    if (!newPassword || !confirmPassword) {
        showMessage("⚠️ Please fill out all password fields.", "error");
        return;
    }

    if (newPassword !== confirmPassword) {
        showMessage("❌ Passwords do not match.", "error");
        return;
    }

    if (newPassword.length < 8) {
        showMessage("⚠️ Password must be at least 8 characters long.", "error");
        return;
    }

    const strongPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$/;
    if (!strongPassword.test(newPassword)) {
        showMessage("⚠️ Password must include uppercase, lowercase, number, and special character.", "error");
        return;
    }
/* display message */
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showMessage(text, type) {
    messageBox.textContent = text;
    messageBox.style.color = type === "error" ? "red" : "green";
}
});