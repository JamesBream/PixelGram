/* Post usre signup info to server and handle result */
$(function(){
	$('#btnSignUp').click(function(){
		
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
                var data = JSON.parse(response);
                console.log(data['message']);
                signup_alert.warning(data['message']);
			},
			error: function(error){
				console.log(error);
                signup_alert.warning("An error occured, please try again.");
			}
		});
	});
});

signup_alert = function() {}
signup_alert.success = function(message) {
    $('#signup_alert_placeholder').html('<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>'+message+'</span></div>')
}
signup_alert.warning = function(message) {
    $('#signup_alert_placeholder').html('<div class="alert alert-warning alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>'+message+'</span></div>')
}

$(function () {
  $('#sign-up-form').parsley().on('field:validated', function() {
    var ok = $('.parsley-error').length === 0;
    $('.bs-callout-info').toggleClass('hidden', !ok);
    $('.bs-callout-warning').toggleClass('hidden', ok);
  })
  .on('form:submit', function() {
    return false; // Don't submit form for this demo
  });
});