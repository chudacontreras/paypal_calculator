document.getElementById('calculatorForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error');
    
    try {
        const response = await fetch('/calculate/', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Error en el cálculo');
        }
        
        // Mostrar resultados
        document.getElementById('fee').textContent = `$${parseFloat(data.fee).toFixed(2)}`;
        document.getElementById('netAmount').textContent = `$${parseFloat(data.net_amount).toFixed(2)}`;
        
        resultsDiv.classList.remove('hidden');
        errorDiv.classList.add('hidden');
    } catch (error) {
        // Mostrar error
        errorDiv.textContent = error.message;
        errorDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');
    }
});