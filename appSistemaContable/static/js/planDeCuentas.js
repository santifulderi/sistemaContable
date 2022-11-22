console.log("El documento .js se cargó correctamente")

const buttonActivaModalRegistrarCuenta = document.getElementById("regitrar-cuenta-modal-buttom")
const modalRegistrarCuenta = document.getElementById("registrar-cuenta-modal")
const closeModalRegistrarCuenta = document.getElementById("regitrar-cuenta-modal-close")

const buttonRegistrarCuenta = document.getElementById("button-regitrar-cuenta")

const cuentaNombre = document.getElementById("cuenta_nombre")
const cuentaCodigo = document.getElementById("cuenta_codigo")
const cuentaTipo = document.getElementById("cuenta_tipo")
const cuentaRecibeSaldo = document.getElementById("cuenta_recibe_saldo")
const cuentaSaldoActual = document.getElementById("cuenta_saldo_actual")

const urlExistXodigo = '/cuentas/existe-codigo'
const urlRegistrarCuenta = '/cuentas/registrar-nueva-cuenta'

const formRegistrarCuenta = document.getElementById("form_agregar_cuenta")

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

closeModalRegistrarCuenta.addEventListener('click', (e)=>{
    e.preventDefault()
    modalRegistrarCuenta.classList.remove('modal--show')
})

buttonActivaModalRegistrarCuenta.addEventListener('click', (e)=> {
    e.preventDefault()
    modalRegistrarCuenta.classList.add('modal--show')
})

async function existCodigo(codigo) {
    let existe
    await fetch(urlExistXodigo, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'codigo': codigo})
    })
        .then(response => {
            return response.json()
        })
        .then(data => {
            let value = data['existe']
            existe = value
        })
    return existe;
}

formRegistrarCuenta.addEventListener('submit', async (e) => {
    e.preventDefault()

    let mensaje = ""

    let nombre = cuentaNombre.value
    let codigo = cuentaCodigo.value
    let tipo = cuentaTipo.value
    let recibe_saldo = cuentaRecibeSaldo.checked
    let saldo = cuentaSaldoActual.value

    let codigo_existe = await existCodigo(codigo)

    if (codigo_existe) {
        alert("Codigo ya existente")
    }
    else {
        if (recibe_saldo){
            recibe_saldo=1
        }
        else {
            recibe_saldo=0
        }
        await fetch(urlRegistrarCuenta, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'nombre': nombre, 'codigo': codigo, 'tipo': tipo, 'recibe_saldo': recibe_saldo, 'saldo': saldo})
        })
            .then(response => {
                return response.json()
            })
            .then(data => {
                let mensaje = data['mensaje']
                modalRegistrarCuenta.classList.remove('modal--show')
                window.location.reload()
            })
    }
    console.log(mensaje)
})