document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictor-form');
    const errorAlert = document.getElementById('js-error-alert');
    const errorMsg = document.getElementById('js-error-msg');
    const loadingOverlay = document.getElementById('loading-overlay');

    if (form) {
        form.addEventListener('submit', (event) => {
            const cloudInput = document.getElementById('cloud');
            const annualInput = document.getElementById('annual');
            const janfebInput = document.getElementById('janfeb');
            const marMayInput = document.getElementById('marMay');
            const juneSeptInput = document.getElementById('juneSept');

            let isValid = true;
            let errors = [];

            // Clear previous validation states
            [cloudInput, annualInput, janfebInput, marMayInput, juneSeptInput].forEach(input => {
                input.classList.remove('is-invalid');
            });
            errorAlert.classList.add('d-none');
            errorMsg.innerHTML = '';

            // 1. Check for blank fields
            const inputs = [
                { elem: cloudInput, name: 'Cloud Cover' },
                { elem: annualInput, name: 'Annual Rainfall' },
                { elem: janfebInput, name: 'Jan-Feb Rainfall' },
                { elem: marMayInput, name: 'Mar-May Rainfall' },
                { elem: juneSeptInput, name: 'Jun-Sep Rainfall' }
            ];

            for (const input of inputs) {
                if (input.elem.value.trim() === '') {
                    input.elem.classList.add('is-invalid');
                    errors.push(`• <strong>${input.name}</strong> cannot be empty.`);
                    isValid = false;
                }
            }

            // If empty fields exist, stop and display
            if (!isValid) {
                event.preventDefault();
                errorMsg.innerHTML = errors.join('<br>');
                errorAlert.classList.remove('d-none');
                errorAlert.scrollIntoView({ behavior: 'smooth' });
                return;
            }

            // 2. Validate ranges and negative values
            const cloudVal = parseFloat(cloudInput.value);
            const annualVal = parseFloat(annualInput.value);
            const janfebVal = parseFloat(janfebInput.value);
            const marMayVal = parseFloat(marMayInput.value);
            const juneSeptVal = parseFloat(juneSeptInput.value);

            // Cloud cover range: 0-100
            if (isNaN(cloudVal) || cloudVal < 0 || cloudVal > 100) {
                cloudInput.classList.add('is-invalid');
                errors.push('• <strong>Cloud Cover</strong> must be a valid number between 0% and 100%.');
                isValid = false;
            }

            // Positive constraints
            if (isNaN(annualVal) || annualVal < 0) {
                annualInput.classList.add('is-invalid');
                errors.push('• <strong>Annual Rainfall</strong> must be a non-negative number.');
                isValid = false;
            }
            if (isNaN(janfebVal) || janfebVal < 0) {
                janfebInput.classList.add('is-invalid');
                errors.push('• <strong>Jan-Feb Rainfall</strong> must be a non-negative number.');
                isValid = false;
            }
            if (isNaN(marMayVal) || marMayVal < 0) {
                marMayInput.classList.add('is-invalid');
                errors.push('• <strong>Mar-May Rainfall</strong> must be a non-negative number.');
                isValid = false;
            }
            if (isNaN(juneSeptVal) || juneSeptVal < 0) {
                juneSeptInput.classList.add('is-invalid');
                errors.push('• <strong>Jun-Sep Rainfall</strong> must be a non-negative number.');
                isValid = false;
            }

            // 3. Logical Check: Sum of seasonal rainfall cannot exceed Annual Rainfall
            if (isValid) {
                const seasonalSum = janfebVal + marMayVal + juneSeptVal;
                if (seasonalSum > annualVal) {
                    [janfebInput, marMayInput, juneSeptInput, annualInput].forEach(input => {
                        input.classList.add('is-invalid');
                    });
                    errors.push(`• <strong>Logical Conflict:</strong> The sum of seasonal rainfall (Jan-Feb + Mar-May + Jun-Sep) is <strong>${seasonalSum.toFixed(2)} mm</strong>, which exceeds the total Annual Rainfall of <strong>${annualVal.toFixed(2)} mm</strong>.`);
                    isValid = false;
                }
            }

            // Handle invalid submission
            if (!isValid) {
                event.preventDefault();
                errorMsg.innerHTML = errors.join('<br>');
                errorAlert.classList.remove('d-none');
                errorAlert.scrollIntoView({ behavior: 'smooth' });
            } else {
                // If form is valid, trigger loading overlay
                loadingOverlay.classList.remove('d-none');
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span> Predicting...';
                }
            }
        });
    }
});
