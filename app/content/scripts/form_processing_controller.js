// к примеру, для вывода имени изображения в тег span

function forms_processing_controller() {
    $('input[type=file]').on('change', function (event) {
        if (this.files[0]) {
            const splittedFakePath = this.value.split('\\');
            $('#' + $(event.target).attr("id") + "_span").text(splittedFakePath[splittedFakePath.length - 1]);
        } else {
            $('#' + $(event.target).attr("id") + "_span").text("Файл не выбран");
        }
    });
}