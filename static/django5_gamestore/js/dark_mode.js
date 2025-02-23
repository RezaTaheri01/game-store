// dark mode
let switchBtn = document.getElementById("modeSwitch");
let moonSun = document.getElementById("moon");

//set details
function darkLight(val) {
    if (val === 0) {
        document.documentElement.setAttribute('data-bs-theme', 'dark')
        moonSun.className = "fa fa-moon fa-lg mt-1 mx-2"
        moonSun.style.color = "white"
        setCookie('dark')
    } else {
        document.documentElement.setAttribute('data-bs-theme', 'light')
        moonSun.className = "fa fa-sun fa-lg mt-1 mx-2"
        moonSun.style.color = "goldenrod"
        setCookie('light')
    }
}

// on Click
function click_dark_light(isCheck) {
    if (isCheck) {
        darkLight(1)
        setCookie('light')
    } else {
        darkLight(0)
        setCookie('dark')
    }
    switchBtn.style.boxShadow = "none";
    // console.log(getCookie());
}

// on Load
function dark_light(isCheck = switchBtn.checked) {
    let value = document.cookie
    if (value.includes("dark")) {
        darkLight(0)
        switchBtn.checked = false
    } else if (value.includes("light")) {
        darkLight(1)
        switchBtn.checked = true
    } else {
        if (isCheck) {
            darkLight(1)
            setCookie('light')
        } else {
            darkLight(0)
            setCookie('dark')
        }
    }
    switchBtn.style.boxShadow = "none";
}

// Set/Get Cookie
function getCookie() {
    let value = document.cookie
    return value
}

function setCookie(value) {
    document.cookie = value + "; expires=Thu, 18 Dec 2030 12:00:00 UTC; path=/; SameSite=lax"
}

function DelCookie(value) {
    document.cookie = value + "; expires=Thu, 18 Dec 2001 12:00:00 UTC; path=/ ; SameSite=lax"
    document.cookie = value + "; expires=Thu, 18 Dec 2001 12:00:00 UTC; path=/"
}

//Delete Cookie
// DelCookie("dark")
// DelCookie("light")
// console.log(getCookie());
// function saveStaticDataToFile() {
//     let blob = new Blob(["Welcome to Websparrow.org."],
//         {type: "text/plain;charset=utf-8"});
//     saveAs(blob, "static.txt");
// }
//
// saveStaticDataToFile()

// end dark mode

dark_light()