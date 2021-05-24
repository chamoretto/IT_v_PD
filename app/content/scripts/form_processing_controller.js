// к примеру, для вывода имени изображения в тег span

function forms_processing_controller() {
    $('input[type=file]').off('change.select_file').on('change.select_file', function (event) {

        if (this.files[0]) {
            const splittedFakePath = this.value.split('\\');
            $('#' + $(event.target).attr("id") + "_span").text(splittedFakePath[splittedFakePath.length - 1]);
            $(event.target).attr("value", splittedFakePath[splittedFakePath.length - 1])
        } else {
            $('#' + $(event.target).attr("id") + "_span").text("Файл не выбран");
            $(event.target).attr("value", "")
        }

        console.log($(event.target));
        console.log($(event.target)[0].files[0]);
//        console.log($(event.target).attr("files"));
        const fd = new FormData();
		fd.append('file', $(event.target)[0].files[0]);
//		fd.append('file_id',  JSON.stringify({ "file_id":  $(event.target).attr("id") } ) );
		send_ajax("/upload_file", "POST", url_processing, fd, true, true, false);

    });
}