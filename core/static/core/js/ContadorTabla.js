

let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    scrollY: "500px",
    lengthMenu: [10, 25, 50, 100, 250, 500],
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5] },
        { orderable: false, targets: [5] },
        { searchable: false, targets: [0, 5] }
    ],
    pageLength: 15,
    destroy: true,
    language: {
        lengthMenu: "Mostrar _MENU_ registros por página",
        zeroRecords: "Ningún usuario encontrado",
        info: "Mostrando de _START_ a _END_ de un total de _TOTAL_ registros",
        infoEmpty: "Ningún usuario encontrado",
        infoFiltered: "(filtrados desde _MAX_ registros totales)",
        search: "Buscar:",
        loadingRecords: "Cargando...",
        paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior"
        }
    }
}

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await list_transferencias();

    dataTable = $('#datatable-transferencias').DataTable(dataTableOptions);

    dataTableIsInitialized = true
}

const list_transferencias = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/list_transferencias/');
        const data = await response.json();
        let content = ``;
        data.transferencias.forEach((transferencias, index) => {
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${transferencias.nombre}</td>
                    <td>${transferencias.apellido}</td>
                    <td>${transferencias.correo }</td>
                    <td>${transferencias.celular }</td>
                    <td>${transferencias.nombre_calle }</td>
                    <td>${transferencias.numero_calle }</td>
                    <td>${transferencias.region }</td>
                    <td>${transferencias.tipo_pago === 'Transferencia'}</td>
                    <td>
                        <buttom class='btn btn-sm btn-primary'><i class='fa-solid fa-pencil'></i></buttom>
                        <buttom class='btn btn-sm btn-danger'><i class='fa-solid fa-trash-can'></i></buttom>
                    </td>
                </tr>
            `;
            if (transferencias.tipo_pago === 'transferencia') {
                console.log('Transferencia');
              } else {
                console.log('No se acepta este tipo de pago');
              }
              
        });
        tableBody_transferencias.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener("load", async () => {
    await initDataTable();
});
