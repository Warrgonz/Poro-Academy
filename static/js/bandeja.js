'use strict';

function actualizarEstado(idSolicitud, accion) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/actualizar_solicitud", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    var data = JSON.stringify({ id_solicitud: idSolicitud, accion: accion });

    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log("La solicitud fue actualizada correctamente.");
            window.location.href = "/bandeja"; // Redirige a la bandeja después de actualizar la solicitud
        } else {
            console.error("Hubo un error al actualizar la solicitud.");
        }
    };

    xhr.send(data);
}

