function send_ajax(url,
                   method = "GET",
                   callback_f = () => {
                   },
                   data = JSON.stringify({}),
                   x_part=false,
                   is_form = false) {
    setTimeout(() => {
        const xhr = new XMLHttpRequest();
        xhr.open(method, url, true);
        let headers = {
            // "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru,en;q=0.9,la;q=0.8",
            "Cache-Control": "no-cache",
            // "Connection": "keep-alive",
            "Pragma": "no-cache",
            // "Sec-Fetch-Dest": "empty",
            // "Sec-Fetch-Mode": "cors",
            // "Sec-Fetch-Site": "same-origin",
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
        const token = localStorage.getItem('token')
        if (token) {
            headers['Authorization'] = 'Bearer ' + token;
        }
        if (is_form) {
            headers['Content-Type'] = "application/x-www-form-urlencoded";
        }
        if (x_part){
            headers['X-Part'] = "basic-content";
        }
        [...Object.keys(headers)].map( i => {
            xhr.setRequestHeader(i, headers[i])
        });

        if (method === "GET") {
            xhr.send();
        } else {
            xhr.send(data);
        }
        xhr.onreadystatechange = callback_f;

    });

}