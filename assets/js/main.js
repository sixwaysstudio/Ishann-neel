const loadComponents = () => {
    // Determine path prefix based on location
    const isInSubfolder = window.location.pathname.includes('/others/');
    const rootPath = isInSubfolder ? '../' : './';
    const othersPath = isInSubfolder ? './' : 'others/';

    // Inject FontAwesome if not present
    if (!document.getElementById('font-awesome')) {
        const faLink = document.createElement('link');
        faLink.id = 'font-awesome';
        faLink.rel = 'stylesheet';
        faLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
        document.head.appendChild(faLink);
    }

    // Navbar HTML
    const navbarHTML = `
    <nav class="glass-nav">
        <div class="logo-text">ISHAAN<span class="highlight">NEEL</span></div>
        <ul class="nav-links">
            <li><a href="${rootPath}index.html" class="nav-item">Home</a></li>
            <li><a href="${othersPath}about.html" class="nav-item">Story</a></li>
            <li><a href="${othersPath}works.html" class="nav-item">Portfolio</a></li>
            <li><a href="${othersPath}contact.html" class="nav-item">Contact</a></li>
        </ul>
        <div class="burger">
            <div class="line1"></div>
            <div class="line2"></div>
            <div class="line3"></div>
        </div>
    </nav>
    <div class="background-blobs">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
    </div>
    `;

    // Footer HTML
    const footerHTML = `
    <footer class="glass-footer">
        <div class="footer-content">
            <div class="footer-brand">
                <h2>ISHAAN NEEL</h2>
                <p>Photography Portfolio</p>
            </div>
            <div class="footer-socials">
                <h4>Follow Me</h4>
                <div style="display: flex; gap: 1.5rem; font-size: 1.5rem;">
                    <a href="https://instagram.com/vagabond.nef" target="_blank" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                    <a href="https://www.facebook.com/profile.php?id=100088930056390" target="_blank" aria-label="Facebook"><i class="fab fa-facebook"></i></a>
                    <a href="mailto:ishaankphotography@gmail.com" aria-label="Email"><i class="fas fa-envelope"></i></a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            &copy; 2024 Ishaan Neel Photography. All rights reserved.
        </div>
    </footer>
    `;

    // Inject if placeholders exist (or prepend/append)
    // We will prepend Nav and append Footer if specific containers don't exist

    // Navbar Injection
    const navContainer = document.getElementById('dynamic-nav');
    if (navContainer) {
        navContainer.innerHTML = navbarHTML;
    } else {
        // Fallback: Prepend to body if not present
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = navbarHTML;
        while (tempDiv.firstChild) {
            document.body.insertBefore(tempDiv.lastChild, document.body.firstChild);
        }
    }

    // Footer Injection
    const footerContainer = document.getElementById('dynamic-footer');
    if (footerContainer) {
        footerContainer.innerHTML = footerHTML;
    } else {
        // Fallback: Append to body
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = footerHTML;
        while (tempDiv.firstChild) {
            document.body.appendChild(tempDiv.firstChild);
        }
    }

    // Re-initialize Nav Listeners since elements are new
    initNavListeners();
}

const initNavListeners = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');

    if (burger) {
        burger.addEventListener('click', () => {
            // Toggle Nav
            nav.classList.toggle('nav-active');
            burger.classList.toggle('toggle');

            // Animate Links
            navLinks.forEach((link, index) => {
                if (link.style.animation) {
                    link.style.animation = '';
                } else {
                    link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
                }
            });
        });
    }
}

// Navigation Toggle (Legacy function kept but internals moved to initNavListeners)
const navSlide = () => {
    // Already handled in loadComponents -> initNavListeners
}


// Scroll Reveal Animation
const scrollReveal = () => {
    const reveals = document.querySelectorAll('.glass-card, .section-title, .portfolio-item, .work-item, .contact-card-large');

    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        const elementVisible = 150;

        reveals.forEach((reveal) => {
            const elementTop = reveal.getBoundingClientRect().top;
            if (elementTop < windowHeight - elementVisible) {
                reveal.classList.add('show');
            } else {
                reveal.classList.remove('show');
            }
        });
    };

    window.addEventListener('scroll', revealOnScroll);
}

// Init
const app = () => {
    loadComponents();
    scrollReveal();
    /* --- Portfolio Logic --- */

    // Elements
    const modal = document.getElementById('gallery-modal');
    const modalTitle = document.getElementById('modal-category-title');
    const galleryGrid = document.getElementById('gallery-grid');
    const closeModal = document.querySelector('.close-modal');
    const categoryCards = document.querySelectorAll('.category-card');

    // Open Modal
    if (categoryCards) {
        categoryCards.forEach(card => {
            card.addEventListener('click', () => {
                const category = card.getAttribute('data-category');

                // Use global galleryData if available
                let images = [];
                if (typeof galleryData !== 'undefined') {
                    // Filter matching category
                    // galleryData categories are normalized to lowercase
                    // We map 'wildlife' -> 'wild life' logic if needed, but our script generates 'wild life'
                    // actually the script generates based on folder name. 
                    // Folder: 'WILD LIFE' -> category: 'wild life'
                    // Folder: 'STREET' -> category: 'street'

                    images = galleryData.filter(item => {
                        // Loose matching for "wildlife" vs "wild life"
                        if (category === 'wildlife' && item.category === 'wild life') return true;
                        return item.category === category;
                    });
                } else {
                    console.error('galleryData missing');
                }

                if (modalTitle) modalTitle.textContent = category.toUpperCase();

                if (galleryGrid) {
                    galleryGrid.innerHTML = ''; // Clear previous

                    if (images && images.length > 0) {
                        images.forEach(item => {
                            const img = document.createElement('img');
                            // src in galleryData is relative to 'works.html' (../assets/...)
                            // for index.html (root), remove one '../'
                            img.src = item.src.replace('../assets/', 'assets/');
                            img.alt = item.title;
                            img.loading = "lazy";
                            galleryGrid.appendChild(img);
                        });
                    } else {
                        galleryGrid.innerHTML = '<p style="color:white; text-align:center;">No images found. Run update-gallery.bat if you added new photos.</p>';
                    }
                }

                if (modal) {
                    modal.style.display = 'block';
                    document.body.style.overflow = 'hidden';
                }
            });
        });
    }

    // Close Modal
    if (closeModal) {
        closeModal.addEventListener('click', () => {
            if (modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }

    // Close on outside click
    window.addEventListener('click', (e) => {
        if (modal && e.target == modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
}

app();
