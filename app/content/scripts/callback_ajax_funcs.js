function url_processing(event){
    const xhr = event.target;
    if (xhr.readyState === 2){
        // получены загаловки
    }
    if (xhr.readyState !== 4) return;

    if (xhr.status === 200) {
        document.querySelectorAll("main")[0].innerHTML = " " + xhr.responseText;
    } else if (xhr.status === 201){
        document.querySelectorAll("main")[0].innerHTML = " " + xhr.responseText;
    } else if (xhr.status === 404){
        document.querySelectorAll("main")[0].innerHTML = " " + xhr.responseText;
    }
    urls_as_ajax();
    send_form_as_ajax();
}