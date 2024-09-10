// Get URL and Prefix for URL
let url = window.location.href
let pre_fix = ''

$(window).resize(function () {
    let width = $(window).width() //fine
    if (width < 1920) {
        $('#bg-img').css('width', width + 'px')
    }
});


function toggleContent(button) {
    const parent = $(button).parent();
    const replyForm = parent.find(".reply-form");
    // const replies = parent.find(".replies");
    if (replyForm.is(":visible")) {
        $(".reply-form").hide();
        replyForm.hide();
        // replies.hide();
    } else {
        $(".reply-form").hide();
        replyForm.show();
        // replies.show();
    }
}

function sendProductComment(productId, btn, parentId = null) {
    // check site language
    url = window.location.href
    pre_fix = ''
    if (url.includes('/fa/')){
        pre_fix = '/fa'
    }
    
    let comment = $('#comment-text').val()
    // console.log(comment)
    if (comment === "") {
    } else {
        $(btn).prop("disabled", true);
        jQuery.get(pre_fix + '/products/add-comment', {
            product_comment: comment,
            product_id: productId,
            parent_id: parentId
        }).then(res => {
            // console.log(res)
            $(btn).prop("disabled", false);
            $('#comment-text').val('')
            $("#comment-section").html(res)
            let title;
            if (document.dir === "rtl") {
                title = 'نیازمند تایید توسط ادمین'
            } else {
                title = 'visible after admin confirmation'
            }
            Swal.fire({
                background: '#2a2b33',
                color: '#fff',
                font_weight: 100,
                icon: 'info',
                title: title,
                showConfirmButton: true,
                confirmButtonText: 'Okay',
            })
        })
    }
}

function sendReply(button, parentId, productId) {
    // check site language
    url = window.location.href
    pre_fix = ''
    if (url.includes('/fa/')){
        pre_fix = '/fa'
    }
    
    const parent = $(button).parent();
    const comment = parent.find(".reply").val();
    // console.log(replyForm.val()) //True
    // replyForm.scrollIntoView({behavior: "smooth"})
    // console.log(comment)
    if (comment === "") {
    } else {
        $(button).prop("disabled", true);
        jQuery.get(pre_fix + '/products/add-comment', {
            product_comment: comment,
            product_id: productId,
            parent_id: parentId
        }).then(res => {
            $(button).prop("disabled", false);
            parent.find(".reply").val('');
            $("#comment-section").html(res)
            let title;
            if (document.dir === "rtl") {
                title = 'نیازمند تایید توسط ادمین'
            } else {
                title = 'visible after admin confirmation'
            }
            Swal.fire({
                background: '#2a2b33',
                color: '#fff',
                font_weight: 100,
                icon: 'info',
                title: title,
                showConfirmButton: true,
                confirmButtonText: 'Okay',
            })
        })
    }
}

let swiper = []
let n_str = ""
for (let n = 0; n < 2; n++) {
    n_str = n.toString()
    swiper[0] = new Swiper(".swiper-" + n_str, {
        slidesPerView: 4,
        spaceBetween: 5,
        centerSlide: 'true',
        loop: 'true',
        fade: 'true',
        grabCursor: 'true',
        navigation: {nextEl: ".swiper-button-next-" + n_str, prevEl: ".swiper-button-prev-" + n_str,},
        // pagination: {
        //     el: ".swiper-pagination-" + n_str,
        // },
        breakpoints: {
            0: {slidesPerView: 1, slidesPerGroup: 1,},
            520: {slidesPerView: 2, slidesPerGroup: 2,},
            750: {slidesPerView: 3, slidesPerGroup: 3,},
            950: {slidesPerView: 5, slidesPerGroup: 5,},
        },
    });
}

function addProductToCart(productId) {
    url = window.location.href
    const productCount = $("#product-count").val()
    $.get('/cart/add-to-cart/?product_id=' + productId + "&" + 'product_count=' + productCount).then(res => {
            //sweetAlert
            let title = res.message
            let btn = 'Okay'
            if (document.dir === 'rtl') {
                btn = 'باشه'
                if (res.status === 'not valid') {
                    title = 'تعداد معتبر نیست'
                }
                if (res.status === 'not enough') {
                    title = 'موجودی کافی نیست'
                }
                if (res.status === 'success') {
                    title = 'محصول با موفقیت اضافه شد'
                }
                if (res.status === 'not found') {
                    title = 'محصول پیدا نشد'
                }
                if (res.status === 'not authenticated') {
                    title = 'ابتدا وارد شوید'
                }
            }
            Swal.fire({
                background: '#2a2b33',
                color: '#fff',
                font_weight: 100,
                icon: res.icon,
                title: title,
                showConfirmButton: true,
                confirmButtonText: btn,
            }).then((result) => {
                if (result.isConfirmed && res.status === 'not authenticated') {
                    window.location.href = '/accounts/sign-in';
                }
            })
        })
}

//description
document.getElementById("full-des").style.display = 'none'
document.getElementById("less-btn").style.display = 'none'

function showMore() {
    let short = document.getElementById("short-des");
    let full = document.getElementById("full-des");
    let moreBtn = document.getElementById("more-btn");
    let lessBtn = document.getElementById("less-btn")

    if (full.style.display === "none") {
        full.style.display = "block";
        short.style.display = "none";
        moreBtn.style.display = "none";
        lessBtn.style.display = "inline";

    } else {
        short.style.display = "block";
        full.style.display = "none";
        moreBtn.style.display = "inline";
        lessBtn.style.display = "none";
    }
}

lightbox.option({
    'wrapAround': true, 'alwaysShowNavOnTouchDevices': true, 'fadeDuration': 0, 'fitImagesInViewport': true
})
