
$(function() {   
    $('input[type="file"]').change(function () {
        var fileName = $(this).val();
        upload_banner(this);
    });
});

function openfile(element) {
    $(element).prev('input[type="file"]').click();
}

function upload_banner(file) {
    var data = new FormData();
    data.append('file', $(file)[0].files[0]);
    $.ajax({
        url: "/upload_banner", //the page containing python script
        type: "POST", //request type,
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success:function(result){
            console.log(result.abc);
        },
        error: function () {
            console.log("upload error")
        },
    });
} 