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
        // Implementa la lógica de validación del formato del correo electrónico aquí
        // Por ejemplo, puedes usar una expresión regular
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