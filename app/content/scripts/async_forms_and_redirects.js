// function send_form_as_ajax() {
//     const token = localStorage.getItem('token')
//     console.log('--------------------');
//     console.log("Асинхронность формы запущена");
//     $('[type=submit], #submit').click((event) => {
//
//         event.preventDefault();
//         setTimeout(() => {
//             const xhr = new XMLHttpRequest();
//             const $current_form = $(event.target).parents("form");
//             let action = $current_form.attr('action')
//
//             xhr.open($current_form.attr('method'), action, true);
//
//             // xhr.setRequestHeader("Accept-Encoding", "gzip, deflate, br");
//             xhr.setRequestHeader("Accept-Language", "ru,en;q=0.9,la;q=0.8");
//             xhr.setRequestHeader("Cache-Control", "no-cache");
//             // xhr.setRequestHeader("Connection", "keep-alive");
//             xhr.setRequestHeader("Pragma", "no-cache");
//             // xhr.setRequestHeader("Sec-Fetch-Dest", "empty");
//             // xhr.setRequestHeader("Sec-Fetch-Mode", "cors");
//             // xhr.setRequestHeader("Sec-Fetch-Site", "same-origin");
//
//             xhr.setRequestHeader("Accept", "application/json");
// //            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
//             xhr.setRequestHeader("RequestedWith3456i876543", "XMLHttpRequest");
//
//             if (token) {
//                 xhr.setRequestHeader('Authorization', 'Bearer ' + token);
//             }
//
//             // xhr.send($current_form.find("input, select").not('[type="submit"]').serialize());
//             let send_data = {};
//             let form_fields = $current_form.find("input, select").not('[type="submit"]');
//
//             console.log(form_fields);
//             [...form_fields].map( i => {
//                 send_data[$(i).attr('name')] = $(i).val();
//             });
//
//             console.log(send_data)
//             xhr.send(JSON.stringify(send_data));
//             xhr.onreadystatechange = (event) => { // (3)
//
//                 if (xhr.readyState === 2) {
//                     // получены загаловки
//                 }
//                 if (xhr.readyState !== 4) return;
//
//
//                 if (xhr.status === 200 || xhr.status === 201) {
//                     // вывести результат
//                     if (xhr.status === 200) {
//                         console.log(xhr.responseText);
//                         document.querySelectorAll("html")[0].innerHTML = " " + xhr.responseText;
//
//                         send_form_as_ajax();
//                     } else if (xhr.status === 201) {
//                         console.log(xhr.responseText);
//                     }
//
//
//                 } else if (xhr.status === 400) {
//                     let data = JSON.parse(xhr.responseText);
//                     if (data.type) {
//
//                         if (data["type"] === "fields_no_unique" && data["errors"]) {
//                             [...Object.keys(data["errors"])].map(i => {
//                                 return $("#" + i).html(data["type"][i]);
//                             }).map(i => {
//                                 if (i.html() === "") {
//                                     i.removeClass('error')
//                                 } else {
//                                     i.addClass('error');
//                                 }
//                             });
//                         } else if (data["type"] === "fields_create_entity") {
//
//
//                         }
//                     } else {
//                         // обработать ошибку
//                     }
//                 } else if (xhr.status === 401) {
//
//                 }
//                 urls_as_ajax();
//                 set_fixed_position_event();
//             }
//         })
//
//         // const login_form = new FormData();
//         // login_form.append('username', $("#username").val());
//         // login_form.append('password', $("#password").val());
//         //
//         // $.ajax({
//         //     type: 'post',
//         //     dataType: 'json',
//         //     contentType: false,
//         //     processData: false,
//         //     data: ,
//         //
//         //     success: data => {  }
//         // });
//     });
// }

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
            let form_fields = $current_form.find("input, select").not('[type="submit"]');



            let authorization = false;
            if ($current_form.attr('id') && $current_form.attr('id') === "authorization") {
                authorization = true;
                send_data = form_fields.serialize();
            } else {

                [...form_fields].map(i => {
                    const el = $(i);
                    if (el.attr("type") === "radio" || el.attr("type") === "checkbox"){
                        send_data[el.attr('name')] = el.prop('checked')? true: false;
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