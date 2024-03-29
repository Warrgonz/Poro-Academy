// Navbar toggler.

const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("expand");
});

// Login

$("form[name=login_form]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    var correo = $form.find("#correo").val();
    var password = $form.find("#password").val();

    // Validar si los campos están vacíos
    if (!correo || !password) {
        alert("Favor llenar todos los campos.");
        return false; // Evita que el formulario se envíe
    }

    // Validar el formato del correo electrónico
    if (!validarCorreo(correo)) {
        alert("El formato del correo electrónico no es válido.");
        return false; // Evita que el formulario se envíe
    }
    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        success: function (resp) {
            window.location.href = "/";
        },
        error: function (xhr, status, error) {
            if (xhr.status === 401) {
                $error.text(xhr.responseText).removeClass("error--hidden");
            } else {
                $error.text("Error al procesar la solicitud").removeClass("error--hidden");
            }
        }
    });

    function validarCorreo(correo) {
        var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(correo);
    }

    e.preventDefault();
});


// Sign up

$("form[name=signup_form]").submit(function (e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/templates/registroUsuarios.html",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "registroUsuarios.html";
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
})

function validateForm() {
    var nombre = document.getElementById("nombre").value;
    var cedula = document.getElementById("cedula").value;
    // Agregar más campos aquí si es necesario
    
    var isValid = true;

    // Verificar si el campo de nombre está vacío
    if (nombre.trim() === "") {
        document.getElementById("nombre").classList.add("invalid-input");
        isValid = false;
    } else {
        document.getElementById("nombre").classList.remove("invalid-input");
    }

    // Verificar si el campo de cédula está vacío
    if (cedula.trim() === "") {
        document.getElementById("cedula").classList.add("invalid-input");
        isValid = false;
    } else {
        document.getElementById("cedula").classList.remove("invalid-input");
    }

    // Agregar más verificaciones para otros campos si es necesario

    return isValid;
}


// Editar usuario.

$("#editar_form").submit(function (e) {

    var $form = $(this);
    var $error = $form.find(".error-editar");
    var data = $form.serialize();

    $.ajax({
        url: "/editar_usuario",  // Ruta de la aplicación Flask para editar usuario
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            // Manejar la respuesta del servidor (opcional)
            console.log(resp);
            // Opcional: recargar la página o redireccionar a otra después de editar el usuario
            // window.location.href = "ruta_de_redireccion_despues_de_editar";
        },
        error: function (resp) {
            // Manejar errores (opcional)
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});
