// dashboard.js
// Funções para painel de tokens multi-agente

const chartIds = [
    'chart1', 'chart2', 'chart3', 'chart4', 'chart5', 'chart6', 'chart7', 'chart8', 'chart9'
];
const chartConfigs = [
    { title: 'Tokens de Entrada por Projeto', metric: 'tokens_entrada', group: 'projeto' },
    { title: 'Tokens de Saída por Projeto', metric: 'tokens_saida', group: 'projeto' },
    { title: 'Tokens de Entrada por Agente', metric: 'tokens_entrada', group: 'usuario_executor' },
    { title: 'Tokens de Saída por Agente', metric: 'tokens_saida', group: 'usuario_executor' },
    { title: 'Tokens de Entrada por Período', metric: 'tokens_entrada', group: 'data_hora' },
    { title: 'Tokens de Saída por Período', metric: 'tokens_saida', group: 'data_hora' },
    { title: 'Tokens por Modelo LLM', metric: 'tokens_entrada', group: 'model_name' },
    { title: 'Tokens por Modelo LLM por Período', metric: 'tokens_entrada', group: 'model_name_periodo' },
    { title: 'Agrupamento por Usuário', metric: 'all', group: 'usuario_executor' }
];

let chartType = 'bar'; // Default
let charts = {};

// Função para buscar dados do backend
async function fetchTokenData(queryParams = {}) {
    // Exemplo de endpoint: /api/tokens?startDate=...&endDate=...&project=...&user=...&model=...
    const url = new URL('/api/tokens', window.location.origin);
    Object.entries(queryParams).forEach(([key, value]) => {
        if (value) url.searchParams.append(key, value);
    });
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Erro ao buscar dados');
        return await response.json();
    } catch (err) {
        console.error('Erro na busca dos dados:', err);
        return null;
    }
}

// Função para renderizar gráfico Chart.js
function renderChart(canvasId, data, chartType, config) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }
    let chartData, options;
    if (chartType === 'pie') {
        chartData = {
            labels: data.labels,
            datasets: [{
                label: config.title,
                data: data.values,
                backgroundColor: [
                    '#011334', '#E1FF00', '#D8E8EE', '#F5F5F5', '#677185', '#99A1AE', '#CCD0D6', '#F3FF99', '#F9FFCC', '#EFF6F8'
                ],
                borderColor: '#fff',
                borderWidth: 2
            }]
        };
        options = {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: { enabled: true }
            }
        };
    } else {
        chartData = {
            labels: data.labels,
            datasets: [{
                label: config.title,
                data: data.values,
                backgroundColor: 'rgba(1,19,52,0.2)',
                borderColor: '#011334',
                borderWidth: 2
            }]
        };
        options = {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: true }
            },
            scales: {
                x: { ticks: { color: '#011334', font: { size: 12 } } },
                y: { beginAtZero: true, ticks: { color: '#011334', font: { size: 12 } } }
            }
        };
    }
    charts[canvasId] = new Chart(ctx, {
        type: chartType,
        data: chartData,
        options: options
    });
}

// Função para atualizar todos os gráficos
async function updateAllCharts() {
    const queryParams = getFilterParams();
    const rawData = await fetchTokenData(queryParams);
    if (!rawData) return;
    chartConfigs.forEach((config, idx) => {
        const chartData = prepareChartData(rawData, config);
        renderChart(chartIds[idx], chartData, chartType, config);
    });
}

// Função para capturar filtros do formulário
function getFilterParams() {
    return {
        startDate: document.getElementById('startDate').value,
        endDate: document.getElementById('endDate').value,
        project: document.getElementById('projectFilter').value,
        user: document.getElementById('userFilter').value,
        model: document.getElementById('modelFilter').value
    };
}

// Função para preparar dados para cada gráfico
function prepareChartData(rawData, config) {
    // Exemplo: agrupar e somar tokens por campo
    let groupField = config.group;
    let metricField = config.metric;
    let labels = [], values = [];
    if (groupField === 'model_name_periodo') {
        // Agrupamento por modelo e período
        const grouped = {};
        rawData.forEach(item => {
            const key = item.model_name + ' - ' + item.data_hora.slice(0, 10);
            grouped[key] = (grouped[key] || 0) + (item.tokens_entrada || 0);
        });
        labels = Object.keys(grouped);
        values = Object.values(grouped);
    } else if (metricField === 'all') {
        // Agrupamento por usuário, somando tokens de entrada e saída
        const grouped = {};
        rawData.forEach(item => {
            const key = item.usuario_executor || 'N/A';
            grouped[key] = (grouped[key] || 0) + (item.tokens_entrada || 0) + (item.tokens_saida || 0);
        });
        labels = Object.keys(grouped);
        values = Object.values(grouped);
    } else if (groupField === 'data_hora') {
        // Agrupamento por data
        const grouped = {};
        rawData.forEach(item => {
            const key = item.data_hora.slice(0, 10);
            grouped[key] = (grouped[key] || 0) + (item[metricField] || 0);
        });
        labels = Object.keys(grouped);
        values = Object.values(grouped);
    } else {
        // Agrupamento padrão
        const grouped = {};
        rawData.forEach(item => {
            const key = item[groupField] || 'N/A';
            grouped[key] = (grouped[key] || 0) + (item[metricField] || 0);
        });
        labels = Object.keys(grouped);
        values = Object.values(grouped);
    }
    return { labels, values };
}

// Função para lidar com mudança de filtros
function handleFilterChange() {
    chartType = document.getElementById('chartType').value;
    updateAllCharts();
}

// Event listeners
window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('applyFiltersBtn').addEventListener('click', handleFilterChange);
    document.getElementById('chartType').addEventListener('change', handleFilterChange);
    updateAllCharts();
});
