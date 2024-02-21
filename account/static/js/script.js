function selectRole(role) {
    var selectedRoleElement = document.getElementById(role);
    document.querySelectorAll('.role').forEach(function(elem) {
        elem.classList.remove('active');
    });
    selectedRoleElement.classList.add('active');
    document.getElementById('selectedRole').value = role;
    var idInput = document.getElementById('idInput');
    if (role == 'teacher'){
        idInput.placeholder = 'Teacher Number';
    }
    else if(role == 'student'){
        idInput.placeholder = 'Student Number';
    }
    else{
        idInput.placeholder = 'Admin Number';
    }

   
}
