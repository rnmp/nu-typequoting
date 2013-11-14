$(function(){
	var timer = 0;
	$('.js-load').each(function(){
		timer = timer + 300;
		var $this = $(this);
		setTimeout(function(){$this.removeClass('hidden').addClass('load-animation')}, timer)
	})
	setTimeout(function(){
		$('#prompt-countdown').countdown({
			until: 59, 
			layout: '{sn} {sl}', 
			onExpiry: function() {
				$('#id_body').attr('disabled', 'true');
				$('#prompt-countdown').text('…nevermind');
				$('#id_author_name').focus();
			}
		});
	}, 1100);
});