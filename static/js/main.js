// Sistema PDV - JavaScript com mÃ¡scaras
document.addEventListener('DOMContentLoaded', function() {
    console.log('Sistema PDV carregado com mÃ¡scaras!');

    // Auto-hide messages
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-success');
        alerts.forEach(alert => {
            alert.style.display = 'none';
        });
    }, 5000);

    // FormataÃ§Ã£o de CPF/CNPJ
    function formatCpfCnpj(input) {
        let value = input.value.replace(/\D/g, '');
        if (value.length <= 11) {
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
        } else {
            value = value.replace(/^(\d{2})(\d)/, '$1.$2');
            value = value.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
            value = value.replace(/\.(\d{3})(\d)/, '.$1/$2');
            value = value.replace(/(\d{4})(\d)/, '$1-$2');
        }
        input.value = value;
    }

    // Aplicar mÃ¡scaras automaticamente
    const cpfInputs = document.querySelectorAll('input[name*="cpf"], input[placeholder*="CPF"]');
    cpfInputs.forEach(input => {
        input.addEventListener('input', () => formatCpfCnpj(input));
    });
});
