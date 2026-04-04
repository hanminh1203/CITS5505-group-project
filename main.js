$(document).ready(function () {
    const ROUTES = {
        'login': {page: 'login', js: false},
        'profile': {page: 'profile', js: false},
        'requests': {page: 'requests', js: false},
        'dashboard': {page: 'dashboard', js: false},
        'dev': {page: 'dev', js: false},
        'home': {page: 'home', js: false},
        'requests\/(?<requestId>\\d+)': {page: 'request', js: true}
    }
    function loadComponent(elementSelector, componentPath) {
        $(elementSelector).load('src/components/' + componentPath + '.component.html', function (response, status) {
            $.getScript('src/components/' + componentPath + '.component.js');
        });
    }


    function selectComponent(hash) {
        for (let pattern of Object.keys(ROUTES)) {
            let matcher = new RegExp(`^${pattern}$`);
            let match = hash.match(matcher)
            if (match) {
                return {
                    route: ROUTES[pattern],
                    params: match.groups
                };
            }
        }
        return {
            route: ROUTES['home'],
        };
    }
    
    function router() {
        const hash = $(location).attr('hash').substring(1) || 'home';
        const routeInfo = selectComponent(hash);
        const page = routeInfo.route.page;
        if (routeInfo.route.js) {
            import(`./src/pages/${page}.page.js`).then((module) => {
                const pageComponent = new module.Page($('main'), routeInfo.params);
                pageComponent.render();
            });
        } else {
            $('main').load('src/pages/' + page + '.page.html', function (response, status) {
                $.getScript('src/pages/' + page + '.page.js');
            });
        }
        $('main').removeClass().addClass(page);
    }

    loadComponent('header', 'header');
    $("footer").load("src/components/footer.component.html");
    $(window).on('hashchange load', router);
});