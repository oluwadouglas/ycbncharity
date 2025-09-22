/* ===== SDG SECTION ANIMATIONS ===== */
/* Enhanced animations and interactions for the UN SDGs section */

(function() {
    'use strict';
    
    // Initialize SDG animations when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
        initSDGSlider();
        initSDGMarquee();
        initSDGAnimations();
        initScrollReveal();
        initCounterAnimations();
        initParticleEffects();
        initProgressBars();
    });
    
    // Initialize SDG Marquee (continuous scrolling icons/titles)
    function initSDGMarquee() {
        const marquee = document.querySelector('.sdg-marquee');
        const track = marquee ? marquee.querySelector('.sdg-marquee-track') : null;
        if (!marquee || !track) return;

        // Reduce motion support
        const prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        const forced = marquee.getAttribute('data-force-animate') === '1';
        if (prefersReduced && !forced) {
            // Do not animate; allow manual scroll
            track.style.animation = 'none';
            marquee.style.overflowX = 'auto';
            return;
        }

        // Find the inline goals group and duplicate it once for seamless loop
        const groups = track.querySelectorAll('.sdg-goals-inline');
        if (groups.length > 0 && groups.length < 2) {
            const clone = groups[0].cloneNode(true);
            clone.setAttribute('aria-hidden', 'true');
            track.appendChild(clone);
        }

        // Compute animation duration based on content width for consistent speed
        requestAnimationFrame(() => {
            const firstGroup = track.querySelector('.sdg-goals-inline');
            if (!firstGroup) return;
            const contentWidth = firstGroup.scrollWidth; // pixels for one loop
const baseSpeed = 35; // px per second (slower)
            const minDuration = 60; // seconds (ensure slow movement)
            const duration = Math.max(minDuration, Math.round(contentWidth / baseSpeed));
            track.style.animationDuration = duration + 's';
        });

        // Pause/resume on hover and touch
        const pause = () => { track.style.animationPlayState = 'paused'; };
        const resume = () => { track.style.animationPlayState = 'running'; };
        marquee.addEventListener('mouseenter', pause);
        marquee.addEventListener('mouseleave', resume);
        marquee.addEventListener('touchstart', pause, { passive: true });
        marquee.addEventListener('touchend', resume);
    }

    // Initialize SDG Slider
    function initSDGSlider() {
        const sdgSlider = document.getElementById('sdgSlider');
        if (sdgSlider && typeof Swiper !== 'undefined') {
            // Prefer data-slider-options from the DOM if present
            let dataOptions = {};
            try {
                const attr = sdgSlider.getAttribute('data-slider-options');
                if (attr) {
                    dataOptions = JSON.parse(attr);
                }
            } catch (_) { /* ignore parse errors */ }

            const compactDefaults = {
                // Compact defaults to avoid huge inline widths/margins
                loop: false,
                centeredSlides: false,
                autoHeight: false,
                spaceBetween: 6,
                speed: 600,
                navigation: {
                    nextEl: '.sdg-slider-next',
                    prevEl: '.sdg-slider-prev',
                },
                pagination: {
                    el: '.sdg-slider-pagination',
                    clickable: true,
                },
                breakpoints: {
                    0:   { slidesPerView: 2, spaceBetween: 6 },
                    576: { slidesPerView: 3, spaceBetween: 6 },
                    768: { slidesPerView: 4, spaceBetween: 6 },
                    992: { slidesPerView: 5, spaceBetween: 6 },
                    1200:{ slidesPerView: 6, spaceBetween: 6 }
                }
            };

            // Helper to remove Swiper's inline slide sizing so CSS rules win
            function scrubInline(swiper) {
                if (!swiper || !swiper.slides) return;
                swiper.slides.forEach(function (slide) {
                    if (slide && slide.style) {
                        slide.style.width = '';
                        slide.style.marginRight = '';
                    }
                });
            }

            // Merge data options over defaults
            const options = Object.assign({}, compactDefaults, dataOptions);
            // Ensure our scrub runs on lifecycle events
            options.on = Object.assign({}, options.on || {}, {
                init: function () { scrubInline(this); },
                resize: function () { scrubInline(this); },
                update: function () { scrubInline(this); },
                breakpoint: function () { scrubInline(this); },
                slideChange: function () { /* no-op */ }
            });

            const instance = new Swiper('#sdgSlider', options);
            // Final safeguard after init
            scrubInline(instance);
        }
    }
    
    // Main SDG Animation Controller
    function initSDGAnimations() {
        const sdgCards = document.querySelectorAll('.sdg-card, .sdg-detail-card');
        
        sdgCards.forEach((card, index) => {
            // Add hover enhancements
            addHoverEffects(card, index);
            
            // Add click interactions
            addClickEffects(card);
            
            // Add loading animations
            addLoadingAnimation(card, index);
        });
        
        // Add pulsing effect to featured card
        const featuredCard = document.querySelector('.sdg-card-featured');
        if (featuredCard) {
            addFeaturedCardEffects(featuredCard);
        }
    }
    
    // Enhanced Hover Effects
    function addHoverEffects(card, index) {
        const icon = card.querySelector('.sdg-icon, .sdg-detail-icon');
        const background = card.querySelector('.sdg-background');
        
        card.addEventListener('mouseenter', function() {
            // Add bounce animation to icon
            if (icon) {
                icon.style.animation = 'bounceIn 0.6s ease-out';
            }
            
            // Add ripple effect
            createRippleEffect(card);
            
            // Animate background if exists
            if (background) {
                background.style.transform = 'scale(4) rotate(45deg)';
                background.style.opacity = '1';
            }
            
            // Add subtle glow
            card.style.filter = 'drop-shadow(0 0 20px rgba(26, 104, 91, 0.3))';
        });
        
        card.addEventListener('mouseleave', function() {
            // Reset animations
            if (icon) {
                icon.style.animation = '';
            }
            
            if (background) {
                background.style.transform = '';
                background.style.opacity = '';
            }
            
            card.style.filter = '';
        });
    }
    
    // Click Effects with Pulse Animation
    function addClickEffects(card) {
        card.addEventListener('click', function(e) {
            // Create click pulse effect
            createPulseEffect(card, e);
            
            // Add temporary highlight
            card.classList.add('sdg-clicked');
            setTimeout(() => {
                card.classList.remove('sdg-clicked');
            }, 600);
        });
    }
    
    // Loading Animations with Staggered Delays
    function addLoadingAnimation(card, index) {
        // Set initial state
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px) scale(0.8)';
        
        // Animate in with delay
        setTimeout(() => {
            card.style.transition = 'all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0) scale(1)';
        }, 100 + (index * 150));
    }
    
    // Featured Card Special Effects
    function addFeaturedCardEffects(card) {
        // Add subtle pulsing
        setInterval(() => {
            if (!card.matches(':hover')) {
                card.style.animation = 'pulse 2s ease-in-out';
                setTimeout(() => {
                    card.style.animation = '';
                }, 2000);
            }
        }, 8000);
        
        // Add floating particles
        addFloatingParticles(card);
    }
    
    // Scroll Reveal Animation
    function initScrollReveal() {
        const observerOptions = {
            threshold: 0.2,
            rootMargin: '0px 0px -100px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    element.classList.add('animate-on-scroll');
                    
                    // Add special entrance animation
                    if (element.classList.contains('sdg-card')) {
                        animateSDGCard(element);
                    } else if (element.classList.contains('sdg-detail-card')) {
                        animateDetailCard(element);
                    }
                    
                    observer.unobserve(element);
                }
            });
        }, observerOptions);
        
        // Observe all SDG elements
        document.querySelectorAll('.sdg-card, .sdg-detail-card, .sdg-cta, .sdg-footer').forEach(el => {
            observer.observe(el);
        });
    }
    
    // Counter Animations for Numbers
    function initCounterAnimations() {
        const numbers = document.querySelectorAll('.sdg-number, .sdg-detail-icon');
        
        numbers.forEach(number => {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });
            
            observer.observe(number);
        });
    }
    
    // Particle Effects
    function initParticleEffects() {
        const sdgSection = document.querySelector('.sdg-section');
        if (sdgSection) {
            createFloatingDots(sdgSection);
        }
    }
    
    // Progress Bars Animation
    function initProgressBars() {
        // Animate any progress elements that might be added
        const progressElements = document.querySelectorAll('.sdg-progress');
        
        progressElements.forEach(progress => {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateProgress(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.3 });
            
            observer.observe(progress);
        });
    }
    
    // Helper Functions
    function createRippleEffect(element) {
        const ripple = document.createElement('div');
        ripple.className = 'sdg-ripple';
        ripple.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(26, 104, 91, 0.3);
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 1;
            animation: ripple 0.6s linear;
        `;
        
        element.style.position = 'relative';
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
    
    function createPulseEffect(element, event) {
        const pulse = document.createElement('div');
        const rect = element.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        pulse.className = 'sdg-pulse';
        pulse.style.cssText = `
            position: absolute;
            top: ${y}px;
            left: ${x}px;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.8);
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 2;
            animation: pulse 0.5s ease-out;
        `;
        
        element.style.position = 'relative';
        element.appendChild(pulse);
        
        setTimeout(() => {
            pulse.remove();
        }, 500);
    }
    
    function animateSDGCard(card) {
        const icon = card.querySelector('.sdg-icon');
        const number = card.querySelector('.sdg-number');
        const title = card.querySelector('.sdg-title');
        const description = card.querySelector('.sdg-description');
        const btn = card.querySelector('.sdg-btn');
        
        // Staggered animation for card elements
        if (icon) {
            icon.style.animation = 'slideInLeft 0.6s ease-out 0.2s both';
        }
        if (number) {
            number.style.animation = 'slideInRight 0.6s ease-out 0.3s both';
        }
        if (title) {
            title.style.animation = 'fadeInUp 0.6s ease-out 0.4s both';
        }
        if (description) {
            description.style.animation = 'fadeInUp 0.6s ease-out 0.5s both';
        }
        if (btn) {
            btn.style.animation = 'bounceIn 0.6s ease-out 0.6s both';
        }
    }
    
    function animateDetailCard(card) {
        const icon = card.querySelector('.sdg-detail-icon');
        const title = card.querySelector('.sdg-detail-title');
        const text = card.querySelector('.sdg-detail-text');
        
        if (icon) {
            icon.style.animation = 'rotateIn 0.6s ease-out 0.2s both';
        }
        if (title) {
            title.style.animation = 'fadeInLeft 0.6s ease-out 0.3s both';
        }
        if (text) {
            text.style.animation = 'fadeInUp 0.6s ease-out 0.4s both';
        }
    }
    
    function animateCounter(element) {
        const text = element.textContent;
        const number = parseInt(text);
        
        if (!isNaN(number)) {
            let current = 0;
            const increment = number / 30;
            const timer = setInterval(() => {
                current += increment;
                if (current >= number) {
                    current = number;
                    clearInterval(timer);
                }
                element.textContent = Math.floor(current);
            }, 50);
        }
    }
    
    function createFloatingDots(container) {
        for (let i = 0; i < 20; i++) {
            const dot = document.createElement('div');
            dot.className = 'floating-dot';
            dot.style.cssText = `
                position: absolute;
                width: ${Math.random() * 8 + 4}px;
                height: ${Math.random() * 8 + 4}px;
                background: rgba(26, 104, 91, ${Math.random() * 0.3 + 0.1});
                border-radius: 50%;
                top: ${Math.random() * 100}%;
                left: ${Math.random() * 100}%;
                pointer-events: none;
                z-index: 1;
                animation: float ${Math.random() * 6 + 4}s linear infinite;
                animation-delay: ${Math.random() * 2}s;
            `;
            
            container.appendChild(dot);
        }
    }
    
    function addFloatingParticles(element) {
        const particles = [];
        
        for (let i = 0; i < 8; i++) {
            const particle = document.createElement('div');
            particle.className = 'sdg-particle';
            particle.style.cssText = `
                position: absolute;
                width: 6px;
                height: 6px;
                background: rgba(255, 172, 0, 0.6);
                border-radius: 50%;
                top: ${Math.random() * 100}%;
                left: ${Math.random() * 100}%;
                pointer-events: none;
                z-index: 1;
                opacity: 0;
                animation: particleFloat ${Math.random() * 4 + 3}s ease-in-out infinite;
                animation-delay: ${Math.random() * 2}s;
            `;
            
            element.appendChild(particle);
            particles.push(particle);
        }
        
        return particles;
    }
    
    function animateProgress(element) {
        const progressBar = element.querySelector('.progress-bar');
        if (progressBar) {
            const width = progressBar.getAttribute('data-width') || '75%';
            progressBar.style.width = '0%';
            setTimeout(() => {
                progressBar.style.transition = 'width 2s ease-out';
                progressBar.style.width = width;
            }, 100);
        }
    }
    
})();

/* ===== ADDITIONAL CSS ANIMATIONS ===== */
/* These will be injected into the page */

// Add CSS animations dynamically
(function() {
    const style = document.createElement('style');
    style.textContent = `
        /* SDG Click Effect */
        .sdg-clicked {
            transform: translateY(-15px) scale(1.02) !important;
            box-shadow: 
                0 35px 80px rgba(26, 104, 91, 0.25),
                0 15px 40px rgba(0, 0, 0, 0.15) !important;
        }
        
        /* Ripple Animation */
        @keyframes ripple {
            to {
                width: 200px;
                height: 200px;
                opacity: 0;
            }
        }
        
        /* Pulse Animation */
        @keyframes pulse {
            to {
                width: 50px;
                height: 50px;
                opacity: 0;
            }
        }
        
        /* Enhanced Pulse for Featured Card */
        @keyframes pulse {
            0% {
                transform: scale(1);
                box-shadow: 0 15px 50px rgba(26, 104, 91, 0.12);
            }
            50% {
                transform: scale(1.02);
                box-shadow: 0 20px 60px rgba(26, 104, 91, 0.18);
            }
            100% {
                transform: scale(1);
                box-shadow: 0 15px 50px rgba(26, 104, 91, 0.12);
            }
        }
        
        /* Entrance Animations */
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translate3d(-100%, 0, 0);
            }
            to {
                opacity: 1;
                transform: none;
            }
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translate3d(100%, 0, 0);
            }
            to {
                opacity: 1;
                transform: none;
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translate3d(0, 100%, 0);
            }
            to {
                opacity: 1;
                transform: none;
            }
        }
        
        @keyframes fadeInLeft {
            from {
                opacity: 0;
                transform: translate3d(-50px, 0, 0);
            }
            to {
                opacity: 1;
                transform: none;
            }
        }
        
        @keyframes bounceIn {
            0% {
                opacity: 0;
                transform: scale3d(0.3, 0.3, 0.3);
            }
            20% {
                transform: scale3d(1.1, 1.1, 1.1);
            }
            40% {
                transform: scale3d(0.9, 0.9, 0.9);
            }
            60% {
                opacity: 1;
                transform: scale3d(1.03, 1.03, 1.03);
            }
            80% {
                transform: scale3d(0.97, 0.97, 0.97);
            }
            100% {
                opacity: 1;
                transform: scale3d(1, 1, 1);
            }
        }
        
        @keyframes rotateIn {
            from {
                opacity: 0;
                transform: rotate3d(0, 0, 1, -200deg);
            }
            to {
                opacity: 1;
                transform: none;
            }
        }
        
        /* Particle Animation */
        @keyframes particleFloat {
            0% {
                opacity: 0;
                transform: translateY(20px) scale(0);
            }
            20% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
            80% {
                opacity: 1;
                transform: translateY(-20px) scale(1);
            }
            100% {
                opacity: 0;
                transform: translateY(-40px) scale(0);
            }
        }
        
        /* Enhanced Float Animation for Dots */
        @keyframes float {
            0%, 100% {
                transform: translateY(0px) translateX(0px) rotate(0deg);
                opacity: 0.3;
            }
            25% {
                transform: translateY(-15px) translateX(5px) rotate(90deg);
                opacity: 0.6;
            }
            50% {
                transform: translateY(-10px) translateX(-5px) rotate(180deg);
                opacity: 1;
            }
            75% {
                transform: translateY(-20px) translateX(3px) rotate(270deg);
                opacity: 0.6;
            }
        }
        
        /* Loading Shimmer Effect */
        @keyframes shimmer {
            0% {
                background-position: -1000px 0;
            }
            100% {
                background-position: 1000px 0;
            }
        }
        
        .sdg-loading {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 1000px 100%;
            animation: shimmer 2s infinite;
        }
        
        /* Accessibility - Respect reduced motion preference */
        @media (prefers-reduced-motion: reduce) {
            .sdg-card,
            .sdg-detail-card,
            .sdg-icon,
            .sdg-number,
            .sdg-btn,
            .floating-dot,
            .sdg-particle {
                animation: none !important;
                transition: none !important;
            }
            
            .sdg-card:hover,
            .sdg-detail-card:hover {
                transform: none !important;
            }
        }
        
        /* High performance mode for low-end devices */
        @media (max-width: 576px) and (max-resolution: 150dpi) {
            .floating-dot,
            .sdg-particle {
                display: none;
            }
            
            .sdg-card,
            .sdg-detail-card {
                transition-duration: 0.2s;
            }
        }
    `;
    
    document.head.appendChild(style);
})();

/* ===== EXPORT FOR MODULE SYSTEMS ===== */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initSDGAnimations,
        initScrollReveal,
        initCounterAnimations,
        initParticleEffects,
        initProgressBars
    };
}
