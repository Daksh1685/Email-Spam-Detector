document.addEventListener('DOMContentLoaded', function() {
    const spamForm = document.getElementById('spamForm');
    const emailInput = document.getElementById('emailText');
    
    if (spamForm) {
        spamForm.addEventListener('submit', handleFormSubmit);
    }
});

async function handleFormSubmit(e) {
    e.preventDefault();

    const emailText = document.getElementById('emailText').value.trim();
    const resultContainer = document.getElementById('resultContainer');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const errorAlert = document.getElementById('errorAlert');

    resultContainer.classList.add('d-none');
    errorAlert.classList.add('d-none');
    loadingSpinner.classList.remove('d-none');

    try {
        const response = await fetch('/detect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email_text: emailText
            })
        });

        if (!response.ok) {
            const error = await response.json();
            showError(error.error || 'An error occurred');
            return;
        }

        const data = await response.json();
        
        if (data.success) {
            displayResult(data);
        } else {
            showError(data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to the server. Please try again.');
    } finally {
        loadingSpinner.classList.add('d-none');
    }
}

function displayResult(data) {
    const resultContainer = document.getElementById('resultContainer');
    const resultCard = document.getElementById('resultCard');
    const resultStatus = document.getElementById('resultStatus');
    const resultMessage = document.getElementById('resultMessage');
    const resultIcon = document.getElementById('resultIcon');
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceText = document.getElementById('confidenceText');

    resultCard.classList.remove('success-card', 'danger-card');
    resultIcon.innerHTML = '';

    if (data.result === 'Ham') {
        resultStatus.textContent = '✓ Legitimate Email';
        resultStatus.style.color = '#27ae60';
        resultMessage.textContent = data.message;
        resultIcon.innerHTML = '<i class="bi bi-check-circle-fill result-success"></i>';
        resultCard.classList.add('success-card');
    } else {
        resultStatus.textContent = '✗ Spam Email';
        resultStatus.style.color = '#e74c3c';
        resultMessage.textContent = data.message;
        resultIcon.innerHTML = '<i class="bi bi-exclamation-circle-fill result-danger"></i>';
        resultCard.classList.add('danger-card');
    }

    const confidence = parseFloat(data.confidence);
    confidenceBar.style.width = confidence + '%';
    confidenceText.textContent = confidence.toFixed(2) + '%';

    if (confidence >= 90) {
        confidenceBar.style.background = 'linear-gradient(90deg, #27ae60 0%, #229954 100%)';
    } else if (confidence >= 70) {
        confidenceBar.style.background = 'linear-gradient(90deg, #f39c12 0%, #e67e22 100%)';
    } else {
        confidenceBar.style.background = 'linear-gradient(90deg, #e74c3c 0%, #c0392b 100%)';
    }

    resultContainer.classList.remove('d-none');
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(errorMessage) {
    const errorAlert = document.getElementById('errorAlert');
    const errorMessageSpan = document.getElementById('errorMessage');

    errorMessageSpan.textContent = errorMessage;
    errorAlert.classList.remove('d-none');

    setTimeout(() => {
        errorAlert.classList.add('d-none');
    }, 5000);
}

function resetForm() {
    document.getElementById('spamForm').reset();
    document.getElementById('resultContainer').classList.add('d-none');
    document.getElementById('errorAlert').classList.add('d-none');
    document.getElementById('emailText').focus();
}

function trimString(str) {
    return str.replace(/^\s+|\s+$/g, '');
}

function formatPercentage(value) {
    return (parseFloat(value) * 100).toFixed(2) + '%';
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 'Enter') {
        const spamForm = document.getElementById('spamForm');
        if (spamForm && !document.getElementById('resultContainer').classList.contains('d-none')) {
            handleFormSubmit(new Event('submit'));
        }
    }

    if (event.key === 'Escape') {
        const resultContainer = document.getElementById('resultContainer');
        if (!resultContainer.classList.contains('d-none')) {
            resetForm();
        }
    }
});

document.getElementById('emailText')?.addEventListener('dblclick', function() {
    this.value = 'Free Tickets for IPL! Click here to claim your prize now.';
});

const emailInput = document.getElementById('emailText');
if (emailInput) {
    emailInput.addEventListener('input', function() {
        const charCount = this.value.length;
    });
}