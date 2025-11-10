/*Call user Profile */
document.addEventListener("DOMContentLoaded", function() {
    const profileIcon = document.querySelector(".profile_icon a");
    const userInfoList = document.querySelector(".User_information ul");
    const savedMedicineList = document.querySelector(".saved-medicines ul");
    const warningsList = document.querySelector(".Warnings ul");


    let messagesBox = document.getElementById("profileMessage");
    if (!messageBox) {
        messageBox = document.createElement("p");
        messageBox.id = "profileMessage";
        messageBox.style.color = "blue";
        messageBox.style.fontweight = "bold";
        messageBox.style.marginTop ="10px";
        document.querySelector("-profile-top").prepend(messageBox);
    }
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

/*Display saved Medicines */
    
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

/*  Save User Perferences */
})
