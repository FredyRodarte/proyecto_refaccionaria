function guardarUsuario(){
    //abrir el modal de guardar usuarios
    window.location.href='/admin/guardar_usuario';
}

function guardarInfo(){
    //
}

function editarUsuario(id){
    window.location.href='/admin/guardar_usuario?id=' + id;
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
    window.location.href='/admin/usuarios';
}