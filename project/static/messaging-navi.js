$('#messaging-navi .navbar-nav a').on('click', function () {
	localStorage.setItem('lastNaviItem', $(this).attr('href'));
});

var lastNaviItem = localStorage.getItem('lastNaviItem');
if (lastNaviItem) {
	$('#messaging-navi .navbar-nav').find('li.active').removeClass('active');
	$('#messaging-navi .navbar-nav').find('a[href="' + lastNaviItem + '"]').parent('li').addClass('active');
}

// Enable Archived tile when message is archived and user is redirected to archived messages
if (window.location.href.indexOf("archived") > -1) {
	$('#messaging-navi .navbar-nav').find('li.active').removeClass('active');
	$('#messaging-navi .navbar-nav').find('a[href="/messages/archived/"]').parent('li').addClass('active');
}