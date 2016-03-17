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
            
            // Set thumbnail
            $('#imgUpload').attr('src', filePath);
            
            // Store filePath in hidden input
            $('#filePath').val(filePath);
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
})