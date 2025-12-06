/* Initialize Forgot password page */
document.getElementById("forgotPasswordForm").addEventListener("submit", handleForgotPassword);

// Show error message
function showError(message) {
    const errorBox = document.getElementById("error");
    errorBox.textContent = message;
    errorBox.style.display = "block";

    const successBox = document.getElementById("success");
    successBox.style.display = "none";
}

// Show success message
function showSuccess(message) {
    const successBox = document.getElementById("success");
    successBox.textContent = message;
    successBox.style.display = "block";

    const errorBox = document.getElementById("error");
    errorBox.style.display = "none";
}

// Handle forgot password submission
async function handleForgotPassword(event) {
    event.preventDefault();

    const emailInput = document.getElementById("email");
    const email = emailInput.value.trim().toLowerCase();

    if (!email) {
        showError("Please enter your email");
        return;
    }

    try {
        const formData = new FormData();
        formData.append("email", email);

        const response = await fetch("/forgot_password", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            showError(`Server error: ${response.status}`);
            return;
        }

        const result = await response.json();

        if (result.success) {
            showSuccess(result.message);
            emailInput.value = "";
        } else {
            showError(result.message || "Something went wrong :(");
        }
    } catch (err) {
        showError("Network error: " + err.message);
    }
}