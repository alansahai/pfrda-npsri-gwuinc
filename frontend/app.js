/**
 * NPS Retirement Intelligence Engine - Premium Frontend
 * Enterprise-Grade JavaScript with Advanced Animations & API Integration
 * Version: 2.0.0 (Premium)
 */

// ==================== CONFIGURATION ====================

const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    PROJECTION_ENDPOINT: '/api/v1/projections/calculate',
    HEALTH_ENDPOINT: '/health',
    DEBOUNCE_DELAY: 500,
    API_TIMEOUT: 30000
};

// ==================== TRANSLATIONS ====================

const TRANSLATIONS = {
    en: {
        // Navigation
        home: 'Home',
        dashboard: 'Dashboard',
        methodology: 'Methodology',

        // Hero Section
        heroTitle: 'Plan Your Retirement\nWith Precision',
        heroSubtitle: 'Advanced Monte Carlo simulation for confident pension forecasting',

        // KPI Cards
        totalCorpus: 'Total Corpus',
        monthlyPension: 'Monthly Pension',
        lumpSum: 'Lump Sum',
        projectionPeriod: 'Projection Period',

        // Form Labels
        currentAge: 'Current Age',
        retirementAge: 'Retirement Age',
        monthlyContribution: 'Monthly Contribution (₹)',
        annualGrowth: 'Annual Income Growth (%)',
        riskProfile: 'Risk Profile',

        // Buttons
        calculate: 'Calculate ➤',
        compare: 'Compare ↔',
        reset: 'Reset',

        // Risk Profiles
        conservative: 'Conservative',
        moderate: 'Moderate',
        aggressive: 'Aggressive',

        // Assumptions
        assumptionsTitle: 'Assumptions & Methodology',
        monteCarloExplain: 'Monte Carlo Simulation',
        annuityAllocation: 'Annuity Allocation',
        returnAssumptions: 'Return Assumptions',
        disclaimer: 'Important Disclaimer',

        // Messages
        loading: 'Calculating...',
        error: 'An error occurred. Please try again.',
        success: 'Calculation successful!',

        // Units
        years: 'years',
        rupee: '₹'
    },
    ta: {
        // Navigation
        home: 'முகப்பு',
        dashboard: 'பணிமுறை',
        methodology: 'முறைமை',

        // Hero Section
        heroTitle: 'உங்கள் ஓய்வூதியத்தை\nகோยில் அளவீட்டிடம் திட்டமிடவும்',
        heroSubtitle: 'நம்பிக்கையான ஓய்வூதிய முனைய நிறுவனச் சொல்லப்பட உயர்வும் மாறுதல் உருவாக்கம்',

        // KPI Cards
        totalCorpus: 'மொத்த திரட்டல்',
        monthlyPension: 'மாதாந்திர ஓய்வூதியம்',
        lumpSum: 'ஒரே தொகை',
        projectionPeriod: 'முன்னறிவிப்பு காலம்',

        // Form Labels
        currentAge: 'தற்போதைய வயது',
        retirementAge: 'ஓய்வு வয்து',
        monthlyContribution: 'மாதாந்திர பங்களிப்பு (₹)',
        annualGrowth: 'ஆண்டு வருமான வளர்ச்சி (%)',
        riskProfile: 'ஆபத்து சுயவிவரணம்',

        // Buttons
        calculate: 'கணக்கிடவும் ➤',
        compare: 'ஒப்பிடவும் ↔',
        reset: 'மீட்டமை',

        // Risk Profiles
        conservative: 'பழமைவாத',
        moderate: 'மிதமான',
        aggressive: 'ஆக்கிரமண',

        // Assumptions
        assumptionsTitle: 'ஊகம் மற்றும் முறைமை',
        monteCarloExplain: 'மாண்டே கார்லோ உருவாக்கம்',
        annuityAllocation: 'ஆண்டியோரி பகிர்வு',
        returnAssumptions: 'திருப்பத ஊகம்',
        disclaimer: 'முக்கிய எச்சரிக்கை',

        // Messages
        loading: 'கணக்கிடுகிறது...',
        error: 'ஒரு பிழை ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்.',
        success: 'கணக்கீடு சफலமாக முடிந்தது!',

        // Units
        years: 'வருடங்கள்',
        rupee: '₹'
    }
};

// ==================== LANGUAGE MANAGEMENT ====================

let currentLanguage = localStorage.getItem('language') || 'en';

function setLanguage(lang) {
    try {
        if (lang === 'en' || lang === 'ta') {
            currentLanguage = lang;
            localStorage.setItem('language', lang);
            console.log('💾 Language saved to localStorage:', lang);

            // Update button state
            const btn = document.getElementById('languageToggle');
            if (btn) {
                btn.textContent = lang === 'en' ? 'EN | TA' : 'TA | EN';
                console.log('✅ Language toggle button updated');
            }

            // Update page content
            updatePageLanguage();
        }
    } catch (error) {
        console.error('⚠️  Error setting language:', error);
        // Default to English if anything goes wrong
        currentLanguage = 'en';
    }
}

function t(key) {
    return TRANSLATIONS[currentLanguage][key] || TRANSLATIONS['en'][key] || key;
}

function updatePageLanguage() {
    try {
        console.log('🌐 Updating page language to:', currentLanguage);

        // Update KPI card labels (not h3, but .kpi-label divs)
        const kpiCards = {
            corpus: document.querySelector('[data-kpi="corpus"] .kpi-label'),
            monthly: document.querySelector('[data-kpi="monthly"] .kpi-label'),
            lumpsum: document.querySelector('[data-kpi="lumpsum"] .kpi-label'),
            years: document.querySelector('[data-kpi="years"] .kpi-label')
        };

        if (kpiCards.corpus) kpiCards.corpus.textContent = t('totalCorpus');
        if (kpiCards.monthly) kpiCards.monthly.textContent = t('monthlyPension');
        if (kpiCards.lumpsum) kpiCards.lumpsum.textContent = t('lumpSum');
        if (kpiCards.years) kpiCards.years.textContent = t('projectionPeriod');

        // Update form labels
        const labels = document.querySelectorAll('label');
        labels.forEach(label => {
            const text = label.textContent.toLowerCase();
            if (text.includes('age') && !text.includes('retirement')) {
                label.textContent = t('currentAge');
            } else if (text.includes('retirement')) {
                label.textContent = t('retirementAge');
            } else if (text.includes('contribution')) {
                label.textContent = t('monthlyContribution');
            } else if (text.includes('growth')) {
                label.textContent = t('annualGrowth');
            } else if (text.includes('risk')) {
                label.textContent = t('riskProfile');
            }
        });

        // Update panel headers
        const panelHeaders = document.querySelectorAll('.panel-header h2');
        panelHeaders.forEach(h2 => {
            const text = h2.textContent.toLowerCase();
            if (text.includes('configure')) {
                h2.textContent = 'Configure Your Scenario'; // Keep as is for now
            } else if (text.includes('projection')) {
                h2.textContent = 'Retirement Projection'; // Keep as is for now
            } else if (text.includes('comparison')) {
                h2.textContent = 'Scenario Comparison'; // Keep as is for now
            } else if (text.includes('assumptions')) {
                h2.textContent = t('assumptionsTitle');
            }
        });

        console.log('✅ Page language updated successfully');
    } catch (error) {
        console.error('⚠️  Error updating page language:', error);
        // Don't crash - just log the error and continue
    }
}

// ==================== STATE ====================

const AppState = {
    chart: null,
    isLoading: false,
    activeProjectionPromise: null,
    activeProjectionRequestKey: null,
    pendingAutoCalculate: null,
    currentStep: 1,
    currentScenario: {
        age: 30,
        retirementAge: 60,
        contribution: 10000,
        riskProfile: 'moderate'
    }
};

// ==================== INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎯 NPS Retirement Intelligence Engine - Premium Edition Loading...');

    // Initialize language
    setLanguage(currentLanguage);

    // Hide loader after 1.5 seconds (shorter now)
    setTimeout(() => {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.style.animation = 'fadeOutAndUp 0.4s ease-out forwards';
            setTimeout(() => loader.style.display = 'none', 400);
        }
    }, 1500);

    // Initialize pipeline and features
    console.log('🔧 Initializing pipeline...');
    initializePipeline();

    console.log('🔧 Initializing custom cursor...');
    initializeCustomCursor();

    console.log('🔧 Initializing navbar...');
    initializeNavbarGlassmorphism();

    console.log('🔧 Initializing language toggle...');
    initializeLanguageToggle();

    console.log('🔧 Initializing accordions...');
    initializeAccordions();

    console.log('🔧 Initializing scroll reveal...');
    initializeScrollReveal();

    console.log('🔧 Initializing chart...');
    initializeChart();

    console.log('🔧 Attaching event listeners...');
    attachEventListeners();

    console.log('🔧 Fetching API version...');
    fetchApiVersion();

    console.log('✅ Premium Application Ready');
});

// ==================== PIPELINE MANAGEMENT ====================

function initializePipeline() {
    // Start at step 1
    updateVisibleStep(1);
    updatePipelineIndicator();
}

function updateVisibleStep(step) {
    console.log(`🔄 Updating to step ${step}`);
    AppState.currentStep = step;

    // Show/hide panels based on step
    document.querySelectorAll('[data-pipeline-step]').forEach(el => {
        const elStep = parseInt(el.getAttribute('data-pipeline-step'));
        if (elStep === step) {
            // SHOW THIS PANEL
            el.style.display = 'block';
            el.style.opacity = '1';
            el.style.pointerEvents = 'auto';
            el.classList.add('step-visible');
            el.style.animation = 'fadeInUp 0.6s ease-out forwards';

            // Ensure all form controls are interactive
            el.querySelectorAll('input, select, button, [role="button"]').forEach(ctrl => {
                ctrl.style.pointerEvents = 'auto';
            });

            console.log(`✅ Step ${step} panel visible and interactive`);
        } else {
            // HIDE OTHER PANELS
            el.classList.remove('step-visible');
            el.style.opacity = '0';
            el.style.pointerEvents = 'none';
            el.style.animation = 'none';
            setTimeout(() => {
                el.style.display = 'none';
            }, 100);
        }
    });

    updatePipelineIndicator();
}

function updatePipelineIndicator() {
    // Update pipeline progress visualization
    document.querySelectorAll('.pipeline-step').forEach((step, index) => {
        const stepNum = index + 1;
        step.classList.remove('active', 'completed');

        if (stepNum < AppState.currentStep) {
            step.classList.add('completed');
        } else if (stepNum === AppState.currentStep) {
            step.classList.add('active');
        }
    });

    // Update connectors
    document.querySelectorAll('.pipeline-connector').forEach((connector, index) => {
        connector.classList.remove('active');
        if (index < AppState.currentStep - 1) {
            connector.classList.add('active');
        }
    });
}

function advanceToNextStep(nextStep) {
    updateVisibleStep(nextStep);

    const activePanel = document.querySelector(`[data-pipeline-step="${nextStep}"]`);
    if (activePanel) {
        activePanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
        document.getElementById('dashboard').scrollIntoView({ behavior: 'smooth' });
    }
}

// ==================== CUSTOM CURSOR ====================

function initializeCustomCursor() {
    if (!matchMedia('(hover: hover)').matches) return;

    const cursor = document.querySelector('.custom-cursor');
    const ring = document.querySelector('.custom-cursor-ring');
    let mouseX = 0, mouseY = 0;
    let isHoveringInteractive = false;

    // Interactive elements that should enlarge the cursor
    const interactiveElements = '.btn, a, button, input, select, textarea, [role="button"]';

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;

        // Smooth cursor dot positioning
        cursor.style.left = (mouseX - 5) + 'px';
        cursor.style.top = (mouseY - 5) + 'px';

        // Smoother ring trailing (slight delay effect)
        ring.style.left = (mouseX - 16) + 'px';
        ring.style.top = (mouseY - 16) + 'px';

        // Check if hovering interactive element
        const target = e.target;
        const isInteractive = target.closest(interactiveElements);

        if (isInteractive && !isHoveringInteractive) {
            cursor.classList.add('active');
            ring.classList.add('hover');
            isHoveringInteractive = true;
        } else if (!isInteractive && isHoveringInteractive) {
            cursor.classList.remove('active');
            ring.classList.remove('hover');
            isHoveringInteractive = false;
        }
    });

    document.addEventListener('mouseenter', () => {
        cursor.style.display = 'block';
        ring.style.display = 'block';
    });

    document.addEventListener('mouseleave', () => {
        cursor.style.display = 'none';
        ring.style.display = 'none';
    });
}

// ==================== NAVBAR GLASSMORPHISM ====================

function initializeNavbarGlassmorphism() {
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

function initializeLanguageToggle() {
    const toggleBtn = document.getElementById('languageToggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const newLang = currentLanguage === 'en' ? 'ta' : 'en';
            setLanguage(newLang);
        });
        // Set initial button text
        toggleBtn.textContent = currentLanguage === 'en' ? 'EN | TA' : 'TA | EN';
    }
}

// ==================== SCROLL REVEAL ANIMATIONS ====================

function initializeScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Stagger animation based on element index
                const delay = index * 0.1;
                entry.target.style.animationDelay = delay + 's';
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                // Only animate once
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    });

    revealElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(40px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        observer.observe(el);
    });
}

// ==================== ACCORDIONS ====================

function initializeAccordions() {
    document.querySelectorAll('.accordion-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const item = this.closest('.accordion-item');
            const content = item.querySelector('.accordion-content');
            const isOpen = item.classList.contains('open');

            // Close all other accordions with smooth animation
            document.querySelectorAll('.accordion-item.open').forEach(openItem => {
                if (openItem !== item) {
                    const openContent = openItem.querySelector('.accordion-content');
                    openItem.classList.remove('open');

                    // Smooth close animation
                    if (openContent) {
                        openContent.style.opacity = '0';
                        openContent.style.maxHeight = '0';
                        setTimeout(() => {
                            openContent.style.display = 'none';
                        }, 300);
                    }
                }
            });

            // Toggle current accordion
            if (isOpen) {
                item.classList.remove('open');
                if (content) {
                    content.style.opacity = '0';
                    content.style.maxHeight = '0';
                    setTimeout(() => {
                        content.style.display = 'none';
                    }, 300);
                }
            } else {
                item.classList.add('open');
                if (content) {
                    content.style.display = 'block';
                    setTimeout(() => {
                        content.style.opacity = '1';
                        content.style.maxHeight = 'auto';
                    }, 10);
                }
            }
        });
    });
}

// ==================== EVENT LISTENERS ====================

// Central URL builder so API_BASE_URL is used consistently everywhere.
function buildApiUrl(path) {
    return `${CONFIG.API_BASE_URL}${path}`;
}

// Debouncer with cancel support to ensure submit can bypass pending auto-calculate.
function createDebouncer(func, delay) {
    let timeoutId;

    const debounced = function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            timeoutId = null;
            func.apply(this, args);
        }, delay);
    };

    debounced.cancel = () => {
        clearTimeout(timeoutId);
        timeoutId = null;
    };

    return debounced;
}

function ensureProjectionForm() {
    let form = document.getElementById('projection-form');
    if (form) return form;

    const panel = document.querySelector('[data-pipeline-step="1"]');
    const formContainer = panel?.querySelector('.form-container');
    const sliderSection = panel?.querySelector('.slider-section');
    const buttonGroup = panel?.querySelector('.button-group');

    if (!panel || !formContainer || !sliderSection || !buttonGroup) {
        console.error('❌ Unable to create projection form. Required nodes missing.', {
            panelFound: !!panel,
            formContainerFound: !!formContainer,
            sliderSectionFound: !!sliderSection,
            buttonGroupFound: !!buttonGroup
        });
        return null;
    }

    // Fix: create a real <form> wrapper when markup is missing one,
    // so submit events and Enter key behavior work reliably.
    form = document.createElement('form');
    form.id = 'projection-form';
    form.noValidate = true;

    panel.insertBefore(form, formContainer);
    form.appendChild(formContainer);
    form.appendChild(sliderSection);
    form.appendChild(buttonGroup);

    const calculateBtn = document.getElementById('calculate-btn');
    if (calculateBtn) {
        calculateBtn.type = 'submit';
    }

    console.log('✅ Created projection form wrapper dynamically.');
    return form;
}

function getScenarioFromDom() {
    const ageInput = document.getElementById('age-input');
    const retirementAgeInput = document.getElementById('retirement-age-input');
    const riskSelect = document.getElementById('risk-profile-select');
    const slider = document.getElementById('contribution-slider');

    return {
        age: Number.parseInt(ageInput?.value || '', 10),
        retirementAge: Number.parseInt(retirementAgeInput?.value || '', 10),
        contribution: Number.parseInt(slider?.value || '', 10),
        riskProfile: (riskSelect?.value || '').trim()
    };
}

function validateScenarioInput(scenario) {
    const errors = [];
    const validRiskProfiles = ['conservative', 'moderate', 'aggressive'];

    if (!Number.isFinite(scenario.age) || scenario.age < 18 || scenario.age > 65) {
        errors.push('Current age must be between 18 and 65.');
    }

    if (!Number.isFinite(scenario.retirementAge) || scenario.retirementAge < 40 || scenario.retirementAge > 70) {
        errors.push('Retirement age must be between 40 and 70.');
    }

    if (Number.isFinite(scenario.age) && Number.isFinite(scenario.retirementAge) && scenario.retirementAge <= scenario.age) {
        errors.push('Retirement age must be greater than current age.');
    }

    if (!Number.isFinite(scenario.contribution) || scenario.contribution < 500 || scenario.contribution > 200000) {
        errors.push('Monthly contribution must be between ₹500 and ₹2,00,000.');
    }

    if (!validRiskProfiles.includes(scenario.riskProfile)) {
        errors.push('Risk profile must be conservative, moderate, or aggressive.');
    }

    return {
        isValid: errors.length === 0,
        errors
    };
}

function syncScenarioState(scenario) {
    AppState.currentScenario = {
        age: scenario.age,
        retirementAge: scenario.retirementAge,
        contribution: scenario.contribution,
        riskProfile: scenario.riskProfile
    };
}

function attachEventListeners() {
    console.log('📋 Attaching event listeners...');

    const projectionForm = ensureProjectionForm();

    if (!projectionForm) {
        showError('Input form could not be initialized. Please refresh the page.');
        return;
    }

    // Form inputs
    const ageInput = document.getElementById('age-input');
    const retirementAgeInput = document.getElementById('retirement-age-input');
    const riskSelect = document.getElementById('risk-profile-select');
    const slider = document.getElementById('contribution-slider');

    const scheduleAutoCalculate = createDebouncer(() => {
        const scenario = getScenarioFromDom();
        const validation = validateScenarioInput(scenario);

        if (!validation.isValid) {
            console.warn('⏭️ Auto-calculate skipped due to validation errors:', validation.errors);
            return;
        }

        syncScenarioState(scenario);
        updateSliderDisplay(scenario.contribution);
        calculateProjection({ trigger: 'auto-change' });
    }, CONFIG.DEBOUNCE_DELAY);

    AppState.pendingAutoCalculate = scheduleAutoCalculate;

    // Fix: single authoritative submit handler for user calculation action.
    projectionForm.addEventListener('submit', (event) => {
        event.preventDefault();
        console.log('📝 Projection form submit captured.');

        if (AppState.pendingAutoCalculate?.cancel) {
            AppState.pendingAutoCalculate.cancel();
        }

        const scenario = getScenarioFromDom();
        const validation = validateScenarioInput(scenario);

        if (!validation.isValid) {
            const combined = validation.errors.join(' ');
            console.error('❌ Form validation failed on submit:', {
                errors: validation.errors,
                scenario
            });
            showError(combined);
            return;
        }

        syncScenarioState(scenario);
        calculateProjection({ trigger: 'submit' }).then((success) => {
            if (success) {
                console.log('→ Advancing to step 3 (Results) after successful submit');
                advanceToNextStep(3);
            }
        });
    });

    if (ageInput) {
        ageInput.addEventListener('change', () => {
            console.log('Age changed:', ageInput.value);
            scheduleAutoCalculate();
        });
    } else {
        console.warn('⚠️ Age input not found');
    }

    if (retirementAgeInput) {
        retirementAgeInput.addEventListener('change', () => {
            console.log('Retirement age changed:', retirementAgeInput.value);
            scheduleAutoCalculate();
        });
    } else {
        console.warn('⚠️ Retirement age input not found');
    }

    if (riskSelect) {
        riskSelect.addEventListener('change', () => {
            console.log('Risk profile changed:', riskSelect.value);
            scheduleAutoCalculate();
        });
    } else {
        console.warn('⚠️ Risk profile select not found');
    }

    // Slider updates UI immediately, API call stays debounced.
    if (slider) {
        console.log('✅ Slider found, attaching listener');

        // Ensure slider is interactive
        slider.style.pointerEvents = 'auto';

        slider.addEventListener('input', () => {
            const newValue = parseInt(slider.value);
            console.log('📊 Slider moved to:', newValue);
            updateSliderDisplay(newValue);
            scheduleAutoCalculate();
        });

        // Initial display update
        updateSliderDisplay(parseInt(slider.value));
    } else {
        console.error('❌ CRITICAL: Slider element not found!');
    }

    // Buttons
    const calculateBtn = document.getElementById('calculate-btn');
    if (calculateBtn) {
        console.log('✅ Calculate button found');
        calculateBtn.addEventListener('click', () => {
            console.log('🔘 Calculate button clicked (submit will handle request).');
        });
    } else {
        console.error('❌ CRITICAL: Calculate button not found!');
    }

    const compareBtn = document.getElementById('compare-btn');
    if (compareBtn) {
        console.log('✅ Compare button found');
        compareBtn.addEventListener('click', (e) => {
            console.log('🔘 Compare button clicked');
            e.preventDefault();
            if (AppState.pendingAutoCalculate?.cancel) {
                AppState.pendingAutoCalculate.cancel();
            }
            compareScenarios();
            // Advance to comparison step
            console.log('→ Advancing to step 4 (Comparison)');
            advanceToNextStep(4);
        });
    } else {
        console.error('❌ CRITICAL: Compare button not found!');
    }

    const compareAfterCalcBtn = document.getElementById('compare-after-calc-btn');
    if (compareAfterCalcBtn) {
        console.log('✅ Compare-after-calculation button found');
        compareAfterCalcBtn.addEventListener('click', (e) => {
            console.log('🔘 Compare-after-calculation button clicked');
            e.preventDefault();
            if (AppState.pendingAutoCalculate?.cancel) {
                AppState.pendingAutoCalculate.cancel();
            }
            compareScenarios();
            console.log('→ Advancing to step 4 (Comparison) from results panel');
            advanceToNextStep(4);
        });
    } else {
        console.warn('⚠️ Compare-after-calculation button not found in results panel');
    }

    console.log('✅ Event listeners attached successfully');
}

// ==================== SLIDER DISPLAY ====================

function updateSliderDisplay(value) {
    const valueDisplay = document.getElementById('slider-value');
    const deltaDisplay = document.getElementById('slider-delta');

    if (valueDisplay) {
        const formatted = new Intl.NumberFormat('en-IN').format(value);
        valueDisplay.textContent = formatted;
    }

    if (deltaDisplay) {
        const original = 10000;
        const delta = value - original;
        if (delta === 0) {
            deltaDisplay.textContent = '';
        } else if (delta > 0) {
            deltaDisplay.textContent = `+${new Intl.NumberFormat('en-IN').format(delta)}`;
            deltaDisplay.className = 'slider-delta positive';
        } else {
            deltaDisplay.textContent = new Intl.NumberFormat('en-IN').format(delta);
            deltaDisplay.className = 'slider-delta negative';
        }
    }
}

// ==================== API CALLS ====================

function getProjectionPayload() {
    return {
        current_age: AppState.currentScenario.age,
        retirement_age: AppState.currentScenario.retirementAge,
        monthly_contribution: AppState.currentScenario.contribution,
        risk_profile: AppState.currentScenario.riskProfile,
        annual_income_growth: 5.0
    };
}

function getProjectionRequestKey(payload) {
    return JSON.stringify(payload);
}

// Fix: submission path uses duplicate-request protection and detailed error logging.
async function calculateProjection({ trigger = 'unknown' } = {}) {
    const payload = getProjectionPayload();
    const requestKey = getProjectionRequestKey(payload);

    if (AppState.activeProjectionPromise && AppState.activeProjectionRequestKey === requestKey) {
        console.warn('⛔ Duplicate projection request prevented.', { trigger, requestKey });
        return false;
    }

    if (AppState.isLoading) {
        console.warn('⏳ Calculation ignored because another request is in progress.', { trigger });
        return false;
    }

    console.log('💬 Calculating projection with scenario:', {
        trigger,
        scenario: AppState.currentScenario,
        payload
    });
    setLoadingState(true);

    AppState.activeProjectionRequestKey = requestKey;
    AppState.activeProjectionPromise = (async () => {
        try {
            const url = buildApiUrl(CONFIG.PROJECTION_ENDPOINT);
            console.log('📤 API Request:', { method: 'POST', url, payload });

            const response = await axios.post(url, payload, { timeout: CONFIG.API_TIMEOUT });

            console.log('✅ API Response received:', response.data);
            const data = response.data;

            updateDashboard(data);
            updateChart(data);
            console.log('🏆 Calculation and chart update complete!');
            return true;

        } catch (error) {
            console.error('❌ Calculation Error Details:', {
                trigger,
                message: error.message,
                code: error.code,
                status: error.response?.status,
                statusText: error.response?.statusText,
                data: error.response?.data,
                url: error.config?.url,
                payload
            });

            let errorMsg = 'Failed to calculate projection. Please try again.';
            if (error.code === 'ECONNABORTED') {
                errorMsg = 'Request timeout. Backend may not be running.';
            } else if (error.code === 'ERR_NETWORK' || error.message?.includes('Network')) {
                errorMsg = 'Cannot connect to backend. Is backend running on port 8000?';
            } else if (error.response?.status === 404) {
                errorMsg = 'API endpoint not found at /api/v1/projections/calculate.';
            } else if (error.response?.data?.detail) {
                errorMsg = `Backend error: ${error.response.data.detail}`;
            }

            showError(errorMsg);
            return false;
        } finally {
            setLoadingState(false);
            AppState.activeProjectionPromise = null;
            AppState.activeProjectionRequestKey = null;
        }

    })();

    return AppState.activeProjectionPromise;
}

async function compareScenarios() {
    if (AppState.isLoading) return;

    console.log('🔄 Comparing scenarios...');
    setLoadingState(true);

    try {
        const scenarios = [
            { ...AppState.currentScenario, contribution: 5000 },
            { ...AppState.currentScenario, contribution: 15000 },
            { ...AppState.currentScenario, contribution: 25000 }
        ];

        console.log('📊 Running', scenarios.length, 'scenario calculations');

        const settledResults = await Promise.allSettled(
            scenarios.map((scenario, idx) => {
                console.log(`  Scenario ${idx + 1}: ₹${scenario.contribution.toLocaleString('en-IN')}`);
                return axios.post(
                    buildApiUrl(CONFIG.PROJECTION_ENDPOINT),
                    {
                        current_age: scenario.age,
                        retirement_age: scenario.retirementAge,
                        monthly_contribution: scenario.contribution,
                        risk_profile: scenario.riskProfile,
                        annual_income_growth: 5.0
                    },
                    { timeout: CONFIG.API_TIMEOUT }
                );
            })
        );

        const successfulResults = [];
        const successfulScenarios = [];
        const failedResults = [];

        settledResults.forEach((result, index) => {
            if (result.status === 'fulfilled') {
                successfulResults.push(result.value.data);
                successfulScenarios.push(scenarios[index]);
            } else {
                failedResults.push({
                    scenarioIndex: index + 1,
                    contribution: scenarios[index].contribution,
                    reason: result.reason?.message || 'Unknown error',
                    status: result.reason?.response?.status,
                    detail: result.reason?.response?.data?.detail
                });
            }
        });

        if (failedResults.length > 0) {
            console.error('⚠️ Some scenario comparisons failed:', failedResults);
        }

        if (successfulResults.length === 0) {
            populateComparisonTable([], []);
            showError('Unable to fetch comparison data. Please verify backend API is running and retry.');
            return;
        }

        console.log('✅ Scenario comparison complete:', {
            successful: successfulResults.length,
            failed: failedResults.length
        });

        populateComparisonTable(successfulResults, successfulScenarios);

    } catch (error) {
        console.error('❌ Comparison Error:', {
            message: error.message,
            code: error.code,
            status: error.response?.status,
            detail: error.response?.data?.detail,
            url: error.config?.url
        });
        let errorMsg = 'Failed to compare scenarios. Please try again.';
        if (error.message.includes('Network')) {
            errorMsg = 'Cannot connect to backend. Is backend running on port 8000?';
        } else if (error.response?.status === 404) {
            errorMsg = 'Comparison endpoint not found. Please check backend routes.';
        }
        showError(errorMsg);
    } finally {
        setLoadingState(false);
    }
}

async function fetchApiVersion() {
    try {
        const response = await axios.get(
            buildApiUrl(CONFIG.HEALTH_ENDPOINT),
            { timeout: 5000 }
        );
        const versionEl = document.getElementById('api-version');
        if (versionEl) {
            versionEl.textContent = `Version: ${response.data.version || 'Unknown'}`;
        }
    } catch (error) {
        console.log('API version fetch failed');
    }
}

// ==================== DASHBOARD UPDATE ====================

function updateDashboard(data) {
    // Extract values from backend response format
    const corpusValue = data.corpus_projection?.percentile_50 || data.retirement_corpus || 0;
    const monthlyValue = data.pension_estimate?.monthly_pension_50th || data.monthly_pension || 0;
    const lumpsumValue = data.pension_estimate?.lump_sum_amount || data.lump_sum || 0;

    // Update KPI cards with animation
    animateKPIValue('.kpi-card[data-kpi="corpus"] .kpi-number', corpusValue);
    animateKPIValue('.kpi-card[data-kpi="monthly"] .kpi-number', Math.floor(monthlyValue));
    animateKPIValue('.kpi-card[data-kpi="lumpsum"] .kpi-number', Math.floor(lumpsumValue));
    animateKPIValue('.kpi-card[data-kpi="years"] .kpi-number', AppState.currentScenario.retirementAge - AppState.currentScenario.age);

    updateProjectionExplanation(data);
}

function updateProjectionExplanation(data) {
    const explanationEl = document.getElementById('calculation-explanation');
    if (!explanationEl) return;

    const formatMoney = (value) => `₹${new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(Math.max(0, value || 0))}`;

    const years = AppState.currentScenario.retirementAge - AppState.currentScenario.age;
    const p10 = data.corpus_projection?.percentile_10 || 0;
    const p50 = data.corpus_projection?.percentile_50 || 0;
    const p90 = data.corpus_projection?.percentile_90 || 0;
    const totalContributions = data.total_contributions || 0;

    const annuityAmount = data.pension_estimate?.annuity_purchase_amount || (p50 * 0.4);
    const lumpSumAmount = data.pension_estimate?.lump_sum_amount || (p50 * 0.4);
    const monthlyPension = data.pension_estimate?.monthly_pension_50th || 0;
    const derivedAnnuityRate = annuityAmount > 0 ? ((monthlyPension * 12) / annuityAmount) * 100 : 0;

    explanationEl.innerHTML = `
        <h3>How these values are calculated</h3>
        <ul>
            <li>Inputs used: age ${AppState.currentScenario.age}, retirement age ${AppState.currentScenario.retirementAge}, contribution ${formatMoney(AppState.currentScenario.contribution)}/month, risk profile ${AppState.currentScenario.riskProfile}.</li>
            <li>Investment horizon: ${years} years. Total estimated contributions (with income growth): ${formatMoney(totalContributions)}.</li>
            <li>Monte Carlo simulation output (10th / 50th / 90th percentile corpus): ${formatMoney(p10)} / ${formatMoney(p50)} / ${formatMoney(p90)}.</li>
            <li>At retirement, corpus split into lump sum ${formatMoney(lumpSumAmount)} and annuity purchase ${formatMoney(annuityAmount)}.</li>
            <li>Monthly pension is derived from annuity corpus: (${formatMoney(annuityAmount)} × ${derivedAnnuityRate.toFixed(2)}%) ÷ 12 = ${formatMoney(monthlyPension)}.</li>
            <li>Chart note: intermediate year points are visual interpolation from 0 to retirement corpus percentiles for readability.</li>
        </ul>
    `;

    explanationEl.style.display = 'block';
}

function animateKPIValue(selector, finalValue) {
    const element = document.querySelector(selector);
    if (!element) return;

    const startValue = 0;
    const duration = 1000;
    const startTime = Date.now();

    const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const currentValue = Math.floor(startValue + (finalValue - startValue) * progress);

        element.textContent = new Intl.NumberFormat('en-IN').format(currentValue);

        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    };

    animate();
}

// ==================== CHART ====================

function initializeChart() {
    const ctx = document.getElementById('projection-chart');
    if (!ctx) return;

    AppState.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Projection (50th Percentile)',
                    data: [],
                    borderColor: '#295b49',
                    backgroundColor: 'rgba(41, 91, 73, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6
                },
                {
                    label: 'Upper Range (90th)',
                    data: [],
                    borderColor: 'rgba(200, 16, 46, 0.3)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                },
                {
                    label: 'Lower Range (10th)',
                    data: [],
                    borderColor: 'rgba(200, 16, 46, 0.3)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: { color: '#333', font: { size: 11 } }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#999' },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    ticks: { color: '#999' },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                }
            }
        }
    });
}

function updateChart(data) {
    if (!AppState.chart) return;

    const years = [];
    const projections = [];
    const upper = [];
    const lower = [];

    // Get the investment horizon
    const investmentYears = AppState.currentScenario.retirementAge - AppState.currentScenario.age;

    // Extract percentile values from backend response
    const p10 = data.corpus_projection?.percentile_10 || 0;
    const p50 = data.corpus_projection?.percentile_50 || 0;
    const p90 = data.corpus_projection?.percentile_90 || 0;

    // Create year labels and linear projection arrays
    for (let i = 0; i <= investmentYears; i++) {
        years.push(AppState.currentScenario.age + i);

        // Linear interpolation from 0 to corpus value at retirement
        const factor = i / investmentYears;
        projections.push(Math.max(0, p50 * factor));
        upper.push(Math.max(0, p90 * factor));
        lower.push(Math.max(0, p10 * factor));
    }

    AppState.chart.data.labels = years;
    AppState.chart.data.datasets[0].data = projections;
    AppState.chart.data.datasets[1].data = upper;
    AppState.chart.data.datasets[2].data = lower;
    AppState.chart.update('none');
}

// ==================== COMPARISON TABLE ====================

function populateComparisonTable(results, scenarios) {
    const tbody = document.getElementById('scenarios-table-body');
    if (!tbody) {
        console.warn('⚠️ Comparison table body not found');
        return;
    }

    if (!Array.isArray(results) || results.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align:center; color:#666; font-weight:500;">
                    No comparison data available yet. Click Compare again after a successful calculation.
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = results.map((data, idx) => {
        const scenario = scenarios[idx];
        const scenarioLabel = idx === 0 ? 'Conservative' : idx === 1 ? 'Standard' : 'Optimistic';

        // Extract values from backend response
        const corpus = data.corpus_projection?.percentile_50 || data.retirement_corpus || 0;
        const pension = data.pension_estimate?.monthly_pension_50th || data.monthly_pension || 0;
        const successRate = data.success_rate || 95;

        return `
      <tr>
        <td>${scenarioLabel}</td>
        <td>₹${new Intl.NumberFormat('en-IN').format(scenario.contribution)}</td>
        <td>${scenario.retirementAge}</td>
        <td>₹${new Intl.NumberFormat('en-IN').format(Math.round(corpus))}</td>
        <td>₹${new Intl.NumberFormat('en-IN').format(Math.round(pension))}</td>
        <td>${successRate.toFixed(1)}%</td>
      </tr>
    `;
    }).join('');

    console.log('✅ Comparison table populated with', results.length, 'scenarios');
}

// ==================== LOADING STATE ====================

function setLoadingState(isLoading) {
    AppState.isLoading = isLoading;

    const calculateBtn = document.getElementById('calculate-btn');
    const compareBtn = document.getElementById('compare-btn');
    const compareAfterCalcBtn = document.getElementById('compare-after-calc-btn');

    [calculateBtn, compareBtn, compareAfterCalcBtn].forEach(btn => {
        if (btn) {
            btn.disabled = isLoading;
            if (!isLoading) {
                const text = btn.id === 'calculate-btn' ? '⚡ Calculate Projection' : '🔄 Compare Scenarios';
                btn.innerHTML = `<span class="btn-icon">${text.split(' ')[0]}</span> ${text.split(' ').slice(1).join(' ')}`;
            }
        }
    });
}

// ==================== ERROR HANDLING ====================

function showError(message) {
    console.error('🚨 UI Error:', message);

    const modal = document.getElementById('error-modal');
    const errorMsg = document.getElementById('error-message');

    if (modal && errorMsg) {
        errorMsg.textContent = message;
        modal.style.display = 'flex';
        return;
    }

    let alertEl = document.getElementById('inline-error-alert');
    if (!alertEl) {
        alertEl = document.createElement('div');
        alertEl.id = 'inline-error-alert';
        alertEl.style.margin = '12px 0';
        alertEl.style.padding = '10px 12px';
        alertEl.style.borderRadius = '8px';
        alertEl.style.background = 'rgba(200,16,46,0.08)';
        alertEl.style.border = '1px solid rgba(200,16,46,0.3)';
        alertEl.style.color = '#7f1023';

        const panel = document.querySelector('[data-pipeline-step="1"] .panel-header');
        if (panel) {
            panel.insertAdjacentElement('afterend', alertEl);
        } else {
            document.body.prepend(alertEl);
        }
    }

    alertEl.textContent = message;
}

document.addEventListener('click', (e) => {
    if (e.target.matches('.modal-close, .modal-overlay')) {
        const modal = e.closest('.modal');
        if (modal) modal.style.display = 'none';
    }
});

// ==================== UTILITIES ====================

// ==================== ENHANCED INTERACTIONS ====================

// Initialize smooth link transitions
function initializeLinkEnhancements() {
    document.querySelectorAll('a:not([target="_blank"])').forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href && href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });
}

// Initialize form input focus enhancements
function initializeFormEnhancements() {
    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('focus', function () {
            this.parentElement?.classList?.add('focused');
        });
        input.addEventListener('blur', function () {
            this.parentElement?.classList?.remove('focused');
        });
    });
}

// Call enhancement functions when DOM loads
document.addEventListener('DOMContentLoaded', () => {
    initializeLinkEnhancements();
    initializeFormEnhancements();
}, { once: true });

// ==================== ANIMATION ENHANCEMENTS ====================

// Enhance panel cards with proper reveal animations
function enhancePanelAnimations() {
    const panels = document.querySelectorAll('.panel-card');
    panels.forEach((panel, index) => {
        panel.classList.add('reveal-on-scroll');
        panel.style.setProperty('--reveal-index', index);
    });
}

document.addEventListener('DOMContentLoaded', enhancePanelAnimations, { once: true });

console.log('%c🎯 NPS Retirement Intelligence - Premium Edition',
    'font-size: 14px; font-weight: bold; color: #295b49;');
