export class HeaderComponent {
    constructor(container) {
        this.container = container;
    }

    template() {
        return $.get(`src/components/header.component.html`);
    }

    async render() {
        this.container.html(await this.template());
        this.onInit();
    }

    onInit() {
        $('#logout-btn').click(() => {
            sessionStorage.setItem('isLoggedIn', 'false');
            window.location.hash = '#home';
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