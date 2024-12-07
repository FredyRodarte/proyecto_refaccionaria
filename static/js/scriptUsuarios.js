//Funciones de agregar
function agregarUsuario(){
    //abrir el modal de guardar usuarios
    window.location.href='/admin/agregar_usuario';
}

function agregarCategoria(){
    window.location.href='/admin/agregar_categoria';
}

//Funcion guardar
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

function guardarCat(){
    const form = document.querySelector('.form-categorias');
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.text())
    .then(result => {
        alert('Categoria agregada satisfactoriamente');
        window.location.href = '/admin/categorias';
    })
    .catch(error => {
        console.error('Error', error);
    });
}

//-

function editarUsuario(userID) {
    // Redirigir a la ruta de edición
    window.location.href = `/editar_usuario/${userID}`;
}

function guardarEdit(){

}

//Funcion eliminar
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

function eliminarCat(catID){
    if(confirm('¿Estas seguro de eliminar esta categoria?')){
        fetch(`/admin/eliminar_categoria/${catID}`,{
            method: 'POST',
            headers:{
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(response => {
            if(response.ok){
                location.reload();
                alert('Categoria eliminada exitosamente.')
            } else {
                return response.text().then(text => {throw new Error(text)}); 
            }
        }).catch(error => {
            console.error('Error al eliminar categoria:', error);
            alert("Error al eliminar categoria");
        });
    }
}

//Funcion para cancelar
function cancelarUsuario(){
    document.querySelector('.form-usuarios').reset();
    window.location.href='/admin/usuarios';
}

function cancelarEditarUsuario(){
    document.querySelector('.form-editar-usuarios').reset();
    window.location.href='/admin/usuarios';
}

function cancelarCat(){
    document.querySelector('.form-categorias').reset();
    window.location.href='/admin/categorias';
}