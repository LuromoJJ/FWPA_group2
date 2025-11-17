/* Initialize Forgot password page */
document.getElementById("forgotPasswordFrom").addEventListener("submit", handleForgotPassword);

function showError(message){
    const errorBox = document.getElementById("error");
    errorBox.textContent = message;
    errorBox.style.dispaly = "block";

    const successBox = document.getElementById("success");
    successBox.style.display = "none";
}


/*handle response*/


/* Is Email valid? */