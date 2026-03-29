
$(document).ready(function () {
    function loadComponent(elementSelector, componentPath) {
        $(elementSelector).load('src/components/' + componentPath + '.component.html', function (response, status) {
            $.getScript('src/components/' + componentPath + '.component.js');
        });
    }
    
    function router() {
        const hash = $(location).attr('hash').substring(1) || 'home';

        $('main').load('src/pages/' + hash + '.page.html', function (response, status) {
            if (status !== 'success') {
                $('main').load('src/pages/404.page.html', function (errorPageResponse, errorPageStatus) {
                    $('main').removeClass().addClass('404');
                });
                return;
            }
            $('main').removeClass().addClass(hash);
            $.getScript('src/pages/' + hash + '.page.js');
        });
    }

    loadComponent('header', 'header');
    $("footer").load("src/components/footer.component.html");
    $(window).on('hashchange load', router);
});
