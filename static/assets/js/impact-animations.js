/**
 * Impact Page Animations and Interactions
 * Handles counter animations, scroll effects, and dynamic styling
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all animations and interactions
    initializeCounters();
    initializeScrollAnimations();
    initializeCustomColors();
    initializeSmoothScrolling();
    initializeHighlightFallback();
    
    /**
     * Initialize counter animations
     */
    function initializeCounters() {
        const counters = document.querySelectorAll('.counter-number');
        const observerOptions = {
            threshold: 0.5,
            rootMargin: '0px 0px -100px 0px'
        };
        
        const counterObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }
    
    /**
     * Animate individual counter
     */
    function animateCounter(element) {
        const target = parseInt(element.dataset.target);
        const prefix = element.dataset.prefix || '';
        const suffix = element.dataset.suffix || '';
        const duration = 2000; // 2 seconds
        const increment = target / (duration / 16); // 60fps
        
        let current = 0;
        const card = element.closest('.counter-card');
        
        // Add counting class for animations
        element.classList.add('counting');
        card.classList.add('counting');
        
        const timer = setInterval(() => {
            current += increment;
            
            if (current >= target) {
                current = target;
                clearInterval(timer);
                
                // Remove counting class and add completed
                element.classList.remove('counting');
                card.classList.remove('counting');
                card.classList.add('completed');
                
                // Remove completed class after animation
                setTimeout(() => {
                    card.classList.remove('completed');
                }, 3000);
            }
            
            // Format number based on size
            let displayNumber = Math.floor(current);
            if (target >= 1000000) {
                displayNumber = (displayNumber / 1000000).toFixed(1) + 'M';
            } else if (target >= 1000) {
                displayNumber = (displayNumber / 1000).toFixed(1) + 'K';
            }
            
            element.textContent = prefix + displayNumber + suffix;
        }, 16);
    }
    
    /**
     * Initialize scroll animations for content sections
     */
    function initializeScrollAnimations() {
        const animatedElements = document.querySelectorAll('.impact-content, .impact-img, .counter-card, .highlight-item, .metric-item, .impact-story-card, .floating-stat-card');
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const scrollObserver = new IntersectionObserver(function(entries) {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('animate-on-scroll', 'animate');
                        
                        // Add specific animation classes based on position
                        if (entry.target.classList.contains('impact-content')) {
                            entry.target.classList.add('animate-fade-left');
                        } else if (entry.target.classList.contains('impact-img')) {
                            entry.target.classList.add('animate-fade-right');
                        } else {
                            entry.target.classList.add('animate-fade-up');
                        }
                    }, index * 100); // Stagger animations
                    
                    scrollObserver.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        animatedElements.forEach(element => {
            scrollObserver.observe(element);
        });
    }
    
    /**
     * Apply custom colors to counter cards
     */
    function initializeCustomColors() {
        const counterCards = document.querySelectorAll('.counter-card[data-color]');
        
        counterCards.forEach(card => {
            const color = card.dataset.color;
            if (color && color !== '#1A685B') {
                card.style.setProperty('--counter-color', color);
                
                // Create gradient variations
                const rgbColor = hexToRgb(color);
                if (rgbColor) {
                    const gradientColor = `linear-gradient(135deg, ${color} 0%, ${darkenColor(color, 20)} 100%)`;
                    const lightColor = `${color}20`; // 20% opacity
                    
                    card.style.setProperty('--counter-color', gradientColor);
                    card.querySelector('.counter-card-bg').style.background = lightColor;
                }
            }
        });
    }
    
    /**
     * Initialize highlight items fallback - ensure they're visible even if IntersectionObserver fails
     */
    function initializeHighlightFallback() {
        // Find all highlight items that have animate-on-scroll class
        const highlightItems = document.querySelectorAll('.highlight-item.animate-on-scroll');
        
        console.log(`Found ${highlightItems.length} highlight items for fallback animation`);
        
        highlightItems.forEach((item, index) => {
            // Add a fallback timeout to make items visible if intersection observer doesn't work
            setTimeout(() => {
                if (!item.classList.contains('animate')) {
                    console.log(`Adding fallback animation to highlight item ${index + 1}`);
                    item.classList.add('animate');
                }
            }, 1000 + (index * 200)); // Stagger the fallback animations
        });
    }
    
    /**
     * Initialize smooth scrolling for anchor links
     */
    function initializeSmoothScrolling() {
        const anchorLinks = document.querySelectorAll('a[href^="#"]');
        
        anchorLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    e.preventDefault();
                    
                    const offsetTop = targetElement.offsetTop - 100; // Account for fixed header
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    /**
     * Add hover effects for counter cards
     */
    function initializeHoverEffects() {
        const counterCards = document.querySelectorAll('.counter-card');
        
        counterCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                // Add subtle bounce effect
                this.style.transform = 'translateY(-10px) scale(1.02)';
                
                // Trigger icon rotation
                const icon = this.querySelector('.counter-card-icon');
                if (icon) {
                    icon.style.transform = 'scale(1.1) rotate(5deg)';
                }
            });
            
            card.addEventListener('mouseleave', function() {
                // Reset transforms
                this.style.transform = '';
                
                const icon = this.querySelector('.counter-card-icon');
                if (icon) {
                    icon.style.transform = '';
                }
            });
        });
    }
    
    /**
     * Utility function to convert hex to RGB
     */
    function hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }
    
    /**
     * Utility function to darken a color
     */
    function darkenColor(hex, percent) {
        const rgb = hexToRgb(hex);
        if (!rgb) return hex;
        
        const factor = (100 - percent) / 100;
        const r = Math.round(rgb.r * factor);
        const g = Math.round(rgb.g * factor);
        const b = Math.round(rgb.b * factor);
        
        return `rgb(${r}, ${g}, ${b})`;
    }
    
    /**
     * Add parallax effect to hero section
     */
    function initializeParallax() {
        const heroSection = document.querySelector('.th-hero-wrapper');
        
        if (heroSection) {
            window.addEventListener('scroll', function() {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.5;
                
                heroSection.style.transform = `translateY(${rate}px)`;
            });
        }
    }
    
    /**
     * Initialize loading states
     */
    function initializeLoadingStates() {
        const counterCards = document.querySelectorAll('.counter-card');
        
        // Add loading state initially
        counterCards.forEach(card => {
            card.classList.add('loading');
        });
        
        // Remove loading state after a delay
        setTimeout(() => {
            counterCards.forEach(card => {
                card.classList.remove('loading');
            });
        }, 500);
    }
    
    /**
     * Add click-to-animate functionality for counters
     */
    function initializeClickToAnimate() {
        const counterCards = document.querySelectorAll('.counter-card');
        
        counterCards.forEach(card => {
            card.addEventListener('click', function() {
                const counter = this.querySelector('.counter-number');
                if (counter && !counter.classList.contains('counting')) {
                    // Reset counter
                    const prefix = counter.dataset.prefix || '';
                    const suffix = counter.dataset.suffix || '';
                    counter.textContent = prefix + '0' + suffix;
                    
                    // Re-animate
                    setTimeout(() => {
                        animateCounter(counter);
                    }, 100);
                }
            });
        });
    }
    
    /**
     * Initialize responsive behavior
     */
    function initializeResponsive() {
        function handleResize() {
            const isMobile = window.innerWidth <= 768;
            const counterCards = document.querySelectorAll('.counter-card');
            
            counterCards.forEach(card => {
                if (isMobile) {
                    card.classList.add('mobile');
                } else {
                    card.classList.remove('mobile');
                }
            });
        }
        
        handleResize();
        window.addEventListener('resize', handleResize);
    }
    
    // Initialize additional features
    initializeHoverEffects();
    initializeParallax();
    initializeLoadingStates();
    initializeClickToAnimate();
    initializeResponsive();
    
    // Add custom event for external counter triggering
    window.triggerCounterAnimation = function(counterId) {
        const counter = document.getElementById(counterId);
        if (counter) {
            animateCounter(counter);
        }
    };
    
    // Performance optimization: Debounce scroll events
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Apply debouncing to scroll-heavy functions
    const debouncedParallax = debounce(initializeParallax, 10);
    window.addEventListener('scroll', debouncedParallax);
    
    /**
     * Initialize homepage-specific impact highlights animations
     */
    function initializeHomepageImpactAnimations() {
        // Target the impact highlights section on homepage
        const impactSection = document.querySelector('.impact-highlights-section');
        if (!impactSection) return;
        
        console.log('Initializing homepage impact highlights animations');
        
        // Initialize floating animations for highlight cards
        initializeFloatingCards();
        
        // Initialize text typewriter effects
        initializeTypewriterEffect();
        
        // Initialize progressive image loading
        initializeProgressiveImages();
        
        // Initialize enhanced hover interactions
        initializeEnhancedHovers();
    }
    
    /**
     * Initialize floating animation for impact cards
     */
    function initializeFloatingCards() {
        const impactCards = document.querySelectorAll('.impact-highlight-card, .impact-story-card');
        
        impactCards.forEach((card, index) => {
            // Add floating animation with different delays
            card.style.animationDelay = `${index * 0.5}s`;
            card.classList.add('floating-card');
            
            // Add mouse follow effect
            card.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(20px)`;
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
            });
        });
    }
    
    /**
     * Initialize typewriter effect for impact section titles
     */
    function initializeTypewriterEffect() {
        const typewriterElements = document.querySelectorAll('.impact-highlights-section .typewriter');
        
        typewriterElements.forEach((element, index) => {
            const text = element.textContent;
            element.textContent = '';
            
            // Observe when element comes into view
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        typewriterAnimation(entry.target, text, 50);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });
            
            observer.observe(element);
        });
    }
    
    /**
     * Typewriter animation function
     */
    function typewriterAnimation(element, text, speed) {
        let i = 0;
        element.style.borderRight = '2px solid var(--theme-color, #1f8a70)';
        
        function typeChar() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(typeChar, speed);
            } else {
                // Remove cursor after completion
                setTimeout(() => {
                    element.style.borderRight = 'none';
                }, 1000);
            }
        }
        
        typeChar();
    }
    
    /**
     * Initialize progressive image loading with fade-in effect
     */
    function initializeProgressiveImages() {
        const images = document.querySelectorAll('.impact-highlights-section img');
        
        images.forEach(img => {
            img.style.opacity = '0';
            img.style.transition = 'opacity 0.6s ease-in-out';
            
            if (img.complete) {
                img.style.opacity = '1';
            } else {
                img.addEventListener('load', function() {
                    this.style.opacity = '1';
                });
                
                // Fallback for loading errors
                img.addEventListener('error', function() {
                    this.style.opacity = '0.3';
                });
            }
        });
    }
    
    /**
     * Initialize enhanced hover interactions for impact elements
     */
    function initializeEnhancedHovers() {
        const hoverElements = document.querySelectorAll(
            '.impact-highlights-section .impact-metric, ' +
            '.impact-highlights-section .impact-stat, ' +
            '.impact-highlights-section .highlight-item'
        );
        
        hoverElements.forEach(element => {
            element.addEventListener('mouseenter', function() {
                // Create ripple effect
                createRippleEffect(this, event);
                
                // Scale animation
                this.style.transform = 'scale(1.05)';
                this.style.zIndex = '10';
                
                // Glow effect
                this.style.boxShadow = '0 10px 30px rgba(31, 138, 112, 0.3)';
            });
            
            element.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.zIndex = '';
                this.style.boxShadow = '';
            });
        });
    }
    
    /**
     * Create ripple effect on click/hover
     */
    function createRippleEffect(element, event) {
        const ripple = document.createElement('span');
        ripple.classList.add('ripple-effect');
        
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        // Remove ripple after animation
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }
    
    /**
     * Initialize magnetic cursor effect for interactive elements
     */
    function initializeMagneticCursor() {
        const magneticElements = document.querySelectorAll(
            '.impact-highlights-section .th-btn, ' +
            '.impact-highlights-section .impact-cta'
        );
        
        magneticElements.forEach(element => {
            element.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                
                // Magnetic effect - move element slightly towards cursor
                this.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px)`;
            });
            
            element.addEventListener('mouseleave', function() {
                this.style.transform = 'translate(0, 0)';
            });
        });
    }
    
    /**
     * Initialize scroll-triggered counter animations for impact metrics
     */
    function initializeScrollTriggeredCounters() {
        const impactCounters = document.querySelectorAll('.impact-highlights-section .counter-number, .impact-highlights-section .impact-number');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.dataset.animated) {
                    entry.target.dataset.animated = 'true';
                    
                    // Enhanced counter animation with custom easing
                    animateImpactCounter(entry.target);
                    
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.7, rootMargin: '-50px' });
        
        impactCounters.forEach(counter => {
            observer.observe(counter);
        });
    }
    
    /**
     * Enhanced counter animation with easing
     */
    function animateImpactCounter(element) {
        const target = parseInt(element.dataset.target || element.dataset.count || element.textContent.replace(/[^\d]/g, ''));
        const prefix = element.dataset.prefix || '';
        const suffix = element.dataset.suffix || '';
        const duration = 2500; // 2.5 seconds for smoother animation
        
        let start = null;
        
        // Easing function - ease-out-cubic
        function easeOutCubic(t) {
            return 1 - Math.pow(1 - t, 3);
        }
        
        function animate(timestamp) {
            if (!start) start = timestamp;
            const progress = Math.min((timestamp - start) / duration, 1);
            const easedProgress = easeOutCubic(progress);
            
            const current = Math.floor(target * easedProgress);
            
            // Format number
            let displayNumber = current;
            if (target >= 1000000) {
                displayNumber = (current / 1000000).toFixed(1) + 'M';
            } else if (target >= 1000) {
                displayNumber = (current / 1000).toFixed(1) + 'K';
            }
            
            element.textContent = prefix + displayNumber + suffix;
            
            // Add visual feedback
            element.style.color = `hsl(${160 + (progress * 20)}, 70%, 45%)`; // Color transition
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                // Reset color and add completion effect
                element.style.color = '';
                element.classList.add('counter-completed');
                
                // Pulse effect on completion
                element.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    element.style.transform = 'scale(1)';
                }, 200);
            }
        }
        
        requestAnimationFrame(animate);
    }
    
    // Initialize homepage-specific animations
    initializeHomepageImpactAnimations();
    initializeMagneticCursor();
    initializeScrollTriggeredCounters();
    
    console.log('Enhanced impact page animations initialized successfully!');
});
