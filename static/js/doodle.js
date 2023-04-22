document.addEventListener("DOMContentLoaded", function () {
    const doodle = document.querySelector("css-doodle");
    const nav = document.querySelector("nav");
    const navItems = document.querySelectorAll(".nav-item");
    const body = document.querySelector("body");
  
    const updateDoodle = () => {
      doodle.update(`
        @grid: 20 / 100vmax / #0a0c27;
        @content: @unicode.r(0x2500, 0x257f);
        color: hsla(@r360, 70%, 70%, @r.9);
        font-size: 8vmin;
        font-family: sans-serif;
      `);
    };

    // Ajouter l'événement 'click' sur le body
    body.addEventListener("click", updateDoodle);
  
    // Désactiver le clic sur les éléments de la navbar
    navItems.forEach(item => {
        item.addEventListener("click", (event) => {
            event.stopPropagation();
        });
    });

    // Désactiver le clic sur le nav
    nav.addEventListener("click", (event) => {
        event.stopPropagation();
    });

    // Désactiver le clic sur le formulaire
    const form = document.querySelector("form");
    if (form) {
      form.addEventListener("click", (event) => {
          event.stopPropagation();
      });
    }
  
    // Charger le doodle lors de l'initialisation
    updateDoodle();
});
