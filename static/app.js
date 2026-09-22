const form = document.getElementById("analyzeForm");

const analyzeButton =
    document.getElementById("analyzeButton");

const resumeInput =
    document.getElementById("resume");

const selectedFile =
    document.getElementById("selectedFile");

const results =
    document.getElementById("results");


// =====================================================
// SHOW SELECTED FILE
// =====================================================

resumeInput.addEventListener("change", function () {

    if (resumeInput.files.length > 0) {

        selectedFile.textContent =
            "Selected file: " +
            resumeInput.files[0].name;

    } else {

        selectedFile.textContent = "";

    }

});


// =====================================================
// FORM SUBMIT
// =====================================================

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const formData =
        new FormData(form);

    analyzeButton.disabled = true;

    analyzeButton.textContent =
        "Analyzing with Gemini AI...";

    toast(
        "Uploading resume and analyzing with Gemini AI..."
    );


    try {

        const response = await fetch(
            "/api/analyze",
            {
                method: "POST",
                body: formData
            }
        );


        // ---------------------------------------------
        // READ RESPONSE
        // ---------------------------------------------

        const data =
            await response.json();


        // ---------------------------------------------
        // DEBUG
        // ---------------------------------------------

        console.log(
            "Gemini API response:",
            data
        );


        // ---------------------------------------------
        // HANDLE BACKEND ERROR
        // ---------------------------------------------

        if (!response.ok) {

            throw new Error(
                data.message ||
                data.error ||
                "Gemini analysis failed."
            );

        }


        // ---------------------------------------------
        // CHECK RESPONSE
        // ---------------------------------------------

        if (!data) {

            throw new Error(
                "Empty response received from backend."
            );

        }


        // ---------------------------------------------
        // DISPLAY RESULTS
        // ---------------------------------------------

        renderAnalysis(data);


        toast(
            "Gemini AI analysis completed successfully."
        );


        // Scroll to results

        results.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


    } catch (error) {

        console.error(
            "Analysis error:",
            error
        );


        toast(
            error.message ||
            "Something went wrong."
        );


        // Show error on screen too

        const feedback =
            document.getElementById(
                "aiFeedback"
            );


        if (feedback) {

            feedback.innerHTML = `
                <div class="feedback-block error-feedback">
                    <h3>Gemini Analysis Error</h3>

                    <p>
                        ${escapeHtml(
                            error.message ||
                            "Unable to generate AI feedback."
                        )}
                    </p>
                </div>
            `;

        }


    } finally {

        analyzeButton.disabled = false;

        analyzeButton.textContent =
            "Generate AI Analysis";

    }

});


// =====================================================
// RENDER COMPLETE ANALYSIS
// =====================================================

function renderAnalysis(data) {

    console.log(
        "Rendering Gemini data:",
        data
    );


    // =================================================
    // ATS SCORE
    // =================================================

    const atsScore =
        document.getElementById(
            "atsScore"
        );


    if (atsScore) {

        atsScore.textContent =
            data.ats_score ?? 0;

    }


    // =================================================
    // OVERALL SCORE
    // =================================================

    const overallScore =
        document.getElementById(
            "overallScore"
        );


    if (overallScore) {

        overallScore.textContent =
            data.overall_score ?? 0;

    }


    // =================================================
    // JOB MATCH SCORE
    // =================================================

    const jobMatchScore =
        document.getElementById(
            "jobMatchScore"
        );


    if (jobMatchScore) {

        jobMatchScore.textContent =
            data.job_match_score ?? 0;

    }


    // =================================================
    // MATCHED SKILLS
    // =================================================

    const matchedSkills =
        Array.isArray(data.matched_skills)
            ? data.matched_skills
            : [];


    const matchedCount =
        document.getElementById(
            "matchedCount"
        );


    if (matchedCount) {

        matchedCount.textContent =
            matchedSkills.length;

    }


    renderChips(
        "skillsList",
        matchedSkills,
        "No matched skills found."
    );


    // =================================================
    // MISSING SKILLS
    // =================================================

    const missingSkills =
        Array.isArray(data.missing_skills)
            ? data.missing_skills
            : [];


    const missingCount =
        document.getElementById(
            "missingCount"
        );


    if (missingCount) {

        missingCount.textContent =
            missingSkills.length;

    }


    renderMissingSkills(
        missingSkills
    );


    // =================================================
    // RECOMMENDED SKILLS
    // =================================================

    const recommendedSkills =
        Array.isArray(
            data.recommended_skills
        )
            ? data.recommended_skills
            : [];


    renderRecommendedSkills(
        recommendedSkills
    );


    // =================================================
    // AI IMPROVEMENT SUGGESTIONS
    // =================================================

    const suggestions =
        Array.isArray(
            data.improvement_suggestions
        )
            ? data.improvement_suggestions
            : [];


    renderList(
        "suggestions",
        suggestions,
        "No AI improvement suggestions were generated."
    );


    // =================================================
    // FINAL GEMINI AI FEEDBACK
    // =================================================

    renderFinalFeedback(
        data.final_feedback
    );

}


// =====================================================
// MATCHED SKILLS
// =====================================================

function renderChips(
    elementId,
    items,
    emptyMessage
) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element) {

        console.error(
            "Element not found:",
            elementId
        );

        return;

    }


    if (
        !Array.isArray(items) ||
        items.length === 0
    ) {

        element.innerHTML = `
            <p class="empty">
                ${escapeHtml(emptyMessage)}
            </p>
        `;

        return;

    }


    element.innerHTML =
        items
            .map(function (item) {

                return `
                    <span class="skill-chip">
                        ${escapeHtml(item)}
                    </span>
                `;

            })
            .join("");

}


// =====================================================
// MISSING SKILLS
// =====================================================

function renderMissingSkills(
    skills
) {

    const element =
        document.getElementById(
            "missingSkills"
        );


    if (!element) {

        return;

    }


    if (
        !Array.isArray(skills) ||
        skills.length === 0
    ) {

        element.innerHTML = `
            <p class="empty">
                No important missing skills identified.
            </p>
        `;

        return;

    }


    element.innerHTML =
        skills
            .map(function (skill) {

                return `
                    <span class="missing-skill-chip">
                        ${escapeHtml(skill)}
                    </span>
                `;

            })
            .join("");

}


// =====================================================
// AI RECOMMENDED SKILLS
// =====================================================

function renderRecommendedSkills(
    skills
) {

    const element =
        document.getElementById(
            "recommendedSkills"
        );


    if (!element) {

        return;

    }


    if (
        !Array.isArray(skills) ||
        skills.length === 0
    ) {

        element.innerHTML = `
            <p class="empty">
                Gemini did not return any recommended skills.
            </p>
        `;

        return;

    }


    element.innerHTML =
        skills
            .map(function (skill, index) {

                return `
                    <div class="skill-learning-card">

                        <div class="skill-number">
                            ${index + 1}
                        </div>

                        <div>

                            <strong>
                                ${escapeHtml(skill)}
                            </strong>

                            <p>
                                Recommended by Gemini AI
                                to improve your resume
                                for the target job.
                            </p>

                        </div>

                    </div>
                `;

            })
            .join("");

}


// =====================================================
// AI IMPROVEMENT SUGGESTIONS
// =====================================================

function renderList(
    elementId,
    items,
    emptyMessage
) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element) {

        return;

    }


    if (
        !Array.isArray(items) ||
        items.length === 0
    ) {

        element.innerHTML = `
            <p class="empty">
                ${escapeHtml(emptyMessage)}
            </p>
        `;

        return;

    }


    element.innerHTML = `

        <ul class="analysis-list">

            ${items
                .map(function (item) {

                    return `
                        <li>
                            ${escapeHtml(item)}
                        </li>
                    `;

                })
                .join("")}

        </ul>

    `;

}


// =====================================================
// GEMINI FINAL FEEDBACK
// =====================================================

function renderFinalFeedback(
    feedback
) {

    const element =
        document.getElementById(
            "aiFeedback"
        );


    if (!element) {

        console.error(
            "aiFeedback element not found."
        );

        return;

    }


    console.log(
        "Gemini final feedback:",
        feedback
    );


    // ---------------------------------------------
    // NO FEEDBACK
    // ---------------------------------------------

    if (
        feedback === undefined ||
        feedback === null ||
        String(feedback).trim() === ""
    ) {

        element.innerHTML = `

            <div class="feedback-block">

                <h3>
                    Gemini AI Feedback
                </h3>

                <p>
                    Gemini did not return final feedback.
                </p>

            </div>

        `;

        return;

    }


    // ---------------------------------------------
    // DISPLAY FEEDBACK
    // ---------------------------------------------

    element.innerHTML = `

        <div class="feedback-block">

            <h3>
                Gemini's Resume Assessment
            </h3>

            <p>
                ${escapeHtml(feedback)}
            </p>

        </div>

    `;

}


// =====================================================
// HTML ESCAPE
// =====================================================

function escapeHtml(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );

}


// =====================================================
// TOAST
// =====================================================

function toast(message) {

    const toastElement =
        document.getElementById(
            "toast"
        );


    if (!toastElement) {

        return;

    }


    toastElement.textContent =
        message;


    toastElement.classList.add(
        "show"
    );


    setTimeout(function () {

        toastElement.classList.remove(
            "show"
        );

    }, 3000);

}