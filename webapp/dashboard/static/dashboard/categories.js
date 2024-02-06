var chartDom = document.getElementById('categories');
var myChart = echarts.init(chartDom);
var option;

const result_overall = JSON.parse(document.getElementById('result_overall').textContent);
const categories = [];
categories.push({'name': 'Perceivable', 'value': Number(result_overall['num_p'])});
categories.push({'name': 'Operable', 'value': Number(result_overall['num_o'])});
categories.push({'name': 'Understandable', 'value': Number(result_overall['num_u'])});
categories.push({'name': 'Robust', 'value': Number(result_overall['num_r'])});

option = {
  title: {
    text: 'Pencentage of Error Categories',
    left: 'center',
    top: 30
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'horizontal',
    left: 'center',
    bottom: 40
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: '50%',
      selectedMode: 'single',
      data: categories,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
};

option && myChart.setOption(option);
