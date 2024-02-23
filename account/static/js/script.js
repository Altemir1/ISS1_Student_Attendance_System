function selectRole(role) {
    var selectedRoleElement = document.getElementById(role);
    document.querySelectorAll('.role').forEach(function(elem) {
        elem.classList.remove('active');
    });
    selectedRoleElement.classList.add('active');
    document.getElementById('selectedRole').value = role;
    

   
}
