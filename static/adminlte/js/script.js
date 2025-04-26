let navbar = document.querySelector('.header .navbar');

document.querySelector('#menu-btn').onclick = () => {
    navbar.classList.add('active');
}

document.querySelector('#nav-close').onclick = () => {
    navbar.classList.remove('active');
}

window.onscroll = () => {
    navbar.classList.remove('active');
};

var swiper = new Swiper(".home-slider", {
    loop: true,
    grabCursor:true,
    autoplay:{
        delay:2500,
        disableOnIteraction: false,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });

  var swiper = new Swiper(".gallery-slider", {
    slidesPerView: 3,
    spaceBetween: 10,
    loop:true,
    centeredSlides:true,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    autoplay:{
        delay:2500,
        disableOnIteraction: false,
    },
    breakpoints:{
        0:{
            slidesPerView:1,
        },
        450:{
            slidesPerView:2,
        },
        768:{
            slidesPerView:3,
        },
        1024:{
            slidesPerView:4,
        },
    }
  });

  var swiper = new Swiper(".review-slider", {
    effect: "coverflow",
    grabCursor: true,
    centeredSlides: true,
    slidesPerView: "auto",
    // loop:true,
    autoplay:{
        delay:2500,
        disableOnIteraction: false,
    },
    coverflowEffect: {
      rotate: 50,
      stretch: 0,
      depth: 100,
      modifier: 1,
      slideShadows: true,
    },
    pagination: {
      el: ".swiper-pagination",
    },
  });

  lightGallery(document.querySelector('.gallery-main'));
