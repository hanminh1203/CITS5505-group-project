
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
                $('main').load('src/pages/error-404.page.html', function (errorPageResponse, errorPageStatus) {
                    $('main').removeClass().addClass('error-404');
                    if (errorPageStatus === 'success') {
                        $.getScript('src/pages/error-404.page.js');
                    } else {
                        $('main').empty().append(
                            '<p class="p-4 text-center text-secondary">Unable to load this page.</p>'
                        );
                    }
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
