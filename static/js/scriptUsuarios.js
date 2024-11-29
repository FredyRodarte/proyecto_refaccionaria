
function searchUsers() {
    const search = document.getElementById('search-input').value;
    window.location.href = `/admin_usuarios?search=${search}`;
}

function changePage(page) {
    window.location.href = `/admin_usuarios?page=${page}`;
}

function showAddUserForm() {
    document.getElementById('user-form-modal').style.display = 'block';
    document.getElementById('user-form').reset();
}

function showEditUserForm(id) {
    fetch(`/admin_usuarios/${id}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('user-id').value = data.id_usuario;
            document.getElementById('nombre').value = data.nombre;
            document.getElementById('nickname').value = data.nickname;
            document.getElementById('rol').value = data.rol;
            document.getElementById('user-form-modal').style.display = 'block';
        });
}

function deleteUser(id) {
    if (confirm('¿Estás seguro de eliminar este usuario?')) {
        fetch(`/admin_usuarios/${id}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(() => location.reload());
    }
}

function saveUser(){

    // Capturar los datos del formulario
    const id = document.getElementById('user-id').value;
    const nombre = document.getElementById('nombreUser').value;
    const nickname = document.getElementById('nicknameUser').value;
    const contraseña = document.getElementById('contraseñaUser').value;
    const rol = document.getElementById('rolUser').value;

    //Validacion basica
    if (!nombre || !nickname || !contraseña || !rol) {
        alert("Por favor, completa todos los campos.");
        return;
    }

    // Crear objeto de datos
    const userData = {
        id: id || null, // Si es un nuevo usuario, el ID estará vacío
        nombre: nombre,
        nickname: nickname,
        contraseña: contraseña,
        rol: rol
    };

    // Realizar una solicitud AJAX con fetch
    fetch('/admin_usuarios/guardar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Usuario guardado con éxito.");
            location.reload(); // Recargar la página para ver la tabla actualizada
        } else {
            alert("Error al guardar el usuario: " + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Ocurrió un error al guardar el usuario.");
    });
}

function closeModal() {
    document.getElementById('user-form-modal').style.display = 'none';
}


