function selectRole(role) {
    document.querySelectorAll('.role').forEach(function(elem) {
        elem.classList.remove('active');
    });

    document.querySelector('.role.' + role).classList.add('active');
}
