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
      formEl.style.setProperty('margin-top', '20px');
    } else {
      formEl.style.setProperty('max-height', '0');
      formEl.style.setProperty('margin-top', '0');
    }
  }



  // Event listeners ---------------------------------------------------------
  window.addEventListener('click', function(e) {
    if (e.target.matches('.js-show-form-s')) {
      showSidebarForm(e, '275px');
    }
  });
}



reviewSauce();
