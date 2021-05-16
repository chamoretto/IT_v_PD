function urls_as_ajax(){
    /*
    * Превращает ссылки в ajax-запросы.
    *
    * Должен явно вызываться
    * после каждого ajax-запроса,смены контента, или явной перезагрузки страницы
    *
    * */

    $('a[href]').not('a[href^=http]').not('a[href="#"]').click((event) => {
        event.preventDefault();
        let target = $(event.target);
        if (!target.attr("href")){
            target = $($(event.target).parents("a[href]")[0]);
        }
        console.log(target, target.attr("href"));

        const check_data = target.attr("href").split('?');

        if (check_data.length < 2){
               send_ajax(
                    target.attr("href"),
                    "GET",
                    url_processing,
                    JSON.stringify({}),
                    true,
                    false
                );
        } else {
            let data = {};
            check_data[1].split('&').map( i => i.split('=')).map( i => {data[i[0]] = i[1]})
            send_ajax(
                check_data[0],
                "POST",
                url_processing,
                JSON.stringify(data),
                true,
                false
            );
        }

    });
    console.log('Ссылки перезаписаны на ajax')
}

// urls_as_ajax();
