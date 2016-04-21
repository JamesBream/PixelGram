/* Post usre signup info to server and handle result */
$(function(){
	$('#btnSignUp').click(function(){
		
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
                
                var data = JSON.parse(response);
                
                if (data.hasOwnProperty('success')) {
                    signup_alert.success(data.success);
                }
                else if (data.hasOwnProperty('error')) {
                    signup_alert.warning("Please verify your details are correct");
                    console.log(response);
                }
                else {
                    console.log(response);
                }
			},
			error: function(error){
				console.log(error);
                signup_alert.warning("An error occured, please try again.");
			}
		});
	});
});

// User alerts
signup_alert = function() {}
signup_alert.success = function(message) {
    $('#signup_alert_placeholder').html('<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>'+message+'</span></div>')
}
signup_alert.warning = function(message) {
    $('#signup_alert_placeholder').html('<div class="alert alert-warning alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>'+message+'</span></div>')
}