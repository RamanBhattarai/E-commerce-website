document.addEventListener("DOMContentLoaded", () => {
      const addToCartForms = document.querySelectorAll(".add-to-cart-form");
      addToCartForms.forEach(form => {
        form.addEventListener("submit", e => {
          e.preventDefault();
          const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
          const url = form.action;

          fetch(url, {
            method: "POST",
            headers: {
              "X-CSRFToken": csrfToken,
              "X-Requested-With": "XMLHttpRequest"
            },
          })
          .then(response => {
            if (response.ok) {
              console.log("Added to cart successfully!");
            } else {
              console.error("Error adding to cart");
            }
          });
        });
      });

      const wishlistForms = document.querySelectorAll(".add-to-wishlist-form");
      wishlistForms.forEach(form => {
        form.addEventListener("submit", e => {
          e.preventDefault();
          const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
          const url = form.action;

          fetch(url, {
            method: "POST",
            headers: {
              "X-CSRFToken": csrfToken,
              "X-Requested-With": "XMLHttpRequest"
            },
          })
          .then(response => {
            if (response.ok) {
              console.log("Added to wishlist successfully!");
            } else {
              console.error("Error adding to wishlist");
            }
          });
        });
      });
    });