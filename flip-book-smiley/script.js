document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('.flip-book img');
    if (images.length === 0) return; // Only run if there are images to flip

    let currentIndex = 0;

    function changeImage() {
        images[currentIndex].classList.remove('active');
        currentIndex = (currentIndex + 1) % images.length;
        images[currentIndex].classList.add('active');
    }

    setInterval(changeImage, 1000); // Change image every 1 second
});
