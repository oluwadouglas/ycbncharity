/**
 * Spotlight Page Animations and Interactions
 * ==========================================
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all animations and interactions
    initScrollAnimations();
    initSmoothScrolling();
    initCardHoverEffects();
    
    // Initialize after a short delay to ensure DOM is fully loaded
    setTimeout(() => {
        initPerformanceCounters();
    }, 500);
});

/**
 * Scroll-triggered animations
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    // Create intersection observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-up');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe all animated elements
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Smooth scrolling for anchor links
 */
function initSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Skip if it's just "#"
            if (href === '#') return;
            
            const targetElement = document.querySelector(href);
            if (targetElement) {
                e.preventDefault();
                
                // Calculate offset for fixed header
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Enhanced card hover effects
 */
function initCardHoverEffects() {
    const spotlightCards = document.querySelectorAll('.spotlight-item-card');
    const statCards = document.querySelectorAll('.spotlight-stat-card');
    
    // Spotlight item cards
    spotlightCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            
            // Add subtle glow effect to featured items
            if (this.classList.contains('featured-item')) {
                this.style.boxShadow = '0 20px 40px rgba(255, 193, 7, 0.4)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
    
    // Stat cards
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const bgElement = this.querySelector('.stat-card-bg');
            if (bgElement) {
                bgElement.style.opacity = '1';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            const bgElement = this.querySelector('.stat-card-bg');
            if (bgElement) {
                bgElement.style.opacity = '0';
            }
        });
    });
}

/**
 * Performance score counters with animation
 */
function initPerformanceCounters() {
    const scoreElements = document.querySelectorAll('.score-value');
    
    scoreElements.forEach(element => {
        const scoreText = element.textContent;
        const scoreMatch = scoreText.match(/(\d+)/);
        
        if (scoreMatch) {
            const targetScore = parseInt(scoreMatch[1]);
            animateScore(element, targetScore, scoreText);
        }
    });
}

/**
 * Animate score counting
 */
function animateScore(element, targetScore, originalText) {
    let currentScore = 0;
    const increment = Math.ceil(targetScore / 30); // Animation duration control
    const timer = setInterval(() => {
        currentScore += increment;
        if (currentScore >= targetScore) {
            currentScore = targetScore;
            clearInterval(timer);
        }
        
        // Update the text while preserving the format
        element.textContent = originalText.replace(/\d+/, currentScore);
    }, 50);
}

/**
 * Parallax effect for hero section
 */
function initParallaxEffect() {
    const heroSection = document.querySelector('.hero-wrapper');
    if (!heroSection) return;
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        
        if (scrolled < window.innerHeight) {
            heroSection.style.transform = `translateY(${rate}px)`;
        }
    });
}

/**
 * Dynamic background colors for categories
 */
function initDynamicBackgrounds() {
    const categoryElements = document.querySelectorAll('[data-category-color]');
    
    categoryElements.forEach(element => {
        const color = element.getAttribute('data-category-color');
        if (color) {
            element.style.setProperty('--category-color', color);
        }
    });
}

/**
 * Contact link hover effects
 */
function initContactLinkEffects() {
    const contactLinks = document.querySelectorAll('.contact-link');
    
    contactLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.1)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

/**
 * Featured badge animation
 */
function initFeaturedBadgeAnimation() {
    const featuredBadges = document.querySelectorAll('.featured-badge');
    
    featuredBadges.forEach(badge => {
        // Add a subtle pulse animation
        setInterval(() => {
            badge.style.transform = 'scale(1.05)';
            setTimeout(() => {
                badge.style.transform = 'scale(1)';
            }, 200);
        }, 3000);
    });
}

/**
 * Performance badge color animation
 */
function initPerformanceBadgeEffects() {
    const performanceBadges = document.querySelectorAll('.performance-badge');
    
    performanceBadges.forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.3)';
        });
        
        badge.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
}

/**
 * Stagger animation for cards in the same row
 */
function initStaggeredAnimations() {
    const cardRows = document.querySelectorAll('.row');
    
    cardRows.forEach(row => {
        const cards = row.querySelectorAll('.spotlight-item-card, .spotlight-stat-card');
        
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
    });
}

/**
 * Initialize all effects after DOM is ready
 */
function initAllEffects() {
    initParallaxEffect();
    initDynamicBackgrounds();
    initContactLinkEffects();
    initFeaturedBadgeAnimation();
    initPerformanceBadgeEffects();
    initStaggeredAnimations();
}

// Initialize additional effects
document.addEventListener('DOMContentLoaded', initAllEffects);

/**
 * Utility function to check if element is in viewport
 */
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

/**
 * Debounce function for performance optimization
 */
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}
