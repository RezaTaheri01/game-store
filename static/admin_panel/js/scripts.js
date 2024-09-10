/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});


// dark mode
let switchBtn = document.getElementById("modeSwitch");
let moonSun = document.getElementById("moon");

//set details
function darkLight(val) {
    if (val === 0) {
        document.documentElement.setAttribute('data-bs-theme', 'dark')
        moonSun.className = "fa fa-moon fa-xl mt-1 mx-2"
        moonSun.style.color = "white"
        setCookie('dark')
    } else {
        document.documentElement.setAttribute('data-bs-theme', 'light')
        moonSun.className = "fa fa-sun fa-xl mt-1 mx-2"
        moonSun.style.color = "goldenrod"
        setCookie('light')
    }
}

// on Click
function click_dark_light(isCheck) {
    if (isCheck) {
        darkLight(0)
        setCookie('dark')
    } else {
        darkLight(1)
        setCookie('light')
    }
    switchBtn.style.boxShadow = "none";
    console.log(getCookie());
}

// on Load
function dark_light(isCheck = switchBtn.checked) {
    let value = getCookie().toString()
    // console.log(value)
    if (value === "") {
        if (isCheck) {
            darkLight(0)
            setCookie('dark')
        } else {
            darkLight(1)
            setCookie('light')
        }
    } else {
        // debugger;
        if (value.includes("dark")) {
            darkLight(0)
            switchBtn.checked = true
        } else if (value.includes("light")) {
            darkLight(1)
            switchBtn.checked = false
        }
    }
    switchBtn.style.boxShadow = "none";
    console.log(getCookie())
}

// Set/Get Cookie
function getCookie() {
    let add = false
    let new_val = ''
    let value = document.cookie
    let len = [...value].length
    // debugger;
    for (let i = 0; i < len; i++) {
        if (add) {
            new_val += value.charAt(i)
        } else if (value.charAt(i) === " ") {
            add = true
        }
    }
    return new_val
}

function setCookie(value) {
    document.cookie = value + "; expires=Thu, 18 Dec 2024 12:00:00 UTC; path=/; SameSite=lax"
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