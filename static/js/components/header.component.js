export class HeaderComponent {
    onInit() {
        $('#logout-btn').click(() => {
            sessionStorage.setItem('isLoggedIn', 'false');
            window.location.url = '/home';
        });
    }

    updateHeader() {
        if (sessionStorage.getItem('isLoggedIn') === 'true') {
            $('#header-login-group').addClass('d-none').hide();
            $('#header-logout-group').removeClass('d-none').show();
        } else {
            $('#header-login-group').removeClass('d-none').show();
            $('#header-logout-group').addClass('d-none').hide();
        }
    }

    updateActiveLink(routeInfo) {
        const page = routeInfo.route.page;
        $('.navbar .nav-link').removeClass('active');
        $('.navbar .nav-link-' + page).addClass('active')
    }
}

$(document).ready(() => {
    new HeaderComponent().onInit();
})