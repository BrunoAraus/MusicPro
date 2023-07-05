

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
                    <td>${transferencias.tipo_pago === 'Transferencia'}</td>
                    <td>
                        <buttom class='btn btn-sm btn-primary'><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check2" viewBox="0 0 16 16">
                        <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
                      </svg><i class='fa-solid fa-pencil'></i></buttom>
                    </td>
                    <td>
                        <buttom class='btn btn-sm btn-danger'>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                        </svg><i class='fa-solid fa-trash-can'></i></buttom>
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
