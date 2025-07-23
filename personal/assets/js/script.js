window.addEventListener('load', function () {
    const loader = document.querySelector('.preloader');
    loader.classList.add('hidepreloader')
});

jQuery(document).ready(function () {
    jQuery('[data-toggle="tooltip"]').tooltip();
});

//   change head word 
const text = ['گروه برنامه نویسی فراکد', 'متشکل از کادری مجرب ', 'توسعه دهنده وب سایت و اپ موبایل'];

let count = 0;
let index = 0;
let currentText = "";
let letter = "";


(function type() {

    if (count === text.length) {
        count = 0;
    }
    currentText = text[count];
    letter = currentText.slice(0, ++index);

    document.querySelector('.head-name-faracode').textContent = letter;
    if (letter.length === currentText.length) {
        count++;
        index = 0;
    }

    setTimeout(type, 200);

})()
// end change head word
// welcome message
const intro = document.querySelector('.intro');
const TextLogo = document.querySelectorAll('.logo');

window.addEventListener('load', function () {

    setTimeout(() => {
        TextLogo.forEach((Logo, inx) => {
            setTimeout(() => {
                Logo.classList.add('active')
            }, (inx + 1) * 400);
        })
    })

    setTimeout(() => {
        TextLogo.forEach((Logo, inx) => {
            setTimeout(() => {
                Logo.classList.remove('active');
                Logo.classList.add('fade');
            }, (inx + 1) * 50);
        })
    }, 2000);

    setTimeout(() => {
        intro.style.top = '-100vh'
    }, 2300)
});
// end welcome message

// totop
const totop = document.querySelector('.totop');
window.addEventListener('scroll', func);
function func() {
    if (window.pageYOffset > 200) {
        totop.classList.add('active');
    } else {
        totop.classList.remove('active')
    }
};
// sticky to top
window.addEventListener('scroll', fun);
function fun() {
    const header = document.querySelector('.nav-head');
    header.classList.toggle('sticky', window.scrollY > 0)
};

// video
const videobtn = document.querySelector('.video-btn');
const video = document.querySelector('.video');
const videobg = document.querySelector('.video-bg');
function stopPlayer() {
    video.style.display = 'none';
    videobtn.style.display = "block";
    videobg.style.visibility = "visible"
};


function playvideo() {
    videobtn.style.display = "none";
    video.style.display = "block";
    videobg.style.visibility = "hidden";
}
// progress bar
const progressBar = document.querySelector('.progress-bar');
function updateProgressBar() {
    progressBar.style.width = `${getScrollPercentage()}%`;
    requestAnimationFrame(updateProgressBar)
};
function getScrollPercentage() {
    return ((window.scrollY) / (document.body.scrollHeight - window.innerHeight) * 100);
}
updateProgressBar();
// end progress bar


// gallery projects
const gallery = document.querySelectorAll('.gallery .gallery-img .img-pro .addition');
const prolink = document.querySelectorAll('.pro-link');
const previewBox = document.querySelector('.preview-box');
const previewImg = previewBox.querySelector('img');
const iconClose = document.querySelector('.iconClose');
const currentImg = document.querySelector('.current-img');
const totalImg = document.querySelector('.total-img');
const shadow = document.querySelector('.shadow');
window.onload = () => {
    for (let i = 0; i < prolink.length; i++) {
        totalImg.textContent = prolink.length;
        let newIndex = i;
        gallery[i].onclick = () => {
            function preview() {
                currentImg.textContent = newIndex + 1;
                let imgUrl = gallery[newIndex].querySelector('img').src;
                previewImg.src = imgUrl;
            }

            const prevBtn = document.querySelector('.prev');
            const nextBtn = document.querySelector('.next');
            if (newIndex == 0) {
                prevBtn.style.display = 'none';
            }
            if (newIndex >= prolink.length - 1) {
                nextBtn.style.display = 'none';
            }

            prevBtn.onclick = () => {
                newIndex--;
                if (newIndex == 0) {
                    preview()
                    prevBtn.style.display = 'none';
                } else {
                    preview();
                    nextBtn.style.display = 'block';
                }
            }

            nextBtn.onclick = () => {
                newIndex++;
                if (newIndex >= prolink.length - 1) {
                    preview()
                    nextBtn.style.display = 'none';
                } else {
                    preview();
                    prevBtn.style.display = 'block';
                }

            }

            preview()

            previewBox.classList.add('show');
            shadow.style.display = 'block';

            iconClose.onclick = () => {
                prevBtn.style.display = 'block';
                nextBtn.style.display = 'block';
                previewBox.classList.remove('show')
                shadow.style.display = 'none';
            }
        }
    }
}

