var dataThemeDark = "dark";
var dataThemeDefault = "default";

var onDarkMode = '<i class="fas fa-moon"></i>';
var offDarkMode = '<i class="far fa-moon"></i>';

var stateDarkMode = eval(localStorage.getItem("darkMode") || "false");
console.log(stateDarkMode);
var b = document.body;
var switchersLinkDarkMode = document.getElementsByClassName("dark-mode-switchers");

b.setAttribute("data-theme", stateDarkMode ? dataThemeDark : dataThemeDefault);


function switchDarkMode(state) {
    if (!(typeof state in ["boolean", "number"])) state = stateDarkMode;
    stateDarkMode = !state;
    localStorage.setItem("darkMode", stateDarkMode.toString());

    if (stateDarkMode) {
        b.setAttribute("data-theme", dataThemeDark);
        var ih = offDarkMode;
    }
    else {
        b.setAttribute("data-theme", dataThemeDefault);
        var ih = onDarkMode;
    }

    if (switchersLinkDarkMode.length) {
        for (var i = 0; i < switchersLinkDarkMode.length; i++) {
            switchersLinkDarkMode[i].innerHTML = ih;
        }
    }
}

function initButtons() {
    for (var i = 0; i < switchersLinkDarkMode.length; i++) {
        var a = switchersLinkDarkMode[i];
        a.innerHTML = stateDarkMode ? onDarkMode : offDarkMode;
        a.addEventListener("click", switchDarkMode)
    }
}
