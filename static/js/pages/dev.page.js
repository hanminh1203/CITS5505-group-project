$(document).ready(function () {
    $('#is-logged-in').prop('checked', sessionStorage.getItem('isLoggedIn') === 'true');
    
    $('#is-logged-in').change(function () {
        const isLoggedIn = $(this).is(':checked');
        sessionStorage.setItem('isLoggedIn', isLoggedIn ? 'true' : 'false');
        location.reload();
    });
});