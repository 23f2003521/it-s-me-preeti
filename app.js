/* ==========================================================================
   PREETI MAURYA PORTFOLIO JS - PREMIUM NEON SYSTEM INTERACTIVITY
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // --- Mobile Navigation Toggle ---
    const menuToggle = document.getElementById('menu-toggle');
    const navbar = document.getElementById('navbar');
    const navLinks = document.querySelectorAll('.nav-link');

    if (menuToggle && navbar) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            navbar.classList.toggle('active');
        });

        // Close navbar when clicking a nav link
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                navbar.classList.remove('active');
            });
        });
    }

    // --- Floating Header Scroll Effect ---
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // --- Dynamic Typewriter Effect ---
    const typewriterElement = document.getElementById('typewriter');
    const words = [
        "Junior Software Developer @ SGBC IITM",
        "Data Science Student @ IIT Madras",
        "Building Cross-Platform Plugin Architectures",
        "AI/ML On-Campus Lead 2025"
    ];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;

    function typeEffect() {
        const currentWord = words[wordIndex];
        
        if (isDeleting) {
            // Delete characters
            typewriterElement.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = 50; // Deleting is faster
        } else {
            // Add characters
            typewriterElement.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 100;
        }

        // State switching
        if (!isDeleting && charIndex === currentWord.length) {
            // Word complete, wait before starting delete
            typingSpeed = 2000;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            // Word fully deleted, move to next word
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            typingSpeed = 500; // brief pause before writing next
        }

        setTimeout(typeEffect, typingSpeed);
    }

    if (typewriterElement) {
        setTimeout(typeEffect, 1000);
    }

    // --- Mouse-Tracking Background Gradient Blobs ---
    const blobPurple = document.querySelector('.blob-purple');
    const blobBlue = document.querySelector('.blob-blue');
    const blobCyan = document.querySelector('.blob-cyan');
    let ticking = false;

    window.addEventListener('mousemove', (e) => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const mouseX = e.clientX;
                const mouseY = e.clientY;
                
                // Shift blobs slightly based on mouse position for 3D parallax depth
                if (blobPurple) {
                    blobPurple.style.transform = `translate(${mouseX * 0.05}px, ${mouseY * 0.05}px)`;
                }
                if (blobBlue) {
                    blobBlue.style.transform = `translate(${-(mouseX * 0.03)}px, ${-(mouseY * 0.03)}px)`;
                }
                if (blobCyan) {
                    blobCyan.style.transform = `translate(${mouseX * 0.02}px, ${-(mouseY * 0.04)}px)`;
                }
                
                ticking = false;
            });
            ticking = true;
        }
    });

    // --- Intersection Observer for Active Nav Highlighter ---
    const sections = document.querySelectorAll('section');
    const observerOptions = {
        root: null,
        rootMargin: '-20% 0px -60% 0px', // Trigger near screen middle
        threshold: 0
    };

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                
                // Remove active class from all links
                navLinks.forEach(link => link.classList.remove('active'));
                
                // Add active class to corresponding nav link
                const activeLink = document.querySelector(`.nav-link[href="#${id}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        });
    }, observerOptions);

    sections.forEach(section => sectionObserver.observe(section));

    // --- Entrance Scroll Animations (Reveal items on scroll) ---
    const revealElements = document.querySelectorAll('.glass-card, .timeline-item, .section-header');
    
    const revealObserverOptions = {
        root: null,
        rootMargin: '0px 0px -100px 0px', // Trigger just before elements enter view
        threshold: 0.1
    };

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal', 'active');
                revealObserver.unobserve(entry.target); // Animate only once
            }
        });
    }, revealObserverOptions);

    revealElements.forEach(el => {
        el.classList.add('reveal');
        revealObserver.observe(el);
    });

    // --- Toast Notification System ---
    const toast = document.getElementById('toast');
    function showToast(message) {
        if (!toast) return;
        toast.textContent = message;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    // --- Copy to Clipboard Functionality ---
    const copyEmailBtn = document.getElementById('copy-email-btn');
    const copyPhoneBtn = document.getElementById('copy-phone-btn');

    if (copyEmailBtn) {
        copyEmailBtn.addEventListener('click', () => {
            const email = copyEmailBtn.querySelector('.c-value').textContent;
            navigator.clipboard.writeText(email).then(() => {
                showToast("Email address copied!");
            }).catch(err => {
                console.error('Could not copy email: ', err);
            });
        });
    }

    if (copyPhoneBtn) {
        copyPhoneBtn.addEventListener('click', () => {
            const phone = copyPhoneBtn.querySelector('.c-value').textContent;
            navigator.clipboard.writeText(phone).then(() => {
                showToast("Phone number copied!");
            }).catch(err => {
                console.error('Could not copy phone number: ', err);
            });
        });
    }

    // --- Premium Contact Form Handler ---
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Collect Form Values
            const name = document.getElementById('form-name').value;
            const email = document.getElementById('form-email').value;
            const subject = document.getElementById('form-subject').value;
            const message = document.getElementById('form-message').value;

            // Submit visual feedback
            const submitBtn = contactForm.querySelector('.btn-submit');
            const originalBtnHtml = submitBtn.innerHTML;
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = `Sending... <span class="spinner"></span>`;
            
            // Simulating successful email dispatch (which can be wired to EmailJS/Formspree easily)
            setTimeout(() => {
                showToast(`Thank you, ${name}! Your message has been sent.`);
                contactForm.reset();
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnHtml;
            }, 1500);
        });
    }
});
