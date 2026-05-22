document.addEventListener("DOMContentLoaded", function () {

    const maestro = document.getElementById("maestro");
    if (maestro) {
        maestro.addEventListener("click", function (e) {
            e.preventDefault();
            window.location.href = "/login/";
        });
    }

    const alumno = document.getElementById("alumno");
    if (alumno) {
        alumno.addEventListener("click", function (e) {
            e.preventDefault();
            window.location.href = "/login/";
        });
    }

    const login_alumno = document.getElementById("login_alumno");
    if (login_alumno) {
        login_alumno.addEventListener("click", function (e) {
            e.preventDefault();
            window.location.href = "/dashboard/";
        });
    }
});