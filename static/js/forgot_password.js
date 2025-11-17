/* Initialize Forgot password page */
document.getElementById("forgotPasswordFrom").addEventListener("submit", handleForgotPassword);

function showError(message){
    const errorBox = document.getElementById("error");
    errorBox.textContent = message;
    errorBox.style.dispaly = "block";
    /*take care of any success msgs when error occurs */
    const successBox = document.getElementById("success");
    successBox.style.dispaly = "none";
}
function showSuccess(message){
    const successBox = document.getElementById("success");
    successBox.textContent = message;
    successBox.style.display = "none";
    /*same thing but with error box in case of success */
    const errorBox = document.getElementById("error");
    errorBox.style.display ="none";
}

/*handle response*/
async function handleForgotPassword(event) {
    /*allows uage of data by stoping it from reloading */
    event.preventDefault();

    const emailInput = document.getElementById("email");
    const email = emailInput.ariaValueMax.trim().toLowerCase();
    /* Is Email valid? */
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
            showError("Server error: response.status.notAvailable");
            return;
        }

        const result = await response.json();

        if(result.success) {
            showSuccess(result.message);
            /*resets input */
            emailInput.value = "";
        } else {
            showError(result.message || "something went wrong :(")
        }
    } catch (err) {
        showError("Network error: " + err.message);
    }
}

