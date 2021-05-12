
function set_fixed_position_event() {
    $(".aside_admin_shell").scroll(event => {
        const obj = $(event.target);
        if (obj.offset().top < 5) {
            obj.css("position", "fixed")
        }
    });
}

jQuery(document).ready(set_fixed_position_event);