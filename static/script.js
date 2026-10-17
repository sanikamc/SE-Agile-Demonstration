
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const statusFilter = document.getElementById("statusFilter");
    const taskCards = document.querySelectorAll(".task-card");
    const noResults = document.getElementById("noResults");
    const todayDate = document.getElementById("todayDate");

    // Display today's date
    if (todayDate) {
        todayDate.textContent = new Date().toLocaleDateString("en-IN", {
            day: "numeric",
            month: "short",
            year: "numeric"
        });
    }

    // Search and filter tasks
    function filterTasks() {
        const searchText = searchInput.value.trim().toLowerCase();
        const selectedStatus = statusFilter.value;
        let visibleCount = 0;

        taskCards.forEach((card) => {
            const title = card.dataset.title || "";
            const subject = card.dataset.subject || "";
            const status = card.dataset.status || "";

            const matchesSearch =
                title.includes(searchText) ||
                subject.includes(searchText);

            const matchesStatus =
                selectedStatus === "all" ||
                status === selectedStatus;

            const visible = matchesSearch && matchesStatus;
            card.hidden = !visible;

            if (visible) {
                visibleCount++;
            }
        });

        if (noResults) {
            noResults.hidden = visibleCount > 0;
        }
    }

    searchInput.addEventListener("input", filterTasks);
    statusFilter.addEventListener("change", filterTasks);

    // Prevent accidental double submission of task forms
    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", () => {
            const submitButton = form.querySelector(
                'button[type="submit"]'
            );

            if (submitButton && !form.classList.contains("delete-form")) {
                submitButton.disabled = true;
                submitButton.style.opacity = "0.7";
            }
        });
    });
});
