const menu = document.getElementById("mobile-menu");

const menuToggle = ({ target }) => target.classList.toggle("active");

menu.onclick = menuToggle;
