function selectRole(role) {
    var selectedRoleElement = document.getElementById(role);
    document.querySelectorAll('.role').forEach(function(elem) {
        elem.classList.remove('active');
    });
    selectedRoleElement.classList.add('active');
    document.getElementById('selectedRole').value = role;
}
// Function to hide the error messages after 6 seconds
setTimeout(function() {
    
    hideLoadingOverlay()

    var errorMessages = document.getElementById('error-messages');
    
    if (errorMessages) {
        errorMessages.style.display = 'none';
    }

}, 6000);  // 6 seconds

function showLoadingOverlay() {
    document.getElementById("loading-overlay").style.display = "flex";
}
function hideLoadingOverlay() {
    document.getElementById("loading-overlay").style.display = "none";
}