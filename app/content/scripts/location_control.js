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
        send_ajax(
            $(event.target).attr("href"),
            "GET",
            url_processing,
            JSON.stringify({}),
            true,
            false
        );
    });
    console.log('Ссылки перезаписаны на ajax')
}
urls_as_ajax()
