console.log("El documento .js se cargó correctamente")

const buttonModalRegistrarCuenta = document.getElementById("regitrar-cuenta-modal-buttom")
const modalRegistrarCuenta = document.getElementById("registrar-cuenta-modal")
const closeModalRegistrarCuenta = document.getElementById("regitrar-cuenta-modal-close")


closeModalRegistrarCuenta.addEventListener('click', (e)=>{
    e.preventDefault()
    modalRegistrarCuenta.classList.remove('modal--show')
})

buttonModalRegistrarCuenta.addEventListener('click', (e)=> {
    e.preventDefault()
    modalRegistrarCuenta.classList.add('modal--show')
})