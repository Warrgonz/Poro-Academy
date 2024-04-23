'use strict';

function cargarDatosUsuarioEnModal(elemento) {
    var id = elemento.getAttribute('data-id');
    var nombre = elemento.getAttribute('data-nombre');
    var cedula = elemento.getAttribute('data-cedula');
    var correo = elemento.getAttribute('data-correo');
    var rol = elemento.getAttribute('data-rol');

    // Llenar el formulario de edición con los datos del usuario
    document.getElementById('usuario_id_editar').value = id;
    document.getElementById('nombre_editar').value = nombre;
    document.getElementById('cedula_editar').value = cedula;
    document.getElementById('correo_editar').value = correo;
    document.getElementById('rol_editar').value = rol;
}

function eliminarUsuario(usuario_id) {
    Swal.fire({
        title: "¿Está seguro que desea eliminar al usuario?",
        text: "¡Estos cambios no se pueden revertir!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Eliminar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            // Enviar solicitud al servidor para eliminar el usuario
            fetch('/user/eliminar', {
                method: 'POST',
                body: JSON.stringify({ usuario_id: usuario_id }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        title: "Eliminado!",
                        text: "El usuario fue eliminado apropiadamente.",
                        icon: "success"
                    }).then(() => {
                        // Recargar la página después de la eliminación exitosa
                        location.reload();
                    });
                } else {
                    Swal.fire({
                        title: "Error!",
                        text: data.message,
                        icon: "error"
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });
}

