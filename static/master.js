var timer = 0;
$(window).load(function(){
	var len = $('.js-load').length;
	$('.js-load').each(function(index, elements){
		timer = timer + 50;
		var $this = $(this);
		setTimeout(function(){
			$this.removeClass('hidden').addClass('load-animation')
			if (index == len -1) { 
				$('#prompt-countdown').countdown({
					until: 59, 
					layout: '{sn} {sl}', 
					onExpiry: function() {
						$('#id_body').attr('disabled', 'true');
						$(this).text('…nevermind');
						$('#id_author_name').focus();
					}
				});
			}
		}, timer);
	});
});

$(function(){
	$('.share-link').on('click', function(){
		$(this).select();
	})
});