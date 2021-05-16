
function help_to_change_html_from_ajax(selector, html_data){
    if (html_data) {
        console.log( $(html_data).find(selector));

        // if (((selector[0] === "." || selector[0] === "#") && html_data.includes(selector.substr(1))) || (html_data.includes(selector))) {
        if (String($(html_data).find(selector).prevObject[0]).includes(selector)){
            $(selector).replaceWith(function () {
                return html_data;
            });
            console.log('заменяем вместе с тегом', selector)
        } else {
            $(selector).html(html_data);
            console.log('заменяем содержимое тега', selector)
        }
    }
}

function change_html_from_ajax(json_data){
    const data = JSON.parse(json_data);
    console.log(data);
    if (data.my_response_type === "html"){
        help_to_change_html_from_ajax("#main", data.main);
        help_to_change_html_from_ajax("#alert", data.alert);
        help_to_change_html_from_ajax("#admin_shell", data.admin_shell);
    }
}

function url_processing(event){
    const xhr = event.target;
    if (xhr.readyState === 2){
        // получены загаловки
    }
    if (xhr.readyState !== 4) return;

    if (xhr.status === 200) {
        change_html_from_ajax(xhr.responseText);
        // document.querySelectorAll("main")[0].innerHTML = " " + xhr.responseText;
    } else if (xhr.status === 201){
        document.querySelectorAll("main")[0].innerHTML = " " + xhr.responseText;
    } else if (xhr.status === 401){
        change_html_from_ajax(xhr.responseText);
        // document.querySelectorAll("main")[0].innerHTML = " " + xhr.responseText;
    } else if (xhr.status === 404){
        change_html_from_ajax(xhr.responseText);
        // document.querySelectorAll("main")[0].innerHTML = " " + xhr.responseText;
    }
    after_load_funcs_run();
    // urls_as_ajax();
    // send_form_as_ajax();
    // set_fixed_position_event();
}

function authorization_response_processing(event){
    const xhr = event.target;
    if (xhr.readyState === 2){
        // получены загаловки
    }
    if (xhr.readyState !== 4) return;

    if (xhr.status === 200) {

        const json_data = JSON.parse(xhr.responseText);
        console.log(json_data);
        if (json_data["access_token"]){
            console.log('записываем токен');
            localStorage.setItem('token', json_data["access_token"]);
            console.log('записывали токен');
        }
        // url_processing(event);
    }
    // urls_as_ajax();
    // send_form_as_ajax();
    // set_fixed_position_event();
    after_load_funcs_run()
}