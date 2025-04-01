// Intersection Observer for animations
const animationObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
            if (entry.target.dataset.delay) {
                entry.target.style.animationDelay = `${entry.target.dataset.delay}s`;
            }
        }
    });
}, {
    threshold: 0.1
});

// Elements to animate
document.querySelectorAll('.animate-on-scroll').forEach(element => {
    animationObserver.observe(element);
});

// Parallax effect
const parallaxElements = document.querySelectorAll('.parallax');
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    
    parallaxElements.forEach(element => {
        const speed = element.dataset.speed || 0.5;
        const yPos = -(scrolled * speed);
        element.style.transform = `translateY(${yPos}px)`;
    });
});

// Smooth section transitions
const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('section-visible');
        }
    });
}, {
    threshold: 0.1
});

document.querySelectorAll('section').forEach(section => {
    sectionObserver.observe(section);
});

// Counter animation
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const counter = entry.target;
            const target = parseInt(counter.dataset.target);
            const duration = parseInt(counter.dataset.duration) || 2000;
            let current = 0;
            const step = target / (duration / 16);
            
            const updateCounter = () => {
                current += step;
                if (current < target) {
                    counter.textContent = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };
            
            requestAnimationFrame(updateCounter);
            counterObserver.unobserve(counter);
        }
    });
}, {
    threshold: 1
});

document.querySelectorAll('.counter').forEach(counter => {
    counterObserver.observe(counter);
});

// Stagger animations for lists
document.querySelectorAll('.stagger-list').forEach(list => {
    const items = list.children;
    Array.from(items).forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
    });
});

// Scroll progress indicator
const progressBar = document.querySelector('.scroll-progress');
if (progressBar) {
    window.addEventListener('scroll', () => {
        const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (window.scrollY / windowHeight) * 100;
        progressBar.style.width = `${scrolled}%`;
    });
}

// Typing animation
class TypeWriter {
    constructor(element, words, wait = 3000) {
        this.element = element;
        this.words = words;
        this.txt = '';
        this.wordIndex = 0;
        this.wait = parseInt(wait, 10);
        this.type();
        this.isDeleting = false;
    }
    
    type() {
        const current = this.wordIndex % this.words.length;
        const fullTxt = this.words[current];
        
        if (this.isDeleting) {
            this.txt = fullTxt.substring(0, this.txt.length - 1);
        } else {
            this.txt = fullTxt.substring(0, this.txt.length + 1);
        }
        
        this.element.innerHTML = `<span class="txt">${this.txt}</span>`;
        
        let typeSpeed = 100;
        
        if (this.isDeleting) {
            typeSpeed /= 2;
        }
        
        if (!this.isDeleting && this.txt === fullTxt) {
            typeSpeed = this.wait;
            this.isDeleting = true;
        } else if (this.isDeleting && this.txt === '') {
            this.isDeleting = false;
            this.wordIndex++;
            typeSpeed = 500;
        }
        
        setTimeout(() => this.type(), typeSpeed);
    }
}

// Initialize typing animation
document.querySelectorAll('.txt-type').forEach(element => {
    const words = JSON.parse(element.getAttribute('data-words'));
    const wait = element.getAttribute('data-wait');
    new TypeWriter(element, words, wait);
});

// Tilt effect
document.querySelectorAll('.tilt').forEach(element => {
    element.addEventListener('mousemove', e => {
        const { left, top, width, height } = element.getBoundingClientRect();
        const x = (e.clientX - left) / width;
        const y = (e.clientY - top) / height;
        
        const tiltX = (y - 0.5) * 20;
        const tiltY = (x - 0.5) * 20;
        
        element.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
    });
    
    element.addEventListener('mouseleave', () => {
        element.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
    });
}); 