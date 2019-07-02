function reviewSauce() {

  /**
   * Summary
   *
   * Description
   */
  function showSidebarForm(e, height) {
    const formEl = e.target.nextElementSibling;
    if (!formEl.style.maxHeight || formEl.style.maxHeight == '0px') {
      formEl.style.setProperty('max-height', height);
      formEl.style.setProperty('margin-top', '10px');
      formEl.style.setProperty('margin-bottom', '10px');
    } else {
      formEl.style.setProperty('max-height', '0');
      formEl.style.setProperty('margin-top', '0');
      formEl.style.setProperty('margin-bottom', '0');
    }
  }

  /**
   * Summary
   *
   * Description
   */
  function setupSelectMenu(el) {
    const firstOption = el.firstElementChild;
    firstOption.disabled = true;
    firstOption.selected = true;
  }


  // Event listeners ---------------------------------------------------------
  window.addEventListener('load', function() {
    if (document.querySelectorAll('.js-select-menu')) {
      const menuEls = document.querySelectorAll('.js-select-menu');
      for (let i = 0; i < menuEls.length; i++) {
        setupSelectMenu(menuEls[i]);
      }
    }
  });


  window.addEventListener('click', function(e) {
    if (e.target.matches('.js-show-form')) {
      showSidebarForm(e, '310px');
    }
  });
}



reviewSauce();
