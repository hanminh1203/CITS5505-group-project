$(document).ready(function () {
    // Login logic
    function updateHeader() {
        if (sessionStorage.getItem('isLoggedIn') === 'true') {
            $('#header-login-group').addClass('d-none').hide();
            $('#header-logout-group').removeClass('d-none').show();
        } else {
            $('#header-login-group').removeClass('d-none').show();
            $('#header-logout-group').addClass('d-none').hide();
        }

        const hash = $(location).attr('hash').substring(1) || 'home';
        $('.navbar .nav-link').removeClass('active');
        $('.navbar .nav-link-' + hash).addClass('active')
        // TODO bug when hash has /
    }

    $('#logout-btn').click(function () {
        sessionStorage.setItem('isLoggedIn', 'false');
        window.location.hash = '#home';
    });

    $(window).on('hashchange load', updateHeader);
    updateHeader();
});