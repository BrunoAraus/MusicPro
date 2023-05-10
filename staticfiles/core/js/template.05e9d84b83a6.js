const icono = document.querySelector('.logoEnlace1');
const miDiv = document.querySelector('.contenidoCarrito');

icono.addEventListener('mouseenter', function() {
  miDiv.style.display = 'block';
});

miDiv.addEventListener('mouseleave', function() {
  miDiv.style.display = 'none';
});



