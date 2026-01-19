// Animation au scroll pour le résultat
document.addEventListener("DOMContentLoaded", function () {
  const result = document.querySelector(".result");
  if (result) {
    result.style.opacity = "0";
    setTimeout(() => {
      result.style.opacity = "1";
    }, 100);
  }

  // Validation des champs
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", function (e) {
      const inputs = form.querySelectorAll("input[required]");
      let isValid = true;

      inputs.forEach((input) => {
        if (!input.value) {
          isValid = false;
          input.style.borderColor = "#f5576c";
        } else {
          input.style.borderColor = "#e0e0e0";
        }
      });

      if (!isValid) {
        e.preventDefault();
        alert("Veuillez remplir tous les champs requis");
      }
    });
  }

  // Réinitialiser la couleur de bordure au focus
  const inputs = document.querySelectorAll("input");
  inputs.forEach((input) => {
    input.addEventListener("focus", function () {
      this.style.borderColor = "#667eea";
    });
  });
});
