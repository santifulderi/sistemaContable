console.log("El documento .js se cargó correctamente")

const buttonAplicar = document.getElementById("aplicar_cuenta")
const cuenta = document.getElementById("cuenta")


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


async function getCuentaAsientos(idCuenta) {
    let urlGetCuentaAsientos = '/get-cuenta-asientos';
    let cuentaAsientos = []

    await fetch(urlGetCuentaAsientos, {
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
            cuentaAsientos = data['cuenta_asientos']
        })
    console.log("Cuenta asientos(desde la funcion): ",cuentaAsientos)
    return cuentaAsientos;
}

let botonActivado = false;

buttonAplicar.addEventListener('click', async (e) => {
    e.preventDefault()

    if (botonActivado){
        buttonAplicar.innerHTML = "Ver"
        botonActivado = false
        window.location.reload()
    }

    let idCuenta = cuenta.value
    console.log(idCuenta)
    let cuentaAsientos = []
    cuentaAsientos = await getCuentaAsientos(idCuenta)
    console.log(cuentaAsientos)

    let contador = 1

    for (let i = 0; i < cuentaAsientos.length; i++) {
        let tblDatos = document.getElementById('asiento_tabla').insertRow(contador)
        let col1_fecha = tblDatos.insertCell(0)
        let col2_descrpcion = tblDatos.insertCell(1)
        let col3_debe = tblDatos.insertCell(2)
        let col4_haber = tblDatos.insertCell(3)
        // let col5_saldo = tblDatos.insertCell(4)

        console.log("acaaaaaaaaaaaaaaaaaaaaaaa: ", cuentaAsientos[i][0], cuentaAsientos[i][1], cuentaAsientos[i][2], cuentaAsientos[i][3], cuentaAsientos[i][4])
        console.log("acaaaaaaaaaaaaaaaaaaaaaaa: ", cuentaAsientos[i])
        col1_fecha.innerHTML = cuentaAsientos[i][0]
        col2_descrpcion.innerHTML = cuentaAsientos[i][1]
        col3_debe.innerHTML = cuentaAsientos[i][2]
        col4_haber.innerHTML = cuentaAsientos[i][3]
        // col5_saldo.innerHTML = cuentaAsientos[i][4]

        contador+=1
        console.log(contador)
    }
    botonActivado = true
    buttonAplicar.innerHTML = "Dejar de ver"
})