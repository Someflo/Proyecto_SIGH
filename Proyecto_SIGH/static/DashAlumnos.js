function cambiarActivo(posicion) {
    const items = document.querySelectorAll(".nav ul li");

    items.forEach(item => {
        item.classList.remove("active");
    });

    if (items[posicion]) {
        items[posicion].classList.add("active");
    }
}

function cargarTemplate(idTemplate) {
    const template = document.getElementById(idTemplate);
    const contenido = document.getElementById("contenido-vista");

    if (template && contenido) {
        contenido.innerHTML = template.innerHTML;
    }
}

function mostrarGenerales() {
    document.getElementById("titulo-vista").innerText = "Generales";
    cargarTemplate("template-generales");
    cambiarActivo(1);
}

function mostrarHorarios() {
    document.getElementById("titulo-vista").innerText = "Horarios";
    cargarTemplate("template-horarios");
    cambiarActivo(2);
}

function mostrarAsistencias() {
    document.getElementById("titulo-vista").innerText = "Asistencias";
    cargarTemplate("template-asistencias");
    cambiarActivo(3);
}

function mostrarInformacionGrupo() {
    document.getElementById("titulo-vista").innerText = "Información del Grupo";
    cargarTemplate("template-grupo");
    cambiarActivo(4);
}

function mostrarNotificaciones() {
    document.getElementById("titulo-vista").innerText = "Notificaciones";
    cargarTemplate("template-notificaciones");
    cambiarActivo(5);
}

document.addEventListener("DOMContentLoaded", function () {
    mostrarGenerales();
});