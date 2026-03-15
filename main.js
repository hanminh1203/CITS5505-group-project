$(function () {
    $("header").load("src/components/header.component.html");
    $("footer").load("src/components/footer.component.html");
    
    loadPageByHash();
    $(window).on('hashchange', function () {
        loadPageByHash();
    });
})

function loadPageByHash() {
    const hash = $(location).attr('hash').substring(1) || 'home';
    selectPage(hash);
}

function selectPage(page) {
    $('#main-content').load('src/pages/' + page + '.page.html');
    $('#main-content').removeClass().addClass(page);
    $('.navbar .nav-item').removeClass('active');
    $('.navbar .link-nav-' + page).parent().addClass('active');
}