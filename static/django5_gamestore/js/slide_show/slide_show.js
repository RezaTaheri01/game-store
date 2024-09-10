let stop = false
let slideIndex = 1;
let slideShow = setInterval(() => {
    plusDivs(1)
}, 7500)

showDivs(slideIndex);

function plusDivs(n = 1) {
    showDivs(slideIndex += n);
    clearInterval(slideShow);
    set_interval()
}

function currentDiv(n) {
    showDivs(slideIndex = n);
    clearInterval(slideShow);
    set_interval()
}

function showDivs(n) {
    let i;
    let slide_img = document.getElementsByClassName("mySlides");
    let slide_bg = document.getElementsByClassName("bg_mySlides");
    let slide_detail = document.getElementsByClassName("detail-slideshow");
    let dots = document.getElementsByClassName("main_slide_dot");
    if (n > slide_img.length) {
        slideIndex = 1
    } else if (n < 1) {
        slideIndex = slide_img.length
    }
    for (i = 0; i < slide_img.length; i++) {
        slide_img[i].style.opacity = 0;
        slide_img[i].style.zIndex = 0;
        slide_bg[i].style.opacity = 0;
        slide_detail[i].style.opacity = 0;
        slide_bg[i].className = slide_bg[i].className.replace("bg_mySlides_main", "")
        slide_img[i].className = slide_img[i].className.replace("mySlides_main", "")
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" w3-white", "");
    }

    slide_img[slideIndex - 1].style.opacity = 1;
    slide_img[slideIndex - 1].style.zIndex = 999;
    slide_bg[slideIndex - 1].style.opacity = 1;
    slide_detail[slideIndex - 1].style.opacity = 1;
    slide_bg[slideIndex - 1].className = 'bg_mySlides position-absolute bg_mySlides_main'
    slide_img[slideIndex - 1].className = 'mySlides rounded-5 position-absolute mySlides_main'
    dots[slideIndex - 1].className += " w3-white";
}

$(".mySlides").on('mouseenter', () => {
    stop = true
    clearInterval(slideShow)
}).on('mouseleave', () => {
    stop = false
    set_interval();
})


function set_interval() {
    slideShow = setInterval(() => {
        plusDivs(1)
    }, 7500)
}

let swiper = []
let n_str = ""
for (let n = 0; n < 20; n++) {
    n_str = n.toString()
    swiper[0] = new Swiper(".swiper-" + n_str, {
        slidesPerView: 4,
        spaceBetween: 12,
        centerSlide: 'true',
        // loop: true,
        fade: 'true',
        grabCursor: 'true',
        navigation: {nextEl: ".swiper-button-next-" + n_str, prevEl: ".swiper-button-prev-" + n_str,},
        lazy: {
            enabled : true,
            // loadPrevNext: true, // pre-loads the next image to avoid showing a loading placeholder if possible
            loadPrevNextAmount: 4 //or, if you wish, preload the next 2 images
        },
        // keyboard: {
        //     enabled : true,
        //     // onlyInViewport: true,
        // },
        // autoplay: {
        //     delay: 20000,
        // },
        // pagination: {
        //     el: ".swiper-pagination-" + n_str,
        // },
        breakpoints: {
            0: {slidesPerView: 1, slidesPerGroup: 1,},
            520: {slidesPerView: 2, slidesPerGroup: 2,},
            750: {slidesPerView: 3, slidesPerGroup: 3,},
            950: {slidesPerView: 4, slidesPerGroup: 4,},
        },
    });
}

// control slide show by arrow keys
$.fn.isInViewport = function () {
    let elementTop = $(this).offset().top;
    let elementBottom = elementTop + $(this).outerHeight() / 2;
    let viewportTop = $(window).scrollTop();
    let viewportHalf = viewportTop + $(window).height() / 2;

    return elementBottom > viewportTop && elementTop < viewportHalf;

};

document.onkeydown = function (evt) {
    if ($("#slide-show").isInViewport()) {
        evt = evt || window.event;
        if (evt.keyCode === 39) { // right arrow
            plusDivs()
        } else if (evt.keyCode === 37) { // left arrow
            plusDivs(-1)
        }
        if (stop !== true) {
            clearInterval(slideShow)
            set_interval();
        } else {
            clearInterval(slideShow)
        }
    }
};