const subjectMap = {
    "semester_1": ["Physics Dummy", "Maths Dummy", "Chemistry Dummy"],
    "semester_2": ["BEE Dummy", "Mechanics Dummy", "Graphics Dummy"],
    "semester_3": ["Maths", "DBMS", "DS", "COA", "DSGT"],
    "semester_4": ["Maths", "AOA", "CTD", "MDM", "OS"],
    "semester_5": ["TCS Dummy", "SE Dummy", "CN Dummy"],
    "semester_6": ["SPCC Dummy", "CSS Dummy", "AI Dummy"],
    "semester_7": ["DSIP Dummy", "MCC Dummy"],
    "semester_8": ["HMI Dummy", "DC Dummy"]
};

document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem('theme');
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    let currentTheme = savedTheme;
    if (!currentTheme) {
        currentTheme = systemDark ? 'dark' : 'light';
    }
    
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    const semesterSelect = document.getElementById("semester");
    const subjectSelect = document.getElementById("subject");

    function populateSubjects() {
        if (!semesterSelect || !subjectSelect) return;
        const selectedSem = semesterSelect.value;
        const subjects = subjectMap[selectedSem] || ["Dummy Subject"];
        
        subjectSelect.innerHTML = "";
        subjects.forEach(sub => {
            const opt = document.createElement("option");
            opt.value = sub; 
            opt.textContent = sub;
            subjectSelect.appendChild(opt);
        });
    }

    if (semesterSelect) {
        semesterSelect.addEventListener("change", populateSubjects);
        populateSubjects();
    }
});

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const btn = document.getElementById('themeToggleBtn');
    if (btn) {
        btn.innerText = theme === 'dark' ? '☀️' : '🌙'; // If dark, show sun to toggle light. If light, show moon.
    }
}

async function analyzePYQ() {
    const semester = document.getElementById("semester").value;
    const subject = document.getElementById("subject").value;
    const syllabusFile = document.getElementById("syllabusFile").files[0];
    const btn = document.getElementById("analyzeBtn");

    if (!subject.trim()) {
        alert("Please enter a subject name.");
        return;
    }

    if (!syllabusFile) {
        alert("Please upload your syllabus file.");
        return;
    }

    try {
        btn.classList.add("loading");
        btn.disabled = true;
        
        let formData = new FormData();
        formData.append("semester", semester);
        formData.append("subject", subject);
        formData.append("syllabus", syllabusFile);

        let analyzeResponse = await fetch("/analyze_semester", {
            method: "POST",
            body: formData
        });

        let result = await analyzeResponse.json();

        if (result.error) {
            document.getElementById("result").innerHTML = `<p>${result.error}</p>`;
            return;
        }

        let output = result.top_questions.map(r =>
            `<p><b>Topic:</b> ${r.topic} <br>
             <b>Relevance Score:</b> ${r.score} (Found ${r.frequency} time${r.frequency > 1 ? 's' : ''})<br>
             ${r.question}</p>`
        ).join("");

        if (!output) {
            output = "<p>No matching questions found.</p>";
        }

        document.getElementById("result").innerHTML = output;
    } catch (e) {
        document.getElementById("result").innerHTML = `<p>Something went wrong: ${e.message}</p>`;
    } finally {
        btn.classList.remove("loading");
        btn.disabled = false;
    }
}


async function scanImage() {
    const fileInput = document.getElementById("imageFile");
    const btn = document.getElementById("scanBtn");

    if (!fileInput.files[0]) {
        alert("Please upload an image first.");
        return;
    }

    try {
        btn.classList.add("loading");
        btn.disabled = true;

        let formData = new FormData();
        formData.append("image", fileInput.files[0]);

        let response = await fetch("/extract_image", {
            method: "POST",
            body: formData
        });

        let data = await response.json();

        document.getElementById("ocrResult").innerText = data.text;
    } catch (e) {
        document.getElementById("ocrResult").innerText = "Failed to scan image. Please try again.";
    } finally {
        btn.classList.remove("loading");
        btn.disabled = false;
    }
}