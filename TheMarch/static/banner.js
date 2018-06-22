$(document).ready(function () {
    // Basic
    $('.dropify').dropify();

    // Used events
    var drEvent = $('.dropify').dropify();
    drEvent.on('dropify.beforeClear', function (event, element) {
        return confirm("Do you really want to delete \"" + element.file.name + "\" ?");
    });
    drEvent.on('dropify.afterClear', function (event, element) {
        alert('File deleted');
    });
    drEvent.on('dropify.errors', function (event, element) {
        console.log('Has Errors');
    });
    var drDestroy = $('.dropify').dropify();
    drDestroy = drDestroy.data('dropify')
    $('#toggleDropify').on('click', function (e) {
        alert('sdsd');
        e.preventDefault();
        if (drDestroy.isDropified()) {
            drDestroy.destroy();
        } else {
            drDestroy.init();
        }
    })
});