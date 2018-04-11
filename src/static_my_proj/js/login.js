$(document).ready(function() {
  /* Login form AJAX */
$('#loginform').submit(function(e){
	var formId = $(this).attr('id');
	var submitBtn = $(this).find('input[type=submit]');
	var loginForm = $(".login-form")
  var loginFormMethod = loginForm.attr("method")
	var loginFormEndpoint = loginForm.attr("action")
	alert(loginFormEndpoint);
	submitBtn.prop('disabled', true);
	$('#no-user-error').css('display', 'none');
	$('#password-error').css('display', 'none');
	e.preventDefault();
	$.ajax({
		url: loginFormEndpoint, // the file to call
		type: "POST", // GET or POST
		data: $(this).serialize(),// get the form data

		success: function(data){
			alert(data);
			var login_response = jQuery.parseJSON(data);
			console.log(login_response);
			if (login_response.user == "nouser"){
				$('#no-user-error').css('display', 'block');
				submitBtn.prop('disabled', false);
			}
			else if (login_response.user == "password wrong") {
				$('#password-error').css('display', 'block');
				submitBtn.prop('disabled', false);
			}
			else if ((login_response.user == "not active") && (login_response.user_phone)) {
				$('#login-modal').modal('hide');
				$('#OTP-modal').modal({backdrop:'static', keyboard:false,show:true});
				$('#verify-user-phone').html(login_response.user_phone);
				document.getElementById(formId).reset();
				submitBtn.prop('disabled', false);
			}
			else {
				if (login_response.login == "Failed") {
					alert("Invalid Login!");

				} else {
					document.getElementById(formId).reset();
					$('#login-modal').modal('hide');
					setTimeout(function() {
					location.reload();
					}, 400);
				}
			}/*./else*/
			submitBtn.prop('disabled', false);
			$('#spinner-login').css('display', 'none');
		},/* end of Success */
		error: function(data) {
			$('#loginModal').modal('hide');
			$('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
		}/*  end of error */
	});/*./ajax*/
});
/*End of loin form AJAX */
})
