// Enhanced form interactions and animations
document.addEventListener("DOMContentLoaded", function () {
  // Détecter si on vient du formulaire bulletin (présence de texte dans textarea)
  const bulletinTextarea = document.getElementById("bulletin_text");
  if (bulletinTextarea && bulletinTextarea.value.trim().length > 0) {
    // Activer l'onglet bulletin
    const bulletinTab = document.querySelector('[data-tab="bulletin"]');
    const manualTab = document.querySelector('[data-tab="manual"]');
    const bulletinContent = document.getElementById("tab-bulletin");
    const manualContent = document.getElementById("tab-manual");

    if (bulletinTab && bulletinContent) {
      bulletinTab.classList.add("active");
      bulletinContent.classList.add("active");
      if (manualTab) manualTab.classList.remove("active");
      if (manualContent) manualContent.classList.remove("active");
    }
  }

  // Tab switching
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const targetTab = this.getAttribute("data-tab");

      // Remove active class from all tabs and contents
      tabBtns.forEach((b) => b.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));

      // Add active class to clicked tab and corresponding content
      this.classList.add("active");
      document.getElementById(`tab-${targetTab}`).classList.add("active");
    });
  });

  // Load example bulletin
  const loadExampleBtn = document.getElementById("load-example");
  if (loadExampleBtn) {
    loadExampleBtn.addEventListener("click", function () {
      const exampleBulletin = `WTIO20 FMMD 010600
BULLETIN MARINE SPECIAL
BMS N°07/04 DE FMMDYMYP A 06 TU
EMIS PAR METEO MADAGASCAR LE 01/01/2020 A 06 TU
1. AVIS D'OURAGAN
2. PHENOMENE: CYCLONE TROPICAL 4 (CALVINIA) 976 HPA
POSITION A 06 TU : DANS UN RAYON DE 10 MN AUTOUR DU POINT 26.9 S / 60.6 E
(VINGT SIX DEGRES NEUF SUD ET SOIXANTE DEGRES SIX EST)
DEPLACEMENT: SUD-SUD-EST 17 KT
3. ZONE MENACEE :
TEMPS A GRAINS DANS UN RAYON DE 100 MN AUTOUR DU CENTRE S'ETENDANT
JUSQU'A 350 MN DANS LE DEMI-CERCLE SUD.
OURAGAN 65 KT ET MER TRES GROSSE A ENORME S'ETENDANT JUSQUE 40 MN
DANS LE DEMI-CERCLE EST.
TEMPETE 50/60 KT ET MER GROSSE A TRES GROSSE DANS UN RAYON DE 55 MN
AUTOUR DU CENTRE, S'ETENDANT JUSQUE 80 MN DANS LE DEMI-CERCLE EST.`;

      document.getElementById("bulletin_text").value = exampleBulletin;
    });
  }

  // Upload fichier bulletin (supports TXT and PDF)
  const fileUpload = document.getElementById("file-upload");
  const fileNameDisplay = document.getElementById("file-name-display");
  const fileNameText = document.getElementById("file-name-text");
  const clearFileBtn = document.getElementById("clear-file");

  if (fileUpload) {
    fileUpload.addEventListener("change", async function (e) {
      const file = e.target.files[0];
      if (!file) return;

      const textarea = document.getElementById("bulletin_text");
      const fileName = file.name;

      // Show loading state
      textarea.value = "Chargement du fichier en cours...";

      try {
        if (fileName.toLowerCase().endsWith(".pdf")) {
          // Parse PDF using PDF.js
          const text = await extractTextFromPDF(file);
          textarea.value = text;
        } else {
          // Read as plain text for .txt files
          const reader = new FileReader();
          reader.onload = function (event) {
            textarea.value = event.target.result;
            // Remove error state if present
            textarea.classList.remove("error");
            textarea.style.borderColor = "";
          };
          reader.onerror = function () {
            textarea.value = "Erreur lors de la lecture du fichier.";
          };
          reader.readAsText(file);
        }
        // Remove error state after successful load
        textarea.classList.remove("error");
        textarea.style.borderColor = "";

        // Afficher le nom du fichier
        if (fileNameDisplay && fileNameText) {
          fileNameText.textContent = fileName;
          fileNameDisplay.style.display = "block";
        }
      } catch (error) {
        console.error("Error reading file:", error);
        textarea.value =
          "Erreur lors de la lecture du fichier: " + error.message;
      }
    });
  }

  // Bouton pour supprimer le fichier chargé
  if (clearFileBtn) {
    clearFileBtn.addEventListener("click", function () {
      if (fileUpload) {
        fileUpload.value = "";
      }
      if (fileNameDisplay) {
        fileNameDisplay.style.display = "none";
      }
      const textarea = document.getElementById("bulletin_text");
      if (textarea) {
        textarea.value = "";
      }
    });
  }

  // Function to extract text from PDF using PDF.js
  async function extractTextFromPDF(file) {
    // Set up PDF.js worker
    if (typeof pdfjsLib !== "undefined") {
      pdfjsLib.GlobalWorkerOptions.workerSrc =
        "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
    } else {
      throw new Error("PDF.js library not loaded");
    }

    // Read file as ArrayBuffer
    const arrayBuffer = await file.arrayBuffer();

    // Load the PDF document
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;

    let fullText = "";

    // Extract text from each page
    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
      const page = await pdf.getPage(pageNum);
      const textContent = await page.getTextContent();

      // Concatenate all text items
      const pageText = textContent.items
        .map((item) => {
          // Add newline if there's a significant Y position change
          return item.str;
        })
        .join(" ");

      fullText += pageText + "\n\n";
    }

    // Clean up the text
    fullText = fullText
      .replace(/\s+/g, " ") // Normalize whitespace
      .replace(/\n\s*\n/g, "\n\n") // Clean up multiple newlines
      .trim();

    if (!fullText || fullText.length < 10) {
      throw new Error(
        "Impossible d'extraire le texte du PDF. Le fichier peut être scanné ou protégé.",
      );
    }

    return fullText;
  }

  // Smooth scroll to result when available
  const result = document.querySelector(".result-container");
  if (result) {
    setTimeout(() => {
      result.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }, 200);
  }

  // Form validation with visual feedback
  const forms = document.querySelectorAll("form");
  const inputs = document.querySelectorAll(
    "input[required], select[required], textarea[required]",
  );

  if (forms.length > 0) {
    // Real-time validation feedback for all forms
    inputs.forEach((input) => {
      input.addEventListener("blur", function () {
        validateInput(this);
      });

      input.addEventListener("input", function () {
        if (this.classList.contains("error")) {
          validateInput(this);
        }
      });
    });

    // Form submission for all forms
    forms.forEach((form) => {
      form.addEventListener("submit", function (e) {
        const formInputs = form.querySelectorAll(
          "input[required], select[required], textarea[required]",
        );
        let isValid = true;

        formInputs.forEach((input) => {
          if (!validateInput(input)) {
            isValid = false;
          }
        });

        if (!isValid) {
          e.preventDefault();
          showNotification(
            "Veuillez remplir tous les champs correctement",
            "error",
          );
        } else {
          // Loading state
          const submitBtn = form.querySelector("button[type=submit]");
          if (submitBtn) {
            submitBtn.innerHTML =
              '<i class="fas fa-spinner fa-spin"></i> Analyse en cours...';
            submitBtn.disabled = true;
          }
        }
      });
    });
  }

  // Input validation function
  function validateInput(input) {
    const value = input.value.trim();
    const type = input.type;
    const tagName = input.tagName.toLowerCase();
    let isValid = true;

    // Special handling for textareas - more lenient
    if (tagName === "textarea") {
      isValid = value.length > 0;
    } else if (!value) {
      isValid = false;
    } else if (type === "number") {
      const num = parseFloat(value);
      const min = input.min ? parseFloat(input.min) : -Infinity;
      const max = input.max ? parseFloat(input.max) : Infinity;

      if (isNaN(num) || num < min || num > max) {
        isValid = false;
      }
    }

    if (isValid) {
      input.classList.remove("error");
      input.style.borderColor = "";
    } else {
      input.classList.add("error");
      input.style.borderColor = "#FF3B30";
    }

    return isValid;
  }

  // Show notification
  function showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: ${type === "error" ? "#FF3B30" : "#0066FF"};
      color: white;
      padding: 16px 24px;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
      z-index: 1000;
      animation: slideInRight 0.3s ease-out;
      font-size: 14px;
      font-weight: 500;
      max-width: 300px;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.animation = "slideOutRight 0.3s ease-in";
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }

  // Add smooth animations for inputs
  const allInputs = document.querySelectorAll("input, select, textarea");
  allInputs.forEach((input) => {
    input.addEventListener("focus", function () {
      this.style.transform = "scale(1.01)";
      this.style.transition = "transform 0.2s ease";
    });

    input.addEventListener("blur", function () {
      this.style.transform = "scale(1)";
    });
  });
});

// Add CSS animations
const style = document.createElement("style");
style.textContent = `
  @keyframes slideInRight {
    from {
      transform: translateX(400px);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOutRight {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(400px);
      opacity: 0;
    }
  }

  input.error::placeholder,
  textarea.error::placeholder {
    color: #FF3B30 !important;
    opacity: 0.5;
  }
`;
document.head.appendChild(style);
