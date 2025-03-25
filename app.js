
let currentUser = null;

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('roleSelect').value;

    // In a real application, this would be a server request
    if (username === 'admin' && password === 'admin123' && role === 'admin') {
        currentUser = { username, role };
        showMainSection();
    } else {
        alert('Invalid credentials');
    }
}

function showMainSection() {
    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('mainSection').style.display = 'block';
    document.getElementById('userWelcome').textContent = `${currentUser.username} (${currentUser.role})`;
    
    if (currentUser.role === 'admin') {
        document.getElementById('adminControls').style.display = 'block';
        document.getElementById('employeeControls').style.display = 'none';
    } else {
        document.getElementById('adminControls').style.display = 'none';
        document.getElementById('employeeControls').style.display = 'block';
    }
}

function logout() {
    currentUser = null;
    document.getElementById('loginSection').style.display = 'block';
    document.getElementById('mainSection').style.display = 'none';
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
}

// Admin functions
function showEmployeeManager() {
    // Implementation would go here
    alert('Employee Manager - To be implemented');
}

function showInventoryManager() {
    // Implementation would go here
    alert('Inventory Manager - To be implemented');
}

function showLogs() {
    // Implementation would go here
    alert('System Logs - To be implemented');
}

// Employee functions
function viewInventory() {
    // Implementation would go here
    alert('Inventory View - To be implemented');
}

function viewProfile() {
    // Implementation would go here
    alert('Profile View - To be implemented');
}
