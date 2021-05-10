$('#submit').click((event) => {
    console.log("авторизация")
    event.preventDefault();
    // const login_form = new FormData();
    // login_form.append('username', $("#username").val());
    // login_form.append('password', $("#password").val());

    $.ajax({
        url: '{#{auth_url}#}',
        headers: {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Basic Og==",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
        },
        type: 'post',
        dataType: 'json',
        contentType: false,
        processData: false,
        data: $("#oauth_username, #oauth_password").serialize(),

        success: data => { urls_as_ajax(); }
    });
});
