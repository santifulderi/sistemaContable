console.log("El documento .js se cargó correctamente")

const buttonModalRegistrarAsiento = document.getElementById("regitrar-asiento-modal-buttom")
const modalRegistrarAsiento = document.getElementById("registrar-asiento-modal")
const closeModalRegistrarAsiento = document.getElementById("regitrar-asiento-modal-close")

const asientoDescripcion = document.getElementById("descripcion_asiento")
const asientoTabla = document.getElementById("asiento_tabla")


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


closeModalRegistrarAsiento.addEventListener('click', (e)=>{
    e.preventDefault()
    modalRegistrarAsiento.classList.remove('modal--show')
    window.location.reload()
})

buttonModalRegistrarAsiento.addEventListener('click', (e)=> {
    e.preventDefault()
    modalRegistrarAsiento.classList.add('modal--show')
})

const buttonAgregar = document.getElementById("button_agregar")

const renglonCuenta = document.getElementById("renglon_cuenta")
const renglonMonto = document.getElementById("renglon_monto")
const renglonDebe = document.getElementById("renglon_debe")
const renglonHaber = document.getElementById("renglon_haber")
const formRenglon = document.getElementById("form_renglon")

let entrar = false
let cantidad_renglones = 0
let cuentas_usadas = []
let renglonesAsiento = []

async function isValidSaldo(idCuenta, monto, isDebe) {
    console.log("##########DEBE: ", isDebe)
    const URL = "/is-valid-saldo"
    // let auxValue
    let datos = []

    //esto se hace porque (creo que) no acepta el json valores booleanos
    let tipoOperacion
    if (isDebe){
        tipoOperacion = 'debe'
    }
    else{
        tipoOperacion = 'haber'
    }

    await fetch(URL, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'id_cuenta': idCuenta, 'monto': monto, 'tipo_operacion': tipoOperacion }) //JavaScript object of data to POST
    })
        .then(response => {
            return response.json() //Convert response to JSON
        })
        .then(data => {
            //Perform actions with the response data from the view
            let value = data['value']
            console.log(data['mensaje'])
            console.log("Esto viene en data[value]: ", data['value'])
            auxValue = value
            console.log(auxValue)
            // return data["value"]
            // let datos = []
            datos.push(data["value"])
            datos.push(data['mensaje'])
            // return datos
        })
    // return auxValue
    return datos
}

const urlGetNombreCuenta = "/get-nombre-cuenta"

async function getNombreCuenta(idCuenta) {
    let nombre = ""
    await fetch(urlGetNombreCuenta, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'id_cuenta': idCuenta})
    })
        .then(response => {
            return response.json()
        })
        .then(data => {
            let value = data['nombre']
            nombre = value
        })
    console.log("Nombre cuenta: ",nombre)
    return nombre;
}

//cuando se le da click al boton 'Agregar' para ir agregando los renglones
formRenglon.addEventListener('submit', async (e) => {
    e.preventDefault()

    entrar = false

    if (cuentas_usadas.includes(renglonCuenta.value)) {
        entrar = true
        alert("No es posible utilizar más de una vez la misma cuenta")
    } else {
        if (renglonMonto.value <= 0) {
            entrar = true
            alert("Ingrese un monto valido.")
        }
        if (renglonMonto.value === 'NaN') {
            entrar = true
            alert("Ingrese un monto valido.")
        }
        if ((renglonDebe.checked === true && renglonHaber.checked === true) || (renglonDebe.checked === false && renglonHaber.checked === false)) {
            entrar = true
            alert("Ingrese correctamente si va por el 'Debe' o por el 'Haber'.")
        }
        let auxData = await isValidSaldo(renglonCuenta.value, renglonMonto.value, renglonDebe.checked)
        console.log("auxData: ", auxData)
        let auxValue = auxData[0]
        let auxMensaje = auxData[1]
        if (!auxValue) {
            entrar = true
            alert(auxMensaje)
        }
    }

    if (!entrar) {

        cantidad_renglones += 1
        console.log("Cantidad de renglones: ", cantidad_renglones)

        let tblDatos = document.getElementById('asiento_tabla').insertRow(cantidad_renglones)
        let col1_cuenta = tblDatos.insertCell(0)
        let col2_debe = tblDatos.insertCell(1)
        let col3_haber = tblDatos.insertCell(2)

        cuentas_usadas.push(renglonCuenta.value)
        console.log(cuentas_usadas)

        let nombreCuenta = getNombreCuenta(renglonCuenta.value)

        if (renglonDebe.checked) {
            // col1_cuenta.innerHTML = renglonCuenta.value
            col1_cuenta.innerHTML = await nombreCuenta
            col2_debe.innerHTML = renglonMonto.value
            col3_haber.innerHTML = ''
            renglonesAsiento.push([renglonCuenta.value, parseFloat(renglonMonto.value), 0, renglonMonto.value])
            console.log(renglonesAsiento)
        } else {
            col1_cuenta.style.setProperty("text-align", "right")
            // col1_cuenta.innerHTML = renglonCuenta.value
            col1_cuenta.innerHTML = await nombreCuenta
            col2_debe.innerHTML = ''
            col3_haber.innerHTML = renglonMonto.value
            renglonesAsiento.push([renglonCuenta.value, 0, parseFloat(renglonMonto.value), renglonMonto.value])
            console.log(renglonesAsiento)
        }

        //para limpiar los campos luego de agregar
        // renglonCuenta.innerHTML = ''
        renglonMonto.value = ""
        renglonDebe.checked = false
        renglonHaber.checked = false

    }
})


buttonEliminarUltimoRenglon = document.getElementById("button-cancelar-asiento")

buttonEliminarUltimoRenglon.addEventListener('click', (e)=>{
    e.preventDefault()

    if (cantidad_renglones>0) {
        if (cantidad_renglones===1){
            // document.getElementById("asiento_tabla").getElementsByTagName("tr")[cantidad_renglones-1].remove()
            // cantidad_renglones=0
            // console.log("Cantidad de renglones(luego de borrar): ", cantidad_renglones)
            alert("No es posible borrar, es el único renglón")
            console.log("No es posible borrar el único renglón")
        }
        else{
            document.getElementById("asiento_tabla").getElementsByTagName("tr")[cantidad_renglones].remove()
            cantidad_renglones-=1
            console.log("Cantidad de renglones(luego de borrar): ", cantidad_renglones)
            cuentas_usadas.pop()
            renglonesAsiento.pop()
            console.log(cuentas_usadas)
        }
    }
    else{
        alert("No es posible borrar, no existen renglones")
        console.log("No es posible borrar, no existen renglones")
    }
})


const buttonRegistrarAsiento = document.getElementById("button-regitrar-asiento")

function isAsientoBalanceado(renglonesAsiento) {
    let saldoDebe = 0.00
    let saldoHaber = 0.00
    for (let i = 0; i < renglonesAsiento.length; i++) {
        console.log("id_cuenta:",renglonesAsiento[i][0])
        console.log("debe:",renglonesAsiento[i][1])
        console.log("haber:",renglonesAsiento[i][2])
        console.log("saldo:",renglonesAsiento[i][3])

        saldoDebe += renglonesAsiento[i][1]
        saldoHaber += renglonesAsiento[i][2]
    }
    return saldoDebe===saldoHaber;
}

buttonRegistrarAsiento.addEventListener('click', async (e) => {
    e.preventDefault()

    const urlRegistrarAsiento = '/registrar-nuevo-registro'

    let descripcion = asientoDescripcion.value
    if (descripcion===""){
        descripcion="Sin descripción"
    }
    let valido = isAsientoBalanceado(renglonesAsiento)
    console.log("El asiento esta balanceado: ", valido)

    if (valido && renglonesAsiento.length>1){
        await fetch(urlRegistrarAsiento, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'descripcion': descripcion, 'array_renglones': renglonesAsiento})
        })
            .then(response => {
                return response.json()
            })
            .then(data => {
                let mensaje = data['mensaje']
                modalRegistrarAsiento.classList.remove('modal--show')
            })
    }
    else{
        if (renglonesAsiento.length>1) {
            alert("No es posible registrar. El asiento está desbalanceado.")
        }
        else{
            alert("No es posible registrar un asiento incompleto.")
        }
    }
})