$(function() {   
    $('input[type="file"]').change(function () {
        var fileName = $(this).val();
        selected_file(this);
    });
});

function openfile(element) {
    $(element).prev('input[type="file"]').click();
}

function selected_file(file) {
    var current_row = $(file).closest('tr');
    var current_td = $(file).parent();
    current_row.find(".btn-update").hide();
    current_row.find(".btn-cancel").show();
    current_row.find(".btn-save").show();    
    // load new banner
    if ($(file)[0].files && $(file)[0].files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var old_image =  $(file).closest("tr").find("td:eq(1) img").attr('src')
            $(file).closest("tr").find("td:eq(1) img").attr('url', old_image);
            $(file).closest("tr").find("td:eq(1) img").attr('src', e.target.result);
        }
        reader.readAsDataURL($(file)[0].files[0]);
    }
}

function upload_banner(element) {
    var current_row = $(element).closest('tr');
    var data = new FormData();
    var current_file = $(element).parent().find('input[type="file"]')[0].files[0]
    data.append('file', current_file);
    data.append('number', current_row.find("td:eq(0)").text());
    data.append('file_name', current_row.find("td:eq(2)").text());
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

function cancel_update(element) {
    var current_row = $(element).closest('tr');
    current_row.find(".btn-update").show();
    current_row.find(".btn-cancel").hide();
    current_row.find(".btn-save").hide();
    current_row.find("td:eq(1) img").attr('src', current_row.find("td:eq(1) img").attr('url'));
}

function delete_banner(element) {
    var current_row = $(element).closest('tr');
    var data = new FormData();
    data.append('file_name', current_row.find("td:eq(2)").text());
    data.append('row_index', current_row.find("td:eq(0)").text());
    $.ajax({
        url: "/delete_banner", //the page containing python script
        type: "DELETE", //request type,
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (result) {
            console.log(result);
        },
        error: function () {
            console.log("upload error")
        },
    });
}