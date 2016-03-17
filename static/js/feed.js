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
                        div.append(CreateThumb(data[i].Id, data[i].Title, data[i].Description, data[i].FilePath));
                        $('.well').append(div);
                    } else {
                        div.append(CreateThumb(data[i].Id, data[i].Title, data[i].Description, data[i].FilePath));
                        itemsPerRow++;
                    }
                } else {
                    $('.well').append(div);
                    div = $('<div>').attr('class', 'row');
                    div.append(CreateThumb(data[i].Id, data[i].Title, data[i].Description, data[i].FilePath));
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
function CreateThumb(id, title, desc, fpath) {
    
    var mainDiv = $('<div>').attr('class', 'col-sm-4 col-md-4');
    
    var thumbnail = $('<div>').attr('class', 'thumbnail');
    
    var img = $('<img>').attr({
        'src': fpath,
        'data-holder-rendered': true,
        'style': 'height: 150px; width: 150px; display: block'
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
    
    p.append(btn.append(span));
    
    caption.append(title);
    caption.append(desc);
    caption.append(p);
    
    thumbnail.append(img);
    thumbnail.append(caption);
    mainDiv.append(thumbnail);
    return mainDiv;
}






