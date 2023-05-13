const domicilioRadio = document.getElementById('domicilio');
const retiroRadio = document.getElementById('retiro');

const calleDiv = document.getElementById('calle-div');
const numeroCalleDiv = document.getElementById('numeroCalle-div');
const regionDiv = document.getElementById('region-div');
const tiendaDiv = document.getElementById('tienda-div');

domicilioRadio.addEventListener('change', () => {
  calleDiv.style.display = 'block';
  numeroCalleDiv.style.display = 'block';
  regionDiv.style.display = 'block';
  tiendaDiv.style.display = 'none';
});

retiroRadio.addEventListener('change', () => {
  calleDiv.style.display = 'none';
  numeroCalleDiv.style.display = 'none';
  regionDiv.style.display = 'none';
  tiendaDiv.style.display = 'block';
});