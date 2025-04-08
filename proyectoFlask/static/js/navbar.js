window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    navbar.classList.toggle('bg-white', window.scrollY > 10);
    navbar.classList.toggle('shadow-sm', window.scrollY > 10);
});