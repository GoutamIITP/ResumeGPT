document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("uploadForm");
    const submitBtn = document.getElementById("submitBtn");
    const fileInput = document.getElementById("resume");
    const consentCheckbox = document.querySelector("input[name='consent']");
    const loadingDiv = document.getElementById("loading");

    // Enable/disable submit button based on file and consent
    function updateSubmitButton() {
        const fileSelected = fileInput.files.length > 0;
        const consentGiven = consentCheckbox.checked;
        submitBtn.disabled = !(fileSelected && consentGiven);
    }

    // Validate file type
    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        if (file && !["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"].includes(file.type)) {
            alert("Please upload a PDF or Word (.docx) file.");
            fileInput.value = "";
        }
        updateSubmitButton();
    });

    consentCheckbox.addEventListener("change", updateSubmitButton);

    // Show loading spinner on form submit
    form.addEventListener("submit", () => {
        submitBtn.disabled = true;
        loadingDiv.classList.remove("hidden");
    });
}); 