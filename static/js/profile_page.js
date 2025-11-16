/*Call user Profile */
document.addEventListener("DOMContentLoaded", function() {
    const profileIcon = document.querySelector(".profile_icon a");
    const userInfoList = document.querySelector(".User_information ul");
    const savedMedicineList = document.querySelector(".saved-medicines ul");
    const warningsList = document.querySelector(".Warnings ul");



    /* edit profile icon */
    profileIcon.addEventListener("click", function (event){
        messageBox.textContent = "Redirecting to edit profile...";
    });

    function checkUserInfo(){
        const listItems = userInfoList.querySelectorAll("li");
        listItems.forEach(li=> {
            if (li.textContent.includes("Not set")) {
                li.style.color ="red";
            }
        });
    }
    checkUserInfo();

    

/* attach Event List */
function attachEventListeners() {
    // Saved medicines links hover
    const savedMedicineItems = document.querySelectorAll(".saved-medicines li a");
    savedMedicineItems.forEach(a => {
        a.addEventListener("mouseover", () => {
            a.style.color = "#007BFF";
        });
        a.addEventListener("mouseout", () => {
            a.style.color = "#333";
        });
    });
    // Profile icon click
    const profileIcon = document.querySelector(".profile_icon a");
    profileIcon.addEventListener("click", () => {
        console.log("Redirecting to edit profile page...");
        // optional: display message or animate
    });
}
attachEventListeners();
/*Display saved Medicines */
    const savedMedicineItems = savedMedicinesList.querySelector("li a");
     savedMedicineItems.forEach(a => {
        a.addEventListener("mouseover", () =>{
            a.style.color="#007BFF";
        });
        a.addEventListener("mouseout", () => {
            a.style.color = "#333";
        });
     })
/* display Warnings */
    function generateWarnings (){
        const warnings = [];
        if (warnings.length > 0) {
            warningsList.innerHTML = "";
            warnings.forEach (w=> {
                const li = document.createElement("li");
                li.textContent =w;
                li.style.color="red";
                warningsList.appendChild(li);
            });
        } else {
            warningsList.innerHTML = "<li>No warnings at this time</li>";
        }
    }
generateWarnings();
/* Load Medicin Schedule*/
function loadMedicineSchedule() {
    const scheduleList = document.querySelector(".Calender ul");

    const schedule = [
        { medicine: "Aspirin", time: "8:00 AM"},
        { medicine: "ibuprofen", time:"12:00 PM"},
        { medicine: "paracetamol", time:"8:00 PM"}
    ];

    scheduleList.innerHTML ="";
    
    if (schedule.lenght > 0){
        scheduleList.innerHTML = "<li>No schedule medicines yet.</li>";
    } else {
        schedule.forEach(item => {
            const li = document.createElement("li");
            li.textContent = '${item.medicine} at ${item.time}';
            scheduleList.appendChild(li);
        });
    }
}
loadMedicineSchedule();
/*  Save User Perferences */
function saveUserPreferences(preferences) {
    // Example: preferences = { theme: "dark", notifications: true }
    localStorage.setItem("userPreferences", JSON.stringify(preferences));
    console.log("User preferences saved!");
}

// Example usage
const userPrefs = {
    theme: "light",
    notifications: true
};
saveUserPreferences(userPrefs);

// Optional: load preferences on page load
function loadUserPreferences() {
    const prefs = JSON.parse(localStorage.getItem("userPreferences")) || {};
    console.log("Loaded preferences:", prefs);
    // Apply preferences to page (theme, notifications, etc.)
}
})
