// Add interactive effects and form validation

document.addEventListener('DOMContentLoaded', function() {
    // Add loading animation to form submission
    const form = document.querySelector('.recommendation-form');
    const submitBtn = document.querySelector('.btn-submit');
    const presetButtons = document.querySelectorAll('.preset-btn');

    const presets = {
        balanced: {
            nitrogen: 80,
            phosphorus: 45,
            potassium: 40,
            temperature: 26,
            humidity: 62,
            ph: 6.6,
            rainfall: 180
        },
        humid: {
            nitrogen: 95,
            phosphorus: 40,
            potassium: 45,
            temperature: 28,
            humidity: 82,
            ph: 6.1,
            rainfall: 240
        },
        dry: {
            nitrogen: 55,
            phosphorus: 32,
            potassium: 35,
            temperature: 31,
            humidity: 42,
            ph: 7.2,
            rainfall: 80
        }
    };

    if (!form || !submitBtn) {
        return;
    }
    
    form.addEventListener('submit', function(e) {
        // Add loading state
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        submitBtn.disabled = true;
        
        // Re-enable after a short delay (in case of client-side validation)
        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fa-solid fa-leaf"></i> Recommend Crop';
        }, 2000);
    });
    
    // Add input focus effects
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
        
        // Add real-time validation
        input.addEventListener('input', function() {
            validateInput(this);
        });
    });
    
    // Add smooth scroll for prediction result
    const predictionResult = document.querySelector('.prediction-result');
    if (predictionResult) {
        predictionResult.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    presetButtons.forEach(button => {
        button.addEventListener('click', function() {
            const key = this.dataset.preset;
            const preset = presets[key];
            if (!preset) {
                return;
            }

            Object.keys(preset).forEach(name => {
                const input = form.querySelector(`input[name="${name}"]`);
                if (input) {
                    input.value = preset[name];
                    validateInput(input);
                }
            });
        });
    });
    
    // Add particle effect on button hover
    submitBtn.addEventListener('mouseenter', createParticles);
});

function validateInput(input) {
    const value = parseFloat(input.value);
    const name = input.name;
    
    // Basic validation ranges (you can adjust these)
    const ranges = {
        nitrogen: { min: 0, max: 200 },
        phosphorus: { min: 0, max: 150 },
        potassium: { min: 0, max: 200 },
        temperature: { min: -10, max: 50 },
        humidity: { min: 0, max: 100 },
        ph: { min: 0, max: 14 },
        rainfall: { min: 0, max: 1000 }
    };
    
    if (ranges[name]) {
        if (value < ranges[name].min || value > ranges[name].max) {
            input.style.borderColor = '#e17055';
            input.style.boxShadow = '0 0 0 3px rgba(225, 112, 85, 0.1)';
        } else {
            input.style.borderColor = '#00b894';
            input.style.boxShadow = '0 0 0 3px rgba(0, 184, 148, 0.1)';
        }
    }
}

function createParticles() {
    const btn = document.querySelector('.btn-submit');
    const rect = btn.getBoundingClientRect();
    
    for (let i = 0; i < 10; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = rect.left + rect.width / 2 + 'px';
        particle.style.top = rect.top + rect.height / 2 + 'px';
        particle.style.setProperty('--x', (Math.random() - 0.5) * 100 + 'px');
        particle.style.setProperty('--y', (Math.random() - 0.5) * 100 + 'px');
        document.body.appendChild(particle);
        
        setTimeout(() => {
            particle.remove();
        }, 1000);
    }
}

// Add particle styles dynamically
const particleStyles = document.createElement('style');
particleStyles.textContent = `
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: #00b894;
        border-radius: 50%;
        pointer-events: none;
        animation: particleFloat 1s ease-out forwards;
        z-index: 1000;
    }
    
    @keyframes particleFloat {
        0% {
            opacity: 1;
            transform: translate(0, 0) scale(1);
        }
        100% {
            opacity: 0;
            transform: translate(var(--x), var(--y)) scale(0);
        }
    }
    
    .form-group.focused label {
        color: #00b894;
        transform: translateY(-2px);
    }
    
    .form-group.focused label i {
        transform: scale(1.1);
    }
`;
document.head.appendChild(particleStyles);