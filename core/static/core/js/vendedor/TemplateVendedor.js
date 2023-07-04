let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    lengthMenu: [10, 25, 50, 100, 250, 500],
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5] },
        { orderable: false, targets: [4, 5] },
        { searchable: false, targets: [0, 5] }
    ],
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

    await listProductos();

    dataTable = $('#datatable-productos').DataTable(dataTableOptions);

    dataTableIsInitialized = true
}

const listProductos = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/list_productos/');
        const data = await response.json();

        let content = ``;
        data.productos.forEach((productos, index) => {
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${productos.nombre}</td>
                    <td>${productos.stock}</td>
                    <td>${productos.precio}</td>
                    <td>${productos.stock < 1
                    ? "<i class='fa-solid fa-xmark' style='color: red;'></i>"
                    : "<i class='fa-solid fa-check' style='color: green;'></i>"}</td>
                    <td>
                        <buttom class='btn btn-sm btn-primary'><i class='fa-solid fa-pencil'></i></buttom>
                        <buttom class='btn btn-sm btn-danger'><i class='fa-solid fa-trash-can'></i></buttom>
                    </td>
                </tr>
            `;
        });
        tableBody_productos.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener("load", async () => {
    await initDataTable();
});