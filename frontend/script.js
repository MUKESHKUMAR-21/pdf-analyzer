document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('upload-section');
    const fileInput = document.getElementById('file-input');
    const loadingSection = document.getElementById('loading-section');
    const settingsSection = document.getElementById('settings-section');
    const resultsSection = document.getElementById('results-section');
    const errorMessage = document.getElementById('error-message');
    const topicContainer = document.getElementById('topic-container');
    const questionsContainer = document.getElementById('questions-container');
    const resetBtn = document.getElementById('reset-btn');

    // Drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    });

    // Click to upload
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', function () {
        handleFiles(this.files);
    });

    resetBtn.addEventListener('click', () => {
        resultsSection.classList.add('hidden');
        dropZone.classList.remove('hidden');
        settingsSection.classList.remove('hidden');
        fileInput.value = '';
        errorMessage.classList.add('hidden');
    });

    function handleFiles(files) {
        if (files.length === 0) return;

        const file = files[0];

        if (file.type !== 'application/pdf') {
            showError('Please upload a valid PDF file.');
            return;
        }

        uploadFile(file);
    }

    async function uploadFile(file) {
        // UI transitions
        dropZone.classList.add('hidden');
        settingsSection.classList.add('hidden');
        errorMessage.classList.add('hidden');
        loadingSection.classList.remove('hidden');

        const numQuestions = document.getElementById('num-questions').value;
        const difficulty = document.getElementById('difficulty').value;

        const formData = new FormData();
        formData.append('file', file);
        formData.append('num_questions', numQuestions);
        formData.append('difficulty', difficulty);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'An error occurred during analysis');
            }

            renderQuestions(data.data.questions, data.data.topic);

            loadingSection.classList.add('hidden');
            resultsSection.classList.remove('hidden');

        } catch (error) {
            loadingSection.classList.add('hidden');
            dropZone.classList.remove('hidden');
            settingsSection.classList.remove('hidden');
            showError(error.message);
        }
    }

    function renderQuestions(questions, topic) {
        questionsContainer.innerHTML = '';

        if (topic) {
            topicContainer.innerHTML = `<h3>Topic: <span class="highlight">${topic}</span></h3>`;
            topicContainer.classList.remove('hidden');
        } else {
            topicContainer.classList.add('hidden');
        }

        if (!Array.isArray(questions) || questions.length === 0) {
            showError("The AI didn't return any questions. Please try again.");
            return;
        }

        questions.forEach((q, index) => {
            const card = document.createElement('div');
            card.className = 'question-card';

            const badgeClass = q.type === 'mcq' ? 'mcq' : 'short';
            const badgeText = q.type === 'mcq' ? 'Multiple Choice' : 'Short Answer';

            let optionsHtml = '';
            if (q.type === 'mcq' && Array.isArray(q.options)) {
                optionsHtml = '<ul class="options-list">';
                q.options.forEach(opt => {
                    optionsHtml += `<li class="option-item">${opt}</li>`;
                });
                optionsHtml += '</ul>';
            }

            card.innerHTML = `
                <span class="badge ${badgeClass}">${badgeText}</span>
                <div class="question-text">Q${index + 1}. ${q.question}</div>
                ${optionsHtml}
                <div class="answer-section">
                    <button class="answer-btn" onclick="this.nextElementSibling.classList.toggle('hidden')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                        Reveal Answer
                    </button>
                    <div class="answer-content hidden">
                        <strong>Correct Answer:</strong> <br/>
                        ${q.answer}
                    </div>
                </div>
            `;

            questionsContainer.appendChild(card);
        });
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        errorMessage.classList.remove('hidden');
    }
});