/*
  Configurações padrão Chart.js para painel PEERS
  Paleta de cores, responsividade, tooltips customizados, legendas
*/

const peersPalette = {
  blue: '#011334',
  lime: '#E1FF00',
  serene: '#D8E8EE',
  white: '#FFFFFF',
  gray: '#F5F5F5',
  blue02: '#677185',
  blue03: '#99A1AE',
  blue04: '#CCD0D6',
  lime02: '#F3FF99',
  lime03: '#F9FFCC',
  serene02: '#E8F1F5',
  serene03: '#EFF6F8',
  red: '#EF4444',
  yellow: '#FDE047',
  green: '#22C55E'
};

const chartDefaults = {
  palette: [
    peersPalette.blue,
    peersPalette.lime,
    peersPalette.serene,
    peersPalette.gray,
    peersPalette.blue02,
    peersPalette.blue03,
    peersPalette.lime02,
    peersPalette.red,
    peersPalette.yellow,
    peersPalette.green
  ],
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        labels: {
          color: peersPalette.blue,
          font: {
            family: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif',
            size: 13,
            weight: 'bold'
          },
          boxWidth: 18,
          padding: 18
        }
      },
      tooltip: {
        enabled: true,
        backgroundColor: 'rgba(1, 19, 52, 0.95)',
        borderColor: peersPalette.lime,
        borderWidth: 2,
        titleColor: peersPalette.lime,
        bodyColor: peersPalette.white,
        bodyFont: {
          family: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif',
          size: 13
        },
        padding: 12,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed !== undefined) {
              label += context.parsed;
            }
            return label;
          }
        }
      }
    },
    layout: {
      padding: {
        left: 10,
        right: 10,
        top: 10,
        bottom: 10
      }
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(1,19,52,0.07)'
        },
        ticks: {
          color: peersPalette.blue,
          font: {
            family: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif',
            size: 12
          }
        }
      },
      y: {
        grid: {
          color: 'rgba(1,19,52,0.07)'
        },
        ticks: {
          color: peersPalette.blue,
          font: {
            family: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif',
            size: 12
          }
        }
      }
    }
  },
  pieOptions: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'right',
        labels: {
          color: peersPalette.blue,
          font: {
            family: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif',
            size: 13,
            weight: 'bold'
          },
          boxWidth: 18,
          padding: 18
        }
      },
      tooltip: {
        enabled: true,
        backgroundColor: 'rgba(1, 19, 52, 0.95)',
        borderColor: peersPalette.lime,
        borderWidth: 2,
        titleColor: peersPalette.lime,
        bodyColor: peersPalette.white,
        bodyFont: {
          family: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif',
          size: 13
        },
        padding: 12,
        callbacks: {
          label: function(context) {
            let label = context.label || '';
            let value = context.parsed;
            return `${label}: ${value}`;
          }
        }
      }
    }
  }
};

export { peersPalette, chartDefaults };