function agregarUsuario(){
    //abrir el modal de guardar usuarios
    window.location.href='/admin/agregar_usuario';
}

function guardarInfo(){
    const form = document.querySelector('.form-usuarios');
    const formData = new FormData(form);
    
    fetch(form.action, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.text())
    .then(result => {
        //console.log('Success:', result);
        alert('Usuario agregado satisfactoriamente')
        window.location.href = '/admin/usuarios';
    })
    .catch(error => {
        console.error('Error', error);
    });
}

function editarUsuario(userID) {
    // Redirigir a la ruta de edición
    window.location.href = `/editar_usuario/${userID}`;
}

function guardarEdit(){

}

function eliminarUsuario(userID){
    //console.log("Esta ingresando al evento onclick", userID)
    if(confirm('¿Estas seguro de eliminar este usuario?')){
        fetch(`/admin/eliminar_usuario/${userID}`,{
            method: 'POST',
            headers:{
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(response => {
            if(response.ok){
                location.reload();
                alert('Usuario eliminado exitosamente.')
            } else {
                return response.text().then(text => {throw new Error(text)});
            }
        }).catch(error =>{
            console.error('Error al eliminar el usuario:', error);
            alert("Error al eliminar al usuario");
        });
    }
    
}

function cancelarUsuario(){
    document.querySelector('.form-usuarios').reset();
    window.location.href='/admin/usuarios';
}

function cancelarEditarUsuario(){
    document.querySelector('.form-editar-usuarios').reset();
    window.location.href='/admin/usuarios';
}