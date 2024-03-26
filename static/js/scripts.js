// Navbar toggler.

const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});

// Login

$("form[name=login_form]").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/dashboard/";
        },
        error: function(xhr, status, error){
            if (xhr.status === 401) {
                $error.text("Credenciales inválidas").removeClass("error--hidden");
            } else {
                $error.text("Error al procesar la solicitud").removeClass("error--hidden");
            }
        }
    });

    e.preventDefault();
});


// Sign up

$("form[name=signup_form]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/templates/registroUsuarios.html",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "registroUsuarios.html";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
})