const form = document.getElementById("analyzeForm");
const analyzeButton = document.getElementById("analyzeButton");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(form);

  analyzeButton.disabled = true;
  analyzeButton.textContent = "Analyzing...";
  toast("Reading resume and calculating score");

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || "Analysis failed");
    }

    renderAnalysis(data);
    toast("Resume analysis completed");
  } catch (error) {
    toast(error.message);
  } finally {
    analyzeButton.disabled = false;
    analyzeButton.textContent = "Generate Analysis";
  }
});

function renderAnalysis(data) {
  document.getElementById("atsScore").textContent = `${data.atsScore}/100`;
  document.getElementById("grade").textContent = data.grade;
  document.getElementById("sectionScore").textContent = data.sectionScore;
  document.getElementById("skillsScore").textContent = data.skillsScore;
  document.getElementById("keywordScore").textContent = data.keywordScore;
  document.getElementById("actionVerbScore").textContent = data.actionVerbScore;
  document.getElementById("skillCount").textContent = `${data.detectedSkills.length} found`;

  renderChips("skillsList", data.detectedSkills, "No technical skills detected yet.");
  renderChips("matchedKeywords", data.matchedKeywords, "Paste a job description to compare keywords.");
  renderChips("missingKeywords", data.missingKeywords, "No missing keywords found.");

  document.getElementById("suggestions").innerHTML = data.suggestions
    .map((item) => `<li>${escapeHtml(item)}</li>`)
    .join("");

  document.getElementById("aiFeedback").textContent = data.aiFeedback;
}

function renderChips(elementId, values, emptyText) {
  const element = document.getElementById(elementId);
  if (!values.length) {
    element.innerHTML = `<span class="empty">${escapeHtml(emptyText)}</span>`;
    return;
  }
  element.innerHTML = values
    .map((value) => `<span class="chip">${escapeHtml(value)}</span>`)
    .join("");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function toast(message) {
  const toastElement = document.getElementById("toast");
  toastElement.textContent = message;
  toastElement.classList.add("show");
  setTimeout(() => toastElement.classList.remove("show"), 2400);
}
