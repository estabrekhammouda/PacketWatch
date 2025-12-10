document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form data - FIXED: Properly get radio button value
    const unusualTimeRadio = document.querySelector('input[name="unusual_time_access"]:checked');
    
    const formData = {
        session_id: document.getElementById('session_id').value,
        network_packet_size: parseInt(document.getElementById('network_packet_size').value),
        protocol_type: document.getElementById('protocol_type').value,
        login_attempts: parseInt(document.getElementById('login_attempts').value),
        session_duration: parseFloat(document.getElementById('session_duration').value),
        encryption_used: document.getElementById('encryption_used').value || null,
        ip_reputation_score: parseFloat(document.getElementById('ip_reputation_score').value),
        failed_logins: parseInt(document.getElementById('failed_logins').value),
        browser_type: document.getElementById('browser_type').value,
        unusual_time_access: unusualTimeRadio ? parseInt(unusualTimeRadio.value) : 0
    };

    // Show spinner
    const submitBtn = document.querySelector('.btn-submit');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner"></span>';

    try {
        // Send request to API
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        // Display result
        displayResult(result, formData);

        // Hide form, show result
        document.querySelector('.form-section').style.display = 'none';
        document.getElementById('resultSection').style.display = 'block';

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });

    } catch (error) {
        console.error('Error:', error);
        showError('Failed to analyze session. Please check if the API server is running.');
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
});

function displayResult(result, formData) {
    const resultCard = document.getElementById('resultCard');
    const isAttack = result.attack_detected === 1;

    const riskLevel = isAttack ? 'HIGH RISK ⚠️' : 'SAFE ✅';
    const riskClass = isAttack ? 'threat' : 'safe';

    let html = `
        <div class="result-status ${riskClass}">
            ${riskLevel}
        </div>
        <div class="result-details">
            <p><strong>Session ID:</strong> ${escapeHtml(formData.session_id)}</p>
            <p><strong>Prediction:</strong> ${isAttack ? '🚨 ATTACK DETECTED' : '✅ NORMAL TRAFFIC'}</p>
            <p><strong>Confidence:</strong> ${isAttack ? 'Potential intrusion' : 'Benign session'}</p>
            
            <h3 style="margin-top: 20px; color: #667eea;">Session Details:</h3>
            <p><strong>Protocol:</strong> ${formData.protocol_type}</p>
            <p><strong>Packet Size:</strong> ${formData.network_packet_size} bytes</p>
            <p><strong>Session Duration:</strong> ${formData.session_duration} seconds</p>
            <p><strong>Login Attempts:</strong> ${formData.login_attempts}</p>
            <p><strong>Failed Logins:</strong> ${formData.failed_logins}</p>
            <p><strong>IP Reputation Score:</strong> ${formData.ip_reputation_score}/100</p>
            <p><strong>Encryption:</strong> ${formData.encryption_used || 'None'}</p>
            <p><strong>Browser Type:</strong> ${formData.browser_type}</p>
            <p><strong>Unusual Time Access:</strong> ${formData.unusual_time_access === 1 ? 'Yes' : 'No'}</p>
        </div>
    `;

    resultCard.innerHTML = html;
    resultCard.className = `result-card ${riskClass}`;
}

function resetForm() {
    // Show form, hide result
    document.querySelector('.form-section').style.display = 'block';
    document.getElementById('resultSection').style.display = 'none';

    // Reset form
    document.getElementById('predictionForm').reset();

    // Reset button state
    const submitBtn = document.querySelector('.btn-submit');
    submitBtn.disabled = false;
    submitBtn.textContent = '🔍 Analyze Session';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showError(message) {
    const resultCard = document.getElementById('resultCard');
    resultCard.innerHTML = `
        <div class="error-message">
            <strong>❌ Error</strong>
            <p>${escapeHtml(message)}</p>
        </div>
    `;
    resultCard.className = 'result-card error';
    document.getElementById('resultSection').style.display = 'block';
}

// Utility function to prevent XSS attacks
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add event listener for reset button
document.addEventListener('DOMContentLoaded', () => {
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetForm);
    }
});

console.log('PacketWatch initialized successfully');