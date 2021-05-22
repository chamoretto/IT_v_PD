// к примеру, для вывода имени изображения в тег span

function forms_processing_controller() {
    $('input[type=file]').off('change.select_file').on('change.select_file', function (event) {
        if (this.files[0]) {
            const splittedFakePath = this.value.split('\\');
            $('#' + $(event.target).attr("id") + "_span").text(splittedFakePath[splittedFakePath.length - 1]);
        } else {
            $('#' + $(event.target).attr("id") + "_span").text("Файл не выбран");
        }
    });
}