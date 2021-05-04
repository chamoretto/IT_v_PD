function getCookie(name, _default) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : _default;
}

function setCookie(name, value, options) {
    if (!options) {
        options={path: '/'}
    }
    if (name && value) {
        var updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
        for (var optionKey in options) {
            updatedCookie += "; " + optionKey;
            var optionValue = options[optionKey];
            if (optionValue !== true) {
                updatedCookie += "=" + optionValue;
            }
        }
        document.cookie = updatedCookie;
    }
}