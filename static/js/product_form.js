const addButton = document.getElementById('add-description');
  const container = document.getElementById('descriptions-container');
  const totalForms = document.querySelector('#id_descriptions-TOTAL_FORMS');

  function attachRemoveHandler(button) {
    button.addEventListener('click', () => {
      const formToRemove = button.closest('.description-form');
      formToRemove.remove();
      const forms = container.querySelectorAll('.description-form');
      totalForms.value = forms.length;
      forms.forEach((form, index) => {
        form.querySelectorAll('input, select, textarea, label').forEach(el => {
          if (el.name) el.name = el.name.replace(/-\d+-/, `-${index}-`);
          if (el.id) el.id = el.id.replace(/-\d+-/, `-${index}-`);
          if (el.htmlFor) el.htmlFor = el.htmlFor.replace(/-\d+-/, `-${index}-`);
        });
      });
    });
  }

  document.querySelectorAll('.remove-description').forEach(btn => {
    attachRemoveHandler(btn);
  });

  addButton.addEventListener('click', () => {
    const formIdx = parseInt(totalForms.value);
    let emptyForm = container.querySelector('.description-form');
    if (emptyForm) {
      emptyForm = emptyForm.cloneNode(true);
    } else {
      alert('No initial form template available.');
      return;
    }

    emptyForm.querySelectorAll('input, select, textarea').forEach(input => {
      if (input.type === 'checkbox' || input.type === 'radio') {
        input.checked = false;
      } else {
        input.value = '';
      }
    });

    const deleteLabel = emptyForm.querySelector('label');
    if (deleteLabel) deleteLabel.remove();

    emptyForm.querySelectorAll('input, select, textarea, label').forEach(el => {
      if (el.name) el.name = el.name.replace(/-\d+-/, `-${formIdx}-`);
      if (el.id) el.id = el.id.replace(/-\d+-/, `-${formIdx}-`);
      if (el.htmlFor) el.htmlFor = el.htmlFor.replace(/-\d+-/, `-${formIdx}-`);
    });

    container.appendChild(emptyForm);
    totalForms.value = formIdx + 1;

    const removeBtn = emptyForm.querySelector('.remove-description');
    if (removeBtn) attachRemoveHandler(removeBtn);
  });

  // Image preview functionality
  document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById('id_image');
    const preview = document.getElementById('imagePreview');

    if (imageInput) {
      imageInput.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
          }
          reader.readAsDataURL(file);
        } else {
          preview.src = '#';
          preview.style.display = 'none';
        }
      });
    }
  });