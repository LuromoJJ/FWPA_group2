/* Initialize sign up form*/
document.getElementById("info Form").addEventListener("submit", handleFormsubmit);{
    const getFormData = document.querySelector(".User_information ul");


    /* handels form data (p.s. Trim() means w/out whitespace) */
function getFormData(){
    return{
        name : document.getElementById("name").value.trim(),
        age : document.getElementById("age").value,
        weight : document.getElementById("weight").value,
        gender : document.getElementById("gender").value.trim(),
        medical_conditions : document.getElementById("medical_conditions").value,
        height : document.getElementById("height").value,
        smoker : document.getElementById("smoker").value.trim(),
        alcohol : document.getElementById("alcohol").value.trim(),
        allergies : document.getElementById("allergies").value.trim(),
    };
}

function validateData(){
    if (!data.name) return "Name is required";
    if (!data.age || data.age < 0 ) return "Valid age is required";
    if (!data.weight || data.weight <= 0) return "Valid weight is required";
    return null
}

function showError(message){
    const box = document.getElementById("error");
    box.textContent = message;
    box.style.display = "block"
}
/* Handle Form submission*/

async function handleFormsubmit(event) {
    /*trying to prevent page form reloading instantly */
    event.preventDefault();
    const deta = getFormData();
    const error = validateData();
    if (error) {
        showError(error);
        return;
    }
    const formData = new FormData(event.target);
    const response = await fetch("/form", {method: postMessage, body: formData});
/* Display message (success of error)*/
    if (!response.ok){
        showError("Something went wrong please try again.");
        return;
    }
    
    alert("Form submitted successfully")
    
}
}


