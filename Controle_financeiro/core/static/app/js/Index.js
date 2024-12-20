document.addEventListener("DOMContentLoaded", function () {
    const heroImg = document.querySelector(".hero-img");

    function updateHeroImage() {
        if (window.innerWidth <= 992) {
            heroImg.src = "/static/app/images/HelpPocket/Topo_Small.png";
        } else {
            heroImg.src = "/static/app/images/HelpPocket/Topo.png";
        }
    }

    // Verifica o tamanho da tela ao carregar
    updateHeroImage();

    // Monitora o redimensionamento da janela
    window.addEventListener("resize", updateHeroImage);
});


function criarDonutChart(chartId, ganhosTotais, gastosTotais, saldoPeriodo) {
    const dados = {
        labels: ['Ganhos', 'Gastos'],
        datasets: [{
            label: 'Ganhos vs Gastos',
            data: [ganhosTotais, Math.abs(gastosTotais)],
            backgroundColor: ['#28a745', '#dc3545'],

            hoverOffset: 4
        }]
    };
    
    const config = {
        type: 'doughnut',
        data: dados,
        options: {
            responsive: false, // Desabilita o redimensionamento automático
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return 'R$ ' + tooltipItem.raw.toFixed(2);
                        }
                    }
                }
            },
            aspectRatio: 1, // Define a proporção do gráfico (1:1 para circular)
        },
        plugins: [{
            // Plugin customizado para adicionar o saldo no centro
            beforeDraw: function(chart) {
                const ctx = chart.ctx;
                const width = chart.width;
                const height = chart.height;
                const centerX = width / 2;
                const centerY = height / 1.6;

                ctx.restore();
                ctx.font = 'bold 12px Arial';
                ctx.fillStyle = '#000'; // Cor do texto
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText('R$ ' + saldoPeriodo.toFixed(2), centerX, centerY);
                ctx.save();
            }
        }]
    };
    
    var ctx = document.getElementById(chartId).getContext('2d');
    new Chart(ctx, config);
}