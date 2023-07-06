// let dataTable;
// let dataTableIsInitialized = false;

// const dataTableOptions = {
//     lengthMenu: [10, 25, 50, 100, 250, 500],
//     columnDefs: [
//         { className: "centered", targets: [0, 1, 2, 3, 4] },
//         { orderable: false, targets: [2] },
//         { searchable: false, targets: [0, 2] }
//     ],
//     destroy: true,
//     order: [[0, "desc"]],
//     language: {
//         lengthMenu: "Mostrar _MENU_ registros por página",
//         zeroRecords: "Ningún usuario encontrado",
//         info: "Mostrando de _START_ a _END_ de un total de _TOTAL_ registros",
//         infoEmpty: "Ningún usuario encontrado",
//         infoFiltered: "(filtrados desde _MAX_ registros totales)",
//         search: "Buscar:",
//         loadingRecords: "Cargando...",
//         paginate: {
//             first: "Primero",
//             last: "Último",
//             next: "Siguiente",
//             previous: "Anterior"
//         }
//     }
// }

// const initDataTable = async () => {
//     if (dataTableIsInitialized) {
//         dataTable.destroy();
//     }

//     await listPedidos();

//     dataTable = $('#datatable-pedidos').DataTable(dataTableOptions);

//     dataTableIsInitialized = true
// }

// const listPedidos = async () => {
//     try {
//         const response = await fetch('http://127.0.0.1:8000/list_pedidos/');
//         const data = await response.json();

//         let content = ``;
//         data.pedidos.forEach((pedidos, index) => {
//             content += `
//                 <tr>
//                     <td>${index + 1}</td>
//                     <td>${pedidos.nombre}</td>
//                     <td>${pedidos.apellido}</td>
//                     <td>${pedidos.correo}</td>
//                     <td>${pedidos.estado}</td>
//                     <td>${pedidos.tipo_pago}</td>
//                 </tr>
//             `;
//         });
//         tableBody_pedidos.innerHTML = content;
//     } catch (ex) {
//         alert(ex);
//     }
// };

// window.addEventListener("load", async () => {
//     await initDataTable();
// });