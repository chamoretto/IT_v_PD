

function send_form_as_ajax() {
    const token = localStorage.getItem('token')
    console.log('--------------------');
    console.log("Новоя асинхронность формы запущена");
    $('[type=submit], #submit').off("click.ajax_form_click").on({'click.ajax_form_click': (event) => {
        event.preventDefault();
        setTimeout(() => {
            const $current_form = $(event.target).parents("form");
            const action = $current_form.attr('action')
            const method = $current_form.attr('method');



            let send_data = {};
            let form_fields = $current_form.find("input, select, textarea").not('[type="submit"]');



            let authorization = false;
            if ($current_form.attr('id') && $current_form.attr('id') === "authorization") {
                authorization = true;
                send_data = form_fields.serialize();
            } else {

                [...form_fields].map(i => {
                    const el = $(i);
                    if (el.attr("type") === "radio" || el.attr("type") === "checkbox"){
                        send_data[el.attr('name')] = el.prop('checked')? true: false;
                    } else if (el.attr("type") === "file" || el.attr("type") === "image"){
                        console.log([el.val()], "---", [el.attr("value")]);
                        if (el.attr("value") === ""){

                        }
                        send_data[el.attr('name')] = el.attr("value");
                    } else {

                        send_data[el.attr('name')] = el.val();
                    }

                });

                console.log(send_data);
                send_data = JSON.stringify(send_data);
            }
            console.log(send_data);

            send_ajax(action, method, authorization_response_processing, send_data, true, true, authorization)
        });
    }});
}


// send_form_as_ajax();