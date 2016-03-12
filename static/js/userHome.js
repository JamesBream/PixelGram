// PixelGram
// User Home page javascript

$(function(){
    // Initial grid population
    GetPosts();
    
    // Update button on-click event
    $('#btnUpdate').click(function() {
        $.ajax({
            url: '/updatePost',
            data: {
                title: $('#editTitle').val(),
                description: $('#editDescription').val(),
                id: localStorage.getItem('editId')
            },
            type: 'POST',
            success: function(res) {
                $('#editModal').modal('hide');
            
                // Re populate the grid
                GetPosts();
            },
            error: function(error) {
                console.log(error);
            }
        })
    });
});

function GetPosts() {
    $.ajax({
        url: '/getPost',
        type: 'GET',
        success: function(res) {
            
            // Parse JSON to object
            var postObj = JSON.parse(res);
            
            // Empty template and append
            $('#ulist').empty();
            $('#listTemplate').tmpl(postObj).appendTo('#ulist');
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function Edit(elm) {
    // Store ID in local storage use later
    localStorage.setItem('editId', $(elm).attr('data-id'));
    $.ajax({
        url: '/getPostById',
        data: {
            id: $(elm).attr('data-id')
        },
        type: 'POST',
        success: function(res) {
            // Parse the received JSON string (from python)
            var data = JSON.parse(res);
            
            // Populate the pop up
            $('#editTitle').val(data[0]['Title']);
            $('#editDescription').val(data[0]['Description']);
            
            // Trigger pop up
            $('#editModal').modal();
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function ConfirmDelete(elm) {
    localStorage.setItem('deleteId', $(elm).attr('data-id'));
    $('#deleteModal').modal();
}

function Delete() {
    $.ajax({
        url: '/deletePost',
        data: {
            id: localStorage.getItem('deleteId')
        },
        type: 'POST',
        success: function(res) {
            // Parse the received JSON string (from python)
            var result = JSON.parse(res);
            if (result.status == 'OK') {
                $('#deleteModal').modal('hide');
                GetPosts();
            } else {
                alert(result.status);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}