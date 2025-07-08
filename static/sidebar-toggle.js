const sidebar = document.querySelector('.sidebar');
const toggleBtn = document.getElementById('sidebar-toggle-btn');

toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('closed');
});

// On load, ensure sidebar is open by default on desktop, closed on mobile
function setSidebarState() {
    if (window.innerWidth <= 900) {
        sidebar.classList.add('closed');
    } else {
        sidebar.classList.remove('closed');
    }
}
window.addEventListener('resize', setSidebarState);
document.addEventListener('DOMContentLoaded', setSidebarState); 