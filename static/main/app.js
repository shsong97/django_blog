(function () {
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    var toggle = document.querySelector('[data-account-toggle]');
    var menu = document.querySelector('[data-account-menu]');
    if (toggle && menu) {
      toggle.addEventListener('click', function (event) {
        event.stopPropagation();
        var open = menu.hasAttribute('hidden');
        if (open) {
          menu.removeAttribute('hidden');
          toggle.setAttribute('aria-expanded', 'true');
        } else {
          menu.setAttribute('hidden', '');
          toggle.setAttribute('aria-expanded', 'false');
        }
      });
      document.addEventListener('click', function () {
        menu.setAttribute('hidden', '');
        toggle.setAttribute('aria-expanded', 'false');
      });
    }

    document.querySelectorAll('.ig-post').forEach(function (post, index) {
      post.style.animationDelay = (index * 0.05) + 's';
    });

    document.querySelectorAll('.ig-story__ring').forEach(function (ring, index) {
      ring.style.animationDelay = (index * 0.04) + 's';
    });
  });
})();
