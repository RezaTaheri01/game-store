let preload;
let navbar = document.getElementById("main-navbar");
let all = document.getElementById("body-layout");
document.getElementById('moon').hidden = true

// preloader

window.addEventListener('load', () => {
    preload = setInterval(preload_disable, 625)
    document.getElementById('moon').hidden = false
})
preload = setInterval(preload_disable, 5025)

function preload_disable() {
    $('#body-layout').removeClass('d-none')
    $('#preloader').addClass('d-none preloader-end').removeClass('preloader')
    clearInterval(preload);
}

// end preloader

// menu
function rotate_menu_icon(id) {
    if (id.value === "close") {
        id.className = "navbar-toggler border-0 open"
        id.value = "open"
    } else {
        id.className = "navbar-toggler border-0 close"
        id.value = "close"
    }
}

$(document).ready(function () {

    $('.dropdown-submenu a.test').on("click", function (e) {

        $(this).next('ul').toggle();

        e.stopPropagation();

        e.preventDefault();

    });

});

// end menu

// price range & filter
const rangeInput = document.querySelectorAll(".range-input input"),
    priceInput = document.querySelectorAll(".price-input input"),
    range = document.querySelector(".slider .progress");
let priceGap = 500000;
priceInput.forEach(input => {
    input.addEventListener("input", e => {
        let minPrice = parseInt(priceInput[0].value),
            maxPrice = parseInt(priceInput[1].value);

        if ((maxPrice - minPrice >= priceGap) && maxPrice <= rangeInput[1].max) {
            if (e.target.className === "input-min") {
                rangeInput[0].value = minPrice;
                range.style.left = ((minPrice / rangeInput[0].max) * 100) + "%";
            } else {
                rangeInput[1].value = maxPrice;
                range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
            }
        }
    });
});
rangeInput.forEach(input => {
    input.addEventListener("input", e => {
        let minVal = parseInt(rangeInput[0].value),
            maxVal = parseInt(rangeInput[1].value);
        if ((maxVal - minVal) < priceGap) {
            if (e.target.className === "range-min") {
                rangeInput[0].value = maxVal - priceGap
            } else {
                rangeInput[1].value = minVal + priceGap;
            }
        } else {
            priceInput[0].value = minVal;
            document.getElementById("min-value").innerHTML = minVal.toLocaleString('en-US');
            priceInput[1].value = maxVal;
            document.getElementById("max-value").innerHTML = maxVal.toLocaleString('en-US');
            range.style.left = ((minVal / rangeInput[0].max) * 100) + "%";
            range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }
    });
});
rangeInput.forEach(input => {
    let minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);
    if ((maxVal - minVal) < priceGap) {
        if (e.target.className === "range-min") {
            rangeInput[0].value = maxVal - priceGap
        } else {
            rangeInput[1].value = minVal + priceGap;
        }
    } else {
        priceInput[0].value = minVal;
        priceInput[1].value = maxVal;
        range.style.left = ((minVal / rangeInput[0].max) * 100) + "%";
        range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
    }
});

// function showNumber(input) {
//     debugger;
//     alert('change')
//     let parent = $(input).parent()
//     let p = parent.find('.number-p')
//     p.val(input.val())
// }

function fillPage(page) {
    $("#page").val(page)
    $("#filter-form").submit()
}

function SubmitFilterForm() {
    $("#page").val(1)
    $("#filter-form").submit()
}

function active(aTag) {
    let value = ''
    if (aTag.classList.contains("text-info-emphasis")) {
        $(aTag).removeClass("text-info-emphasis")
    } else {
        let parent = $(aTag).parent()
        let all_a = parent.find(".filter")
        for (let i = 0; i < all_a.length; i++) {
            $(all_a[i]).removeClass('text-info-emphasis')
        }
        $(aTag).addClass("text-info-emphasis")
        value = aTag.innerHTML.toString()
    }
    // let res = value.toLowerCase()
    $("#order-by").val(value)
}

function currentValue() {
    let parent_order = $("#order-field")
    let target = parent_order.find(".text-info-emphasis").text()
    $("#order-by").val(target)
}

currentValue()
// end price range & filter

//cart update and delete product
let newDelay;

function waitForUpdateCart(input, productId, productInventory) {
    clearTimeout(newDelay)
    newDelay = setTimeout(() => {
        updateCart(input, productId, productInventory)
    }, 1000)
}

function updateCart(input, productId, productInventory) {
    let new_count = input.value
    if (new_count > productInventory) {
        new_count = productInventory
        $(input).val(productInventory)
    } else if (new_count < 1) {
        new_count = 1
        $(input).val(productInventory)
    }
    let url = window.location.href
    // todo : when input change appear submit button to submit change
    $.get('/user/cart-update/?product_id=' + productId + "&" + 'product_count=' + new_count + "&" + 'url=' + url).then(res => {
        $("#cart-section").html(res.body)
        clearTimeout(newDelay)
    })
}

function deleteFromCart(cartDetailId) {
    let title = 'Are you sure?'
    let btn = 'Yes, delete it'
    let btn_2 = 'Okay'
    let btn_cancel = 'No'
    let confirm = 'Deleted!'
    if (document.dir === "rtl") {
        title = "مطمئن هستید؟"
        btn = "بله"
        btn_2 = "باشه"
        btn_cancel = 'نه'
        confirm = "محصول حذف گردید!"
    }

    Swal.fire({
        title: title,
        icon: 'warning',
        background: "#2a2b33",
        color: '#fff',
        showCancelButton: true,
        focusCancel: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: btn,
        cancelButtonText: btn_cancel,
    }).then((result) => {
        if (result.isConfirmed) {
            let url = window.location.href
            $.get('/user/remove-from-cart/?detail_id=' + cartDetailId + "&" + "url=" + url).then(res => {
                // console.log(res.body)
                $("#cart-section").html(res.body)
                Swal.fire({
                    title: confirm,
                    icon: 'success',
                    background: '#2a2b33',
                    confirmButtonText: btn_2,
                    color: '#fff',
                    timer: 2000,
                })
            })
        }
    })
}

function reload() {
    window.location.reload()
}

//end cart update and delete product

// search bar
$("#search-navbar .dropdown").fadeOut()
let newSearchDelay;

function waitForSearchInput() {
    clearTimeout(newSearchDelay)
    newSearchDelay = setTimeout(searchBarDynamicResult, 1000)
}

function searchBarDynamicResult() {
    let search = $("#search-input").val() //ok
    $.get('/products/search-products/?search=' + search + "&" + 'dynamic=' + 1).then(res => {
        $("#search-dynamic-result").html(res.body)
        const currentUrl = window.location.href
        let en = $("#link-en")
        let fa = $("#link-fa")
        if (currentUrl.includes('/fa/')) {
            en.addClass('d-none')
            fa.removeClass('d-none')
        } else {
            fa.addClass('d-none')
            en.removeClass('d-none')
        }
        clearTimeout(newSearchDelay)
    })
}

function apperRes(inp) {
    let parent = $(inp).parent().parent()
    let res_field = parent.find(".dropdown")
    $(res_field).fadeIn(1000)
}

function disappearRes(inp) {
    let parent = $(inp).parent().parent()
    let res_field = parent.find(".dropdown")
    $(res_field).fadeOut(1000)
}

// end search bar


//category
let dropdowns = document.querySelectorAll('.dropdown-toggle')
dropdowns.forEach((dd) => {
    dd.addEventListener('click', function (e) {
        let el = this.nextElementSibling
        if (el.style.display === 'block') {
            el.style.display = 'none'
            let uls = document.querySelectorAll('.last-submenu')
            uls.forEach((u) => {
                u.style.display = 'none'
            })
        } else {
            // last submenu
            if (el.className.includes('main-submenu')) {
                let uls = document.querySelectorAll('.last-submenu')
                uls.forEach((u) => {
                    u.style.display = 'none'
                })
                let ulsMain = document.querySelectorAll('.main-submenu')
                ulsMain.forEach((um) => {
                    um.style.display = 'none'
                })
            } else {
                if (el.className.includes('last-submenu')) {
                    let uls = document.querySelectorAll('.last-submenu')
                    uls.forEach((u) => {
                        u.style.display = 'none'
                    })
                }
            }
            el.style.display = 'block'
        }
        // el.style.display = el.style.display === 'block' ? 'none' : 'block'
    })
})

//change language
function changeLanguage(btn) {
    let url = window.location.href
    let new_url = ''
    if (btn.innerHTML.toString().includes('fa')) {
        let count = 0
        for (let i = 0; i < url.length; i++) {
            if (url[i] === '/') {
                count++
            }
            if (url[i] === '/' && count === 3) {
                new_url += url[i] + 'fa/'
            } else {
                new_url += url[i]
            }
        }
    } else {
        if (url.includes('/fa/')) {
            let url_list = url.split('/')
            let len = url_list.length
            for (let i = 0; i < len; i++) {
                if (url_list[i] === 'fa') {
                } else {
                    if (i === len - 1) {
                        if (url_list[i].includes('Fa')) {
                            let tmp = url_list[i].substring(2)
                            new_url += 'En' + tmp
                        }else {
                            new_url += url_list[i]
                        }
                    } else {
                        new_url += url_list[i] + '/'
                    }
                }
            }
        }
    }
    window.location.replace(new_url)
}

// close dropdowns
let category = document.getElementById("category-menu")
let profile = document.getElementById("profile-menu")

function close_category() {
    if (category.style.display === "block") {
        category.style.display = "none"
    }
}

function close_profile() {
    if (profile.style.display === "block") {
        profile.style.display = "none"
    }
}

all.addEventListener('click', function (e) {
    if (document.getElementById('header-fix').contains(e.target)) {
        // Clicked in box
    } else {
        if (profile.style.display === "block") {
            profile.style.display = "none"
        }
        if (category.style.display === "block") {
            category.style.display = "none"
        }
    }
});