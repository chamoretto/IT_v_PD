function send_form_as_ajax() {
    const token = localStorage.getItem('token')
    console.log('--------------------');
    $('input[type=submit], button[type=submit], #submit').click((event) => {


        console.log(event)
        console.log(event.target)

        event.preventDefault();
        setTimeout(() => {
            const xhr = new XMLHttpRequest();
            const $current_form = $(event.target).parents("form");
            xhr.open($current_form.attr('method'), $current_form.attr('action'), true);

            xhr.setRequestHeader("Accept-Encoding", "gzip, deflate, br");
            xhr.setRequestHeader("Accept-Language", "ru,en;q=0.9,la;q=0.8");
            xhr.setRequestHeader("Cache-Control", "no-cache");
            xhr.setRequestHeader("Connection", "keep-alive");
            xhr.setRequestHeader("Pragma", "no-cache");
            xhr.setRequestHeader("Sec-Fetch-Dest", "empty");
            xhr.setRequestHeader("Sec-Fetch-Mode", "cors");
            xhr.setRequestHeader("Sec-Fetch-Site", "same-origin");

            xhr.setRequestHeader("Accept", "application/json, text/plain, */*");
//            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

            if (token) {
                xhr.setRequestHeader('Authorization', 'Bearer ' + token);
            }

            xhr.send($current_form.find("input, select").not('[type="submit"]').serialize());
            xhr.onreadystatechange = () => { // (3)
                if (xhr.readyState === 2) {
                    // получены загаловки
                }
                if (xhr.readyState !== 4) return;

                if (xhr.status === 200 || xhr.status === 201) {
                    // вывести результат
                    console.log(xhr.responseText);
                    document.querySelectorAll("html")[0].innerHTML = " " + xhr.responseText;

                    send_form_as_ajax();

                    //[...document.querySelectorAll("script")].map(i => eval(i.innerHTML))
                    //eval($("script", doc).text())
                    // document.html = " " + xhr.responseText;
                } else if (xhr.status === 400) {
                    let data = JSON.parse(xhr.responseText);
                    if (data.type) {

                        if (data["type"] === "fields_no_unique" && data["errors"]) {
                            [...Object.keys(data["errors"])].map(i => {
                                return $("#" + i).html(data["type"][i]);
                            }).map(i => {
                                if (i.html() === "") {
                                    i.removeClass('error')
                                } else {
                                    i.addClass('error');
                                }
                            });
                        }

                        
                    }
                } else {
                    // обработать ошибку
                }
            }
        });
    })

    // const login_form = new FormData();
    // login_form.append('username', $("#username").val());
    // login_form.append('password', $("#password").val());
    //
    // $.ajax({
    //     type: 'post',
    //     dataType: 'json',
    //     contentType: false,
    //     processData: false,
    //     data: ,
    //
    //     success: data => {  }
    // });
}

send_form_as_ajax()
