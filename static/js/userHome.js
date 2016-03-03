$(function() {
    $.ajax({
        url: '/getPost',
        type: 'GET',
        success: function(res) {
            // HTML structure to be created dynamically
            var div = $('<div>')
                .attr('class', 'list-group')
                .append($('<a>')
                       .attr('class', 'list-group-item active')
                       .append($('<h4>')
                              .attr('class', 'list-group-item-heading'),
                              $('<p>')
                              .attr('class', 'list-group-item-text')));
            
            // Parse JSON to object
            var postObj = JSON.parse(res);
            var post = '';
            
            // Clone above div, insert data and loop
            $.each(postObj, function(index, value) {
                post = $(div).clone();
                $(post).find('h4').text(value.Title);
                $(post).find('p').text(value.Description);
                $('.jumbotron').append(post);
            })
        },
        error: function(error) {
            console.log(error);
        }
    });
});