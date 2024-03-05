function selectRole(role) {
    var selectedRoleElement = document.getElementById(role);
    document.querySelectorAll('.role').forEach(function(elem) {
        elem.classList.remove('active');
    });
    selectedRoleElement.classList.add('active');
    document.getElementById('selectedRole').value = role;
}

function loadingIndicator(){
    document.getElementById("loading-overlay").style.display = "flex"; // Show overlay
    loadingTimeout = setTimeout(function() {
            document.getElementById("loading-overlay").style.display = "none"; // Hide overlay
        }, 120000);
}
