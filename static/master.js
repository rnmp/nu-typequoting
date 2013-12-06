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
					until: 90,
					format: 'S', 
					layout: '{sn} {sl}', 
					onExpiry: function() {
						$('#id_body').attr('readonly', 'true');
						$(this).text('…nevermind');
						$('#id_author_name').focus();
					}
				});
			}
		}, timer);
	});
});

function like(event) {
    var btn = $(event.currentTarget);;
    event.preventDefault();
    return $.ajax({
      dataType: 'json',
      url: btn.attr('href'),
      success: function(response) {
        if (response.success) {
          btn.siblings('.likes-display').show().find(
              '.num-likes').text(response.like_count);
          btn.hide();
        } else {
          btn.text(response.message);
        }
      }
    });
}

$(function(){
	$('.share-link').on('click', function(){
		$(this).select();
	})

    $('.like-button').on('click', like)
});
