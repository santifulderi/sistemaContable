const formularioBusqueda = document.getElementById('formulario-busqueda')
const fechaDesde = document.getElementById("fecha-desde")
const fechaHasta = document.getElementById("fecha-hasta")
const buttonLimpiarFiltros = document.getElementById("limpiar-filtros")

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