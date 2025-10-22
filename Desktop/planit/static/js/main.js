// Main JavaScript for PlanIt

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Loading button states
    document.querySelectorAll('.btn-loading').forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="loading me-2"></span>처리중...';
            this.disabled = true;
            
            // Re-enable after 3 seconds (adjust as needed)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 3000);
        });
    });
});

// Utility functions
const PlanIt = {
    // Show toast notification
    showToast: function(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container') || this.createToastContainer();
        const toast = this.createToast(message, type);
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast after it's hidden
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    },

    createToastContainer: function() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1055';
        document.body.appendChild(container);
        return container;
    },

    createToast: function(message, type) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.setAttribute('role', 'alert');
        
        const typeColors = {
            'success': 'text-bg-success',
            'error': 'text-bg-danger',
            'warning': 'text-bg-warning',
            'info': 'text-bg-info'
        };
        
        toast.innerHTML = `
            <div class="toast-header ${typeColors[type] || 'text-bg-info'}">
                <strong class="me-auto">PlanIt</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;
        
        return toast;
    },

    // Confirm dialog
    confirm: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    },

    // Format date
    formatDate: function(date) {
        return new Intl.DateTimeFormat('ko-KR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'long'
        }).format(new Date(date));
    },

    // Format time
    formatTime: function(time) {
        return new Intl.DateTimeFormat('ko-KR', {
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(`2000-01-01T${time}`));
    },

    // CSRF token helper
    getCsrfToken: function() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    },

    // AJAX helper
    ajax: function(url, options = {}) {
        const defaults = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken()
            }
        };
        
        const config = Object.assign(defaults, options);
        
        return fetch(url, config)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('AJAX Error:', error);
                this.showToast('요청 처리 중 오류가 발생했습니다.', 'error');
                throw error;
            });
    }
};

// Timetable specific functions
const Timetable = {
    init: function() {
        this.bindEvents();
    },

    bindEvents: function() {
        // Timetable slot click events
        document.querySelectorAll('.timetable-slot').forEach(slot => {
            slot.addEventListener('click', this.handleSlotClick.bind(this));
        });
    },

    handleSlotClick: function(event) {
        const slot = event.currentTarget;
        const day = slot.dataset.day;
        const time = slot.dataset.time;
        
        // Open modal or form to add/edit subject
        this.openSubjectModal(day, time);
    },

    openSubjectModal: function(day, time) {
        // Implementation for opening subject modal
        console.log(`Opening modal for ${day} at ${time}`);
    }
};

// Planner specific functions
const Planner = {
    init: function() {
        this.bindEvents();
    },

    bindEvents: function() {
        // Task completion toggle
        document.querySelectorAll('.task-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', this.handleTaskToggle.bind(this));
        });
    },

    handleTaskToggle: function(event) {
        const checkbox = event.target;
        const taskId = checkbox.dataset.taskId;
        const completed = checkbox.checked;
        
        // Update task status via AJAX
        this.updateTaskStatus(taskId, completed);
    },

    updateTaskStatus: function(taskId, completed) {
        PlanIt.ajax(`/planner/tasks/${taskId}/toggle/`, {
            method: 'POST',
            body: JSON.stringify({ completed: completed })
        })
        .then(data => {
            PlanIt.showToast('과제 상태가 업데이트되었습니다.', 'success');
        })
        .catch(error => {
            PlanIt.showToast('과제 상태 업데이트에 실패했습니다.', 'error');
        });
    }
};

// Initialize modules based on current page
document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    
    if (body.classList.contains('timetable-page')) {
        Timetable.init();
    }
    
    if (body.classList.contains('planner-page')) {
        Planner.init();
    }
});
