document.addEventListener("DOMContentLoaded", () => {

    const list = document.getElementById("methods-list");
    const emptyState = document.getElementById("empty-state");

    function updateState() {
        const count = list.querySelectorAll(".method-item").length;
        emptyState.style.display = count === 0 ? "block" : "none";
    }

    list.addEventListener("click", (e) => {

        if (e.target.classList.contains("set-default")) {
            const all = list.querySelectorAll(".method-item");
            all.forEach(item => item.classList.remove("active"));
            e.target.closest(".method-item").classList.add("active");
        }

        if (e.target.classList.contains("remove-method")) {
            if (!confirm("Remover este método?")) return;
            e.target.closest(".method-item").remove();
            updateState();
        }
    });

    updateState();
});
