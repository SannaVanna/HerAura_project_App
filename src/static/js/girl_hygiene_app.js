

document.addEventListener("DOMContentLoaded", () => {
      const typedElement = document.querySelector('.typed');
      if (typedElement) {
        let typed_strings = typedElement.getAttribute('data-typed-items');
        typed_strings = typed_strings.split(',').map(s => s.trim());

        new Typed('.typed', {
          strings: typed_strings,
          typeSpeed: 100,
          backSpeed: 50,
          backDelay: 2000,
          loop: true
        });
      }
});



const themeToggle = document.getElementById('themeToggle');

themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  if (document.body.classList.contains('dark')) {
    themeToggle.textContent = '☀';
    localStorage.setItem('theme', 'dark');
  } else {
    themeToggle.textContent = '🌙';
    localStorage.setItem('theme', 'light');
  }
});

window.onload = () => {
  const theme = localStorage.getItem('theme');
  if (theme === 'dark') {
    document.body.classList.add('dark');
    themeToggle.textContent = '☀';
}
};