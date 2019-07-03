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

  /**
   * Toggles the visibility of password fields.
   *
   * This function will work with multiple password fields in a single page.
   * The show/hide icon must have the class "js-showhide", have no child
   * elements, and be the next element sibling to the password field.
   */
  function showHidePassword(e) {
    const passwordEl = e.target.previousElementSibling;
    if (passwordEl.type === 'password') {
      passwordEl.type = 'text';
      e.target.classList.remove('fa-eye');
      e.target.classList.add('fa-eye-slash');
    }
    else {
      passwordEl.type = 'password';
      e.target.classList.remove('fa-eye-slash');
      e.target.classList.add('fa-eye');
    }
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
      showSidebarForm(e, '350px');
    }
    if (e.target.matches('.js-showhide-password')) {
      showHidePassword(e);
    }
  });
}



reviewSauce();
