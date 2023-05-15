var despachoDomicilio = document.querySelector('.despachoDomicilio');
var retiroTienda = document.querySelector('.retiroTienda');
var despachoRadio = document.getElementById('flexRadioDefault1');
var retiroRadio = document.getElementById('flexRadioDefault2');

despachoRadio.addEventListener('change', function() {
  if (despachoRadio.checked) {
    despachoDomicilio.style.display = 'block';
    retiroTienda.style.display = 'none';
  }
});

retiroRadio.addEventListener('change', function() {
  if (retiroRadio.checked) {
    despachoDomicilio.style.display = 'none';
    retiroTienda.style.display = 'block';
  }
});