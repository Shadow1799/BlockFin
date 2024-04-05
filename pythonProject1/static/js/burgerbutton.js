document.addEventListener('DOMContentLoaded', function() {
  var toggle = document.getElementById('navbar-toggle');
  var menu = document.querySelector('.navbar-menu');

  toggle.addEventListener('change', function() {
    if (this.checked) {
      menu.classList.add('active');
    } else {
      menu.classList.remove('active');
    }
  });
});
