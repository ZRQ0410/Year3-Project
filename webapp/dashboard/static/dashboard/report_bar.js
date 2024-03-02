var chartDom = document.getElementById('report-bar');
var myChart = echarts.init(chartDom);
var option;

const num_err = JSON.parse(document.getElementById('num_err').textContent);
const num_likely = JSON.parse(document.getElementById('num_likely').textContent);
const num_potential = JSON.parse(document.getElementById('num_potential').textContent);

option = {
  title: {
    text: 'Number of Errors',
    left: 'center',
    top: 20
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow',
    }
  },
  xAxis: {
    type: 'category',
    data: ['Error', 'Likely Problem', 'Potential Problem'],
    axisTick: {
      alignWithLabel: true
    },
    axisLabel: { interval: 0, rotate: 0 }
  },
  yAxis: {
    type: 'value'
  },
  grid: {
    bottom: 20,
  },
  series: [
    {
      data: [
        {
          value: num_err,
          itemStyle: {
            color: '#ee6666'
          }
        },
        {
          value: num_likely,
          itemStyle: {
            color: '#fac858'
          }
        },
        {
          value: num_potential,
          itemStyle: {
            color: '#5470c6'
          }
        },
      ],
      type: 'bar'
    }
  ]
};

option && myChart.setOption(option);
