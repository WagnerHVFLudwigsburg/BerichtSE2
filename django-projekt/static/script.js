document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const toggleMenu = document.querySelector('.toggle-menu');
    const navBar = document.querySelector('.nav-bar');
    const body = document.body;
    
    // Toggle mobile menu
    function toggleMobileMenu() {
        toggleMenu.classList.toggle('active');
        navBar.classList.toggle('active');
        body.classList.toggle('no-scroll');
    }
    
    // Toggle menu on burger click
    if (toggleMenu) {
        toggleMenu.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleMobileMenu();
        });
    }
    
    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (navBar.classList.contains('active') && 
            !navBar.contains(e.target) && 
            !toggleMenu.contains(e.target)) {
            toggleMobileMenu();
        }
    });
    
    // Close menu when clicking on a nav link (for single page applications)
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (navBar.classList.contains('active')) {
                toggleMobileMenu();
            }
        });
    });
    
    // User profile dropdown
    const userProfile = document.querySelector('.user-profile');
    const profileDropdown = document.querySelector('.profile-dropdown');
    
    if (userProfile && profileDropdown) {
        userProfile.addEventListener('click', function(e) {
            e.stopPropagation();
            profileDropdown.classList.toggle('active');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function() {
            if (profileDropdown.classList.contains('active')) {
                profileDropdown.classList.remove('active');
            }
        });
    }
    
    // Prevent body scroll when menu is open on mobile
    const noScrollClass = 'no-scroll';
    
    // Add no-scroll class to body when menu is open on mobile
    function handleBodyScroll() {
        if (window.innerWidth <= 768) {
            if (navBar.classList.contains('active')) {
                body.classList.add(noScrollClass);
            } else {
                body.classList.remove(noScrollClass);
            }
        } else {
            body.classList.remove(noScrollClass);
        }
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            toggleMenu.classList.remove('active');
            navBar.classList.remove('active');
            body.classList.remove(noScrollClass);
        }
    });
});
