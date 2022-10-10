console.log("El documento .js se cargó correctamente")

const formularioBusqueda = document.getElementById('formulario-busqueda')
const fechaDesde = document.getElementById("fecha-desde")
const fechaHasta = document.getElementById("fecha-hasta")
const buttonLimpiarFiltros = document.getElementById("limpiar-filtros")

const buttonModalRegistrarAsiento = document.getElementById("regitrar-asiento-modal-buttom")
const modalRegistrarAsiento = document.getElementById("registrar-asiento-modal")
const closeModalRegistrarAsiento = document.getElementById("regitrar-asiento-modal-close")


closeModalRegistrarAsiento.addEventListener('click', (e)=>{
    e.preventDefault()
    modalRegistrarAsiento.classList.remove('modal--show')
})

buttonModalRegistrarAsiento.addEventListener('click', (e)=> {
    e.preventDefault()
    modalRegistrarAsiento.classList.add('modal--show')
})




function getFechaActual(){
    let today = new Date()
    let day = today.getDate()
    let month = today.getMonth() + 1
    let year = today.getFullYear()

    // return '${year}-${month}-${day}'
    return (year+'-'+month+'-'+day)
}

buttonLimpiarFiltros.addEventListener('click', (e)=>{
    e.preventDefault()
    alert("Limpiando filtros...")
    fechaDesde.innerHTML = ''
    fechaHasta.innerHTML = ''
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

formularioBusqueda.addEventListener("submit", e => {
    e.preventDefault()
    let entrar = false


    if (fechaDesde.value === '' || fechaHasta.value === ''){
        entrar = true
        alert("Error: no puede ingresar fechas nulas")
    }
    else{
        if (fechaDesde.value > fechaHasta.value){
            entrar = true
            alert("Error: la fecha desde no puede ser mayor que la fecha hasta")
        }
    }



    // if (fechaDesde.value > getFechaActual()){
    //     entrar = true
    //     console.log("Error: la fecha desde es mayor a la fecha actual")
    // //    no funciona
    // }

    if (!entrar) {
        console.log("El formulario se envía correctamente")
        formularioBusqueda.submit()
    }
})
