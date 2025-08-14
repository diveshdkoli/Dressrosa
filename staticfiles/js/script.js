// === Search Bar ===
const searchBtn = document.getElementById("searchBtn");
const searchForm = document.getElementById("searchForm");

if (searchBtn && searchForm) {
  searchBtn.addEventListener("click", () => {
    if (!searchForm.classList.contains("active")) {
      searchForm.classList.add("active");
    } else {
      searchForm.submit(); // optional submit on second click
    }
  });

  document.addEventListener("click", (e) => {
    if (!searchForm.contains(e.target)) {
      searchForm.classList.remove("active");
    }
  });
}

// === Scrolling Carousel (imageTrack) ===
const imageTrack = document.getElementById("imageTrack");

if (imageTrack) {
  const images = imageTrack.querySelectorAll("img");
  let currentIndex = 0;

  function updateCarousel() {
    if (images.length === 0) return;

    const imageWidth = images[0].offsetWidth + 20; // assuming 20px gap
    const wrapper = document.querySelector(".carousel-wrapper");
    if (!wrapper) return;

    const wrapperWidth = wrapper.offsetWidth;
    const centerOffset = (wrapperWidth / 2) - (imageWidth / 2);
    const translateX = -(currentIndex * imageWidth) + centerOffset;

    imageTrack.style.transform = `translateX(${translateX}px)`;

    images.forEach((img, i) => {
      img.classList.toggle("active", i === currentIndex);
    });
  }

  function moveLeft() {
    currentIndex = currentIndex > 0 ? currentIndex - 1 : images.length - 1;
    updateCarousel();
  }

  function moveRight() {
    currentIndex = currentIndex < images.length - 1 ? currentIndex + 1 : 0;
    updateCarousel();
  }

  window.addEventListener("load", updateCarousel);
  window.addEventListener("resize", updateCarousel);
  setInterval(moveRight, 5000);
}

// === Swiper.js Initialization (if loaded) ===
if (typeof Swiper !== "undefined") {
  new Swiper('.products__swiper', {
    loop: true,
    spaceBetween: 20,
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      0: { slidesPerView: 1 },
      576: { slidesPerView: 2 },
      768: { slidesPerView: 3 },
      992: { slidesPerView: 4 },
    },
  });
}

// === Scroll Active Link Highlight ===
const sections = document.querySelectorAll("section[id]");

function scrollActive() {
  const scrollY = window.pageYOffset;

  sections.forEach((section) => {
    const sectionHeight = section.offsetHeight;
    const sectionTop = section.offsetTop - 58;
    const sectionId = section.getAttribute("id");
    const navLink = document.querySelector(`.nav__menu a[href*=${sectionId}]`);

    if (navLink) {
      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        navLink.classList.add("active-link");
      } else {
        navLink.classList.remove("active-link");
      }
    }
  });
}

window.addEventListener("scroll", scrollActive);

// === Product Carousel 1 (infinite loop) ===
const track = document.querySelector('.carousel-track');
const originalCards = Array.from(document.querySelectorAll('.product-card'));
const prev = document.getElementById('prev');
const next = document.getElementById('next');

if (track && originalCards.length > 0 && prev && next) {
  let index = 0;
  let slideWidth;
  const cloneCount = Math.min(3, originalCards.length);

  // Clone cards for infinite effect
  for (let i = 0; i < cloneCount; i++) {
    const firstClone = originalCards[i].cloneNode(true);
    const lastClone = originalCards[originalCards.length - 1 - i].cloneNode(true);
    track.appendChild(firstClone);
    track.insertBefore(lastClone, track.firstChild);
  }

  const allCards = document.querySelectorAll('.product-card');
  index = cloneCount;

  function updateSlideWidth() {
    slideWidth = allCards[0].offsetWidth;
    track.style.transition = 'none';
    track.style.transform = `translateX(${-slideWidth * index}px)`;
  }

  updateSlideWidth();

  function moveToSlide() {
    track.style.transition = 'transform 0.5s ease-in-out';
    track.style.transform = `translateX(${-slideWidth * index}px)`;
  }

  next.addEventListener('click', () => {
    if (index >= allCards.length - cloneCount) return;
    index++;
    moveToSlide();
  });

  prev.addEventListener('click', () => {
    if (index <= 0) return;
    index--;
    moveToSlide();
  });

  track.addEventListener('transitionend', () => {
    if (index === allCards.length - cloneCount) {
      track.style.transition = 'none';
      index = cloneCount;
      track.style.transform = `translateX(${-slideWidth * index}px)`;
    } else if (index === 0) {
      track.style.transition = 'none';
      index = allCards.length - 2 * cloneCount;
      track.style.transform = `translateX(${-slideWidth * index}px)`;
    }
  });

  window.addEventListener('resize', updateSlideWidth);
}

// === Product Carousel 2 (alternative infinite carousel) ===
const carouselTrack2 = document.getElementById('carouselTrack');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
let autoScroll;
let itemsPerSlide = 4;

function updateItemsPerSlide() {
  if (window.innerWidth <= 576) {
    itemsPerSlide = 1;
  } else if (window.innerWidth <= 992) {
    itemsPerSlide = 2;
  } else {
    itemsPerSlide = 4;
  }
}
updateItemsPerSlide();
window.addEventListener('resize', updateItemsPerSlide);

function moveNext() {
  if (!carouselTrack2) return;
  carouselTrack2.style.transition = "transform 0.6s ease-in-out";
  carouselTrack2.style.transform = `translateX(-100%)`;

  carouselTrack2.addEventListener('transitionend', () => {
    for (let i = 0; i < itemsPerSlide; i++) {
      if (carouselTrack2.firstElementChild)
        carouselTrack2.appendChild(carouselTrack2.firstElementChild);
    }
    carouselTrack2.style.transition = "none";
    carouselTrack2.style.transform = "translateX(0)";
  }, { once: true });
}

function movePrev() {
  if (!carouselTrack2) return;
  for (let i = 0; i < itemsPerSlide; i++) {
    if (carouselTrack2.lastElementChild)
      carouselTrack2.insertBefore(carouselTrack2.lastElementChild, carouselTrack2.firstElementChild);
  }
  carouselTrack2.style.transition = "none";
  carouselTrack2.style.transform = `translateX(-100%)`;

  requestAnimationFrame(() => {
    carouselTrack2.style.transition = "transform 0.6s ease-in-out";
    carouselTrack2.style.transform = "translateX(0)";
  });
}

function startAutoScroll() {
  autoScroll = setInterval(moveNext, 5000);
}
function stopAutoScroll() {
  clearInterval(autoScroll);
}

if (nextBtn && prevBtn) {
  nextBtn.addEventListener('click', () => {
    stopAutoScroll();
    moveNext();
    startAutoScroll();
  });

  prevBtn.addEventListener('click', () => {
    stopAutoScroll();
    movePrev();
    startAutoScroll();
  });

  startAutoScroll();
}
