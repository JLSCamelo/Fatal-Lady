function toggleDetails(pedidoId) {
    const detailsElement = document.getElementById(`details-${pedidoId}`);
    
    if (detailsElement) {
        detailsElement.classList.toggle('hidden');
        
        const button = event.target;
        if (detailsElement.classList.contains('hidden')) {
            button.textContent = 'Ver Detalhes';
        } else {
            button.textContent = 'Ocultar Detalhes';
        }
    }
}