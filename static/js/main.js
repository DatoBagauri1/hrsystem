document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll(".glass-alert");
    alerts.forEach((alert) => {
        window.setTimeout(() => {
            const dismissButton = alert.querySelector(".btn-close");
            if (dismissButton) {
                dismissButton.click();
            }
        }, 4500);
    });

    const navbar = document.querySelector(".main-navbar");
    if (navbar) {
        const handleScroll = () => {
            navbar.classList.toggle("scrolled", window.scrollY > 10);
        };
        handleScroll();
        document.addEventListener("scroll", handleScroll, { passive: true });
    }
});
