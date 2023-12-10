document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;
    const inputMsg = document.getElementById("input-msg");

    themeToggle.addEventListener("click", function () {
        // Check if 'dark-mode' class is present on the body
        const isDarkMode = body.classList.contains("dark-mode");

        // Toggle the 'dark-mode' class on the body
        body.classList.toggle("dark-mode", !isDarkMode);
        body.classList.toggle("light-mode", isDarkMode);

        inputMsg.toggle("dark-mode", !isDarkMode);
        inputMsg.toggle("light-mode", isDarkMode);
    });
});
