$('#messaging-navi .navbar-nav a').on('click', function () {
	localStorage.setItem('lastNaviItem', $(this).attr('href'));
});

var lastNaviItem = localStorage.getItem('lastNaviItem');
if (lastNaviItem) {
	$('#messaging-navi .navbar-nav').find('li.active').removeClass('active');
	$('#messaging-navi .navbar-nav').find('a[href="' + lastNaviItem + '"]').parent('li').addClass('active');
}
