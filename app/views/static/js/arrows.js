document.addEventListener('DOMContentLoaded', function(){
var activeFilter = null;


function refreshRow(row){
var track = row.querySelector('.category-products');
var prev = row.querySelector('.scroll-prev');
var next = row.querySelector('.scroll-next');
if(!track) return;
// força recálculo após layout
requestAnimationFrame(function(){
var maxScroll = Math.max(0, track.scrollWidth - track.clientWidth - 1);
// garante que, ao mostrar a fileira, o scrollLeft esteja válido
if(track.scrollLeft > maxScroll) track.scrollLeft = maxScroll;
if(prev) prev.style.display = track.scrollLeft > 5 ? 'inline-flex' : 'none';
if(next) next.style.display = track.scrollLeft < maxScroll ? 'inline-flex' : 'none';
});
}


// inicializa setas por fileira
document.querySelectorAll('.category-row').forEach(function(row){
var track = row.querySelector('.category-products');
var prev = row.querySelector('.scroll-prev');
var next = row.querySelector('.scroll-next');
if(!track) return;
var scrollAmount = Math.round(track.clientWidth * 0.7) || 600;
if(prev) prev.addEventListener('click', function(){ track.scrollBy({ left: -scrollAmount, behavior: 'smooth' }); setTimeout(function(){ refreshRow(row); }, 260); });
if(next) next.addEventListener('click', function(){ track.scrollBy({ left: scrollAmount, behavior: 'smooth' }); setTimeout(function(){ refreshRow(row); }, 260); });
// atualizar setas ao rolar
track.addEventListener('scroll', function(){ refreshRow(row); });
// recalcular resize
window.addEventListener('resize', function(){ scrollAmount = Math.round(track.clientWidth * 0.7) || 600; refreshRow(row); });
// primeira atualização
refreshRow(row);
});


// lógica de filtro: mostra apenas a fileira selecionada; click no mesmo filtro mostra todas
document.querySelectorAll('.filter-btn').forEach(function(btn){
btn.addEventListener('click', function(){
var filter = btn.getAttribute('data-filter');
// toggle
if(activeFilter === filter){
activeFilter = null;
document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
document.querySelectorAll('.category-row').forEach(function(r){ r.style.display = ''; refreshRow(r); });
return;
}
activeFilter = filter;
document.querySelectorAll('.filter-btn').forEach(b=>b.classList.toggle('active', b===btn));
// esconde todas e mostra apenas a filtrada
document.querySelectorAll('.category-row').forEach(function(r){
if(r.id === 'category-' + filter){ r.style.display = ''; /* mostra */ setTimeout(function(){ refreshRow(r); }, 60); }
else { r.style.display = 'none'; }
});
});
});


// caso a página carregue já com uma altura estranha, força refresh geral
setTimeout(function(){ document.querySelectorAll('.category-row').forEach(refreshRow); }, 120);
});