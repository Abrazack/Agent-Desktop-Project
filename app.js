
let currentUser = null;

// Employee Management Functions
function showEmployeeForm() {
    const modal = document.getElementById('settingsModal');
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content">
            <h3>Add Employee</h3>
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" id="empName" required>
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" id="empEmail" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="empPassword" required>
            </div>
            <div class="form-group">
                <label>Department</label>
                <input type="text" id="empDepartment" required>
            </div>
            <div class="form-group">
                <label>Job Title</label>
                <input type="text" id="empJobTitle" required>
            </div>
            <button class="action-button success" onclick="saveEmployee()">Save</button>
            <button class="action-button" onclick="closeModal()">Cancel</button>
        </div>
    `;
}

function saveEmployee() {
    const data = {
        username: document.getElementById('empName').value.toLowerCase().replace(/\s/g, ''),
        full_name: document.getElementById('empName').value,
        email: document.getElementById('empEmail').value,
        password: document.getElementById('empPassword').value,
        department: document.getElementById('empDepartment').value,
        job_title: document.getElementById('empJobTitle').value,
        role: 'employee'
    };

    fetch('/api/employees', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if(result.success) {
            loadEmployees();
            closeModal();
        }
    });
}

function loadEmployees() {
    fetch('/api/employees')
    .then(response => response.json())
    .then(employees => {
        const tbody = document.getElementById('employeeList');
        tbody.innerHTML = employees.map(emp => `
            <tr>
                <td>${emp.full_name}</td>
                <td>${emp.job_title}</td>
                <td>${emp.salary}</td>
                <td>
                    <button class="action-button edit" onclick="editEmployee(${emp.id})">✏️</button>
                    <button class="action-button delete" onclick="deleteEmployee(${emp.id})">🗑️</button>
                </td>
            </tr>
        `).join('');
    });
}

// Inventory Management Functions
function showInventoryForm() {
    const modal = document.getElementById('settingsModal');
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content">
            <h3>Add Product</h3>
            <div class="form-group">
                <label>Product Name</label>
                <input type="text" id="prodName" required>
            </div>
            <div class="form-group">
                <label>Price</label>
                <input type="number" id="prodPrice" step="0.01" required>
            </div>
            <div class="form-group">
                <label>Quantity</label>
                <input type="number" id="prodQuantity" required>
            </div>
            <button class="action-button success" onclick="saveProduct()">Save</button>
            <button class="action-button" onclick="closeModal()">Cancel</button>
        </div>
    `;
}

function saveProduct() {
    const data = {
        name: document.getElementById('prodName').value,
        price: parseFloat(document.getElementById('prodPrice').value),
        quantity: parseInt(document.getElementById('prodQuantity').value),
        reorder_level: 10,
        supplier_id: 1
    };

    fetch('/api/inventory', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if(result.success) {
            loadInventory();
            closeModal();
        }
    });
}

function loadInventory() {
    fetch('/api/inventory')
    .then(response => response.json())
    .then(products => {
        const tbody = document.getElementById('inventoryList');
        tbody.innerHTML = products.map(prod => `
            <tr>
                <td>${prod.name}</td>
                <td>${prod.quantity}</td>
                <td>${prod.price}</td>
                <td>
                    <button class="action-button edit" onclick="editProduct(${prod.id})">✏️</button>
                    <button class="action-button delete" onclick="deleteProduct(${prod.id})">🗑️</button>
                </td>
            </tr>
        `).join('');
    });
}

// Sales Management Functions
function showSaleForm() {
    fetch('/api/inventory')
    .then(response => response.json())
    .then(products => {
        const modal = document.getElementById('settingsModal');
        modal.style.display = 'flex';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>New Sale</h3>
                <div class="form-group">
                    <label>Product</label>
                    <select id="saleProduct" required>
                        ${products.map(p => `<option value="${p.id}">${p.name} - $${p.price}</option>`).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label>Quantity</label>
                    <input type="number" id="saleQuantity" required>
                </div>
                <button class="action-button success" onclick="saveSale()">Complete Sale</button>
                <button class="action-button" onclick="closeModal()">Cancel</button>
            </div>
        `;
    });
}

function saveSale() {
    const productId = document.getElementById('saleProduct').value;
    const quantity = parseInt(document.getElementById('saleQuantity').value);
    
    fetch('/api/sales', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity,
            employee_id: currentUser.id
        })
    })
    .then(response => response.json())
    .then(result => {
        if(result.success) {
            loadSales();
            closeModal();
        }
    });
}

function loadSales() {
    fetch('/api/sales')
    .then(response => response.json())
    .then(sales => {
        const tbody = document.getElementById('salesList');
        tbody.innerHTML = sales.map(sale => `
            <tr>
                <td>${new Date(sale.date).toLocaleString()}</td>
                <td>${sale.product_id}</td>
                <td>${sale.quantity}</td>
                <td>${sale.total_amount}</td>
            </tr>
        `).join('');
    });
}

// Settings Functions
function showSettingsTab(tab) {
    document.querySelectorAll('.settings-tab').forEach(t => t.classList.add('hidden'));
    document.getElementById(`${tab}Settings`).classList.remove('hidden');
}

function showUserForm() {
    const modal = document.getElementById('settingsModal');
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content">
            <h3>Add User</h3>
            <div class="form-group">
                <label>Username</label>
                <input type="text" id="userName" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="userPassword" required>
            </div>
            <div class="form-group">
                <label>Role</label>
                <select id="userRole">
                    <option value="admin">Admin</option>
                    <option value="employee">Employee</option>
                </select>
            </div>
            <button class="action-button success" onclick="saveUser()">Save</button>
            <button class="action-button" onclick="closeModal()">Cancel</button>
        </div>
    `;
}

// Utility Functions
function closeModal() {
    document.getElementById('settingsModal').style.display = 'none';
}

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('roleSelect').value;

    fetch('/api/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ username, password, role })
    })
    .then(response => response.json())
    .then(result => {
        if(result.success) {
            currentUser = result.user;
            document.getElementById('loginPage').classList.add('hidden');
            document.getElementById('dashboard').classList.remove('hidden');
            document.getElementById('currentUser').textContent = `${currentUser.username} (${currentUser.role})`;
            loadEmployees();
            loadInventory();
            loadSales();
        } else {
            alert('Invalid credentials');
        }
    });
}

// Initialize event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Navigation buttons
    document.querySelectorAll('.nav-button').forEach(button => {
        button.addEventListener('click', () => {
            const sectionId = button.dataset.section;
            document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
            document.getElementById(sectionId).classList.remove('hidden');
            
            // Load data for the selected section
            if(sectionId === 'employees') loadEmployees();
            else if(sectionId === 'inventory') loadInventory();
            else if(sectionId === 'sales') loadSales();
        });
    });
});
