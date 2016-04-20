// PixelGram
// New post page javascript

// Initialise BlueImp file uploader
$(function() {
    $('#fileupload').fileupload({
        url: 'upload',
        dataType: 'json',
        add: function(e, data) {
            data.submit();
        },
        success: function(response, status) {
            
            var filePath = 'static/uploads/' + response.filename;
            
            // If error received, display it to the user
            if (response.hasOwnProperty('error')) {
                upload_alert.warning(response.error);
                console.log("Encountered an error!");
            }
            else {
                upload_alert.success("Image uploaded successfully!")
                // Set thumbnail
                $('#imgUpload').attr('src', filePath);
            
                // Store filePath in hidden input
                $('#filePath').val(filePath);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
})

// User alerts
upload_alert = function() {}
upload_alert.success = function(message) {
    $('#upload_alert_placeholder').html('<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>'+message+'</span></div>')
}
upload_alert.warning = function(message) {
    $('#upload_alert_placeholder').html('<div class="alert alert-warning alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>'+message+'</span></div>')
}