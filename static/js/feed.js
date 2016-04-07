// PixelGram
// Feed page javascript

// Ajax to retrieve all posts - TODO: needs pagination!
$(function() {
    $.ajax({
        url: '/getAllPosts',
        type: 'GET',
        success: function(res) {
            var data = JSON.parse(res);
            
            var itemsPerRow = 0;
            var div = $('<div>').attr('class', 'row');
            for (var i = 0; i < data.length; i++) {
                
                // 3 items in each grid row
                if (itemsPerRow < 3) {
                    
                    if (i == data.length - 1) {
                        div.append(CreateThumb(data[i].Id, data[i].Title, data[i].Description, data[i].FilePath, data[i].Like, data[i].HasLiked));
                        $('.well').append(div);
                    } else {
                        div.append(CreateThumb(data[i].Id, data[i].Title, data[i].Description, data[i].FilePath, data[i].Like, data[i].HasLiked));
                        itemsPerRow++;
                    }
                } else {
                    $('.well').append(div);
                    div = $('<div>').attr('class', 'row');
                    div.append(CreateThumb(data[i].Id, data[i].Title, data[i].Description, data[i].FilePath, data[i].Like, data[i].HasLiked));
                    if (i == data.length - 1) {
                        $('.well').append(div);
                    }
                    itemsPerRow = 1;
                }
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
})

// Function to create the thumbnail html
// See: https://gist.github.com/JamesBream/75e6b9ae85d42a172837
function CreateThumb(id, title, desc, fpath, like, hasLiked) {
    
    var mainDiv = $('<div>').attr('class', 'col-sm-4 col-md-4');
    
    var thumbnail = $('<div>').attr('class', 'thumbnail');
    
    var img = $('<img>').attr({
        'src': fpath,
        'data-holder-rendered': true,
        'style': 'height: 255px; width: 150px; display: block'
    });
    
    var caption = $('<div>').attr('class', 'caption');
    
    var title = $('<h3>').text(title);
    
    var desc = $('<p>').text(desc);
    
    var p = $('<p>');
    
    var btn = $('<button>').attr({
        'id': 'btn_' + id,
        'type': 'button',
        'class': 'btn btn-danger btn-sm'
    });
    
    var span = $('<span>').attr({
        'class': 'glyphicon glyphicon-thumbs-up',
        'aria-hidden': 'true'
    });
    
    var likes = $('<span>').attr({'aria-hidden': 'true', 'id': 'span_' + id});
    
    if(hasLiked == "1") {
        likes.html('&nbsp;You & ' + (Number(like) - 1) + ' others');
    } else {
        likes.html('&nbsp;' + like + ' like(s)');
    }
    
    p.append(btn.append(span));
    p.append(likes);
    
    caption.append(title);
    caption.append(desc);
    caption.append(p);
    
    thumbnail.append(img);
    thumbnail.append(caption);
    mainDiv.append(thumbnail);
    return mainDiv;
}

// Onclick function for 'Like' button
$(document).on('click', '[id^="btn_"]', function() {
    var spId = $(this).attr('id').split('_')[1];
    $.ajax({
        url: '/addUpdateLike',
        method: 'POST',
        data: {
            post: $(this).attr('id').split('_')[1],
            like: 1
        },
        success: function(response) {
            // Parse returned like status and count
            var obj = JSON.parse(response);
            
            if (obj.likeStatus == "1") {
                $('#span_' + spId).html('&nbsp;You & ' + (Number(obj.total) - 1) + ' Others');
            } else {
                $('#span_' + spId).html('&nbsp;' + obj.total + ' like(s)');
            }
            console.log(response);
        },
        error: function(error) {
        console.log(error);
        }
    });
});





