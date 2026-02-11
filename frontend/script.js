document.addEventListener('DOMContentLoaded', () => {
    // --- Auth UI Logic ---
    const navUl = document.querySelector('nav ul');

    function isUserLoggedIn() {
        const t = localStorage.getItem('soil_ai_token');
        const u = localStorage.getItem('soil_ai_user');
        return t && t !== 'null' && t !== 'undefined' && t !== '' && u;
    }

    function updateNav() {
        const loggedIn = isUserLoggedIn();
        const username = localStorage.getItem('soil_ai_user');

        const authLinks = document.getElementById('nav-auth-links');
        const userProfile = document.getElementById('nav-user-profile');
        const navUsername = document.getElementById('nav-username');
        const logoutLink = document.getElementById('logout-link');

        if (loggedIn && username) {
            // User is logged in
            if (authLinks) authLinks.classList.add('hidden');
            if (userProfile) {
                userProfile.classList.remove('hidden');
                if (navUsername) navUsername.textContent = username;
            }

            // Handle Logout
            if (logoutLink) {
                logoutLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    localStorage.removeItem('soil_ai_token');
                    localStorage.removeItem('soil_ai_user');
                    window.location.reload();
                });
            }
        } else {
            // Guest mode
            if (authLinks) authLinks.classList.remove('hidden');
            if (userProfile) userProfile.classList.add('hidden');
        }
    }
    updateNav();

    // --- Main Logic ---
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeImgBtn = document.getElementById('remove-img');
    const resultsSection = document.getElementById('results-section');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');

    let selectedFile = null;

    if (dropZone) {
        dropZone.addEventListener('click', () => {
            if (!selectedFile) fileInput.click();
        });

        fileInput.addEventListener('change', (e) => {
            handleFile(e.target.files[0]);
        });

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.style.borderColor = '#00ff88';
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.style.borderColor = 'rgba(255, 255, 255, 0.1)';
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            handleFile(e.dataTransfer.files[0]);
        });
    }

    function handleFile(file) {
        if (!file || !file.type.startsWith('image/')) {
            alert('Please upload a valid soil image.');
            return;
        }

        selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            previewContainer.classList.remove('hidden');
            analyzeBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    if (removeImgBtn) {
        removeImgBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            selectedFile = null;
            fileInput.value = '';
            previewContainer.classList.add('hidden');
            analyzeBtn.disabled = true;
            if (resultsSection) resultsSection.classList.add('hidden');
        });
    }

    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', async () => {
            const loggedIn = isUserLoggedIn();
            const token = localStorage.getItem('soil_ai_token');
            const guestScansKey = 'soil_ai_guest_scans';

            if (!loggedIn) {
                let scans = parseInt(localStorage.getItem(guestScansKey) || '0');
                if (scans >= 5) {
                    alert('Guest limit (5 scans) reached. Please Login or Sign Up to continue!');
                    window.location.href = 'login.html';
                    return;
                }
            }

            if (!selectedFile) {
                alert('Please select a soil image first.');
                return;
            }

            analyzeBtn.disabled = true;
            btnText.textContent = 'Analyzing...';
            loader.classList.remove('hidden');
            if (resultsSection) resultsSection.classList.add('hidden');

            const formData = new FormData();
            formData.append('image', selectedFile);

            const headers = {};
            if (loggedIn) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            const handleSuccess = (data) => {
                if (!loggedIn) {
                    let scans = parseInt(localStorage.getItem(guestScansKey) || '0');
                    localStorage.setItem(guestScansKey, scans + 1);
                }
                displayResults(data);
            };

            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: headers,
                    body: formData
                });

                if (response.status === 401 && loggedIn) {
                    localStorage.removeItem('soil_ai_token');
                    localStorage.removeItem('soil_ai_user');
                    alert('Session expired. Processing as a guest scan.');

                    const guestResponse = await fetch('/api/analyze', {
                        method: 'POST',
                        body: formData
                    });
                    if (!guestResponse.ok) throw new Error('Analysis failed');
                    const data = await guestResponse.json();
                    handleSuccess(data);
                    return;
                }

                if (!response.ok) {
                    const err = await response.json().catch(() => ({ detail: 'Analysis failed' }));
                    throw new Error(err.detail || 'Analysis failed');
                }

                const data = await response.json();
                handleSuccess(data);
            } catch (error) {
                console.error(error);
                alert('Error: ' + error.message);
                btnText.textContent = 'Retry Analysis';
            } finally {
                loader.classList.add('hidden');
                analyzeBtn.disabled = false;
                btnText.textContent = 'Analyze Soil Sample';
            }
        });
    }

    function displayResults(data) {
        if (!resultsSection) return;
        resultsSection.classList.remove('hidden');

        document.getElementById('res-soil-type').textContent = `${data.soil_type} (${data.confidence})`;
        document.getElementById('res-score').textContent = data.health_score;
        document.getElementById('res-texture').textContent = data.texture;
        document.getElementById('res-ph').textContent = `${data.ph_min} - ${data.ph_max}`;
        document.getElementById('res-nitrogen').textContent = data.nitrogen;
        document.getElementById('res-phosphorus').textContent = data.phosphorus;
        document.getElementById('res-potassium').textContent = data.potassium;
        document.getElementById('res-om').textContent = data.organic_matter;
        document.getElementById('res-moisture').textContent = data.moisture;
        document.getElementById('res-water-ret').textContent = data.water_retention;
        document.getElementById('res-salinity').textContent = data.salinity_ec;
        document.getElementById('res-cec').textContent = data.cec;
        document.getElementById('res-season').textContent = data.planting_season;
        document.getElementById('res-temp').textContent = data.optimal_temp;
        document.getElementById('res-drainage').textContent = data.drainage_type;
        document.getElementById('res-compaction').textContent = data.compaction_level;
        document.getElementById('res-deficiencies').textContent = data.possible_deficiencies.join(', ');
        document.getElementById('res-fertilizer').textContent = data.recommended_fertilizer;

        const microList = document.getElementById('micro-list');
        if (microList) {
            microList.innerHTML = '';
            for (const [nutrient, value] of Object.entries(data.micro_nutrients)) {
                const div = document.createElement('div');
                div.className = 'micro-item';
                div.innerHTML = `<div>${nutrient}</div><div>${value}</div>`;
                microList.appendChild(div);
            }
        }

        const cropsList = document.getElementById('crops-list');
        if (cropsList) {
            cropsList.innerHTML = '';
            data.recommended_crops.forEach(crop => {
                const span = document.createElement('span');
                span.className = 'crop-tag';
                span.textContent = crop;
                cropsList.appendChild(span);
            });
        }

        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // --- Dynamic Plan Button Click Handler ---
    document.addEventListener('click', (e) => {
        if (e.target && e.target.classList.contains('primary-btn') && e.target.textContent.includes('Get Started')) {
            const heroSection = document.querySelector('.hero');
            if (heroSection) {
                heroSection.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });

    console.log('Soil AI Backend Ready.');
});
