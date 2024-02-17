var chartDom = document.getElementById('trend-cat');
var myChart = echarts.init(chartDom);
var option;

setTimeout(function () {
  option = {
    title: {
      text: 'Errors by Category over Time',
      left: 'center',
      top: 10
    },
    legend: {
      top: 260,
    },
    tooltip: {
      trigger: 'axis',
    },
    dataset: {
      source: [
        ['category', '2024.Q1', '2024.Q2', '2024.Q3', '2024.Q4', '2025.Q1', '2025.Q2'],
        ['Perceivable', 30628, 31252, 30946, 29432, 28642, 26532],
        ['Operable', 7821, 7615, 7951, 8046, 8364, 8943],
        ['Understandable', 7018, 6953, 6882, 6725, 6702, 6620],
        ['Robust', 422, 402, 435, 422, 403, 412]
      ]
    },
    xAxis: {
      type: 'category',
      // boundaryGap: false
    },
    yAxis: { gridIndex: 0 },
    grid: {
      width: 450,
      top: 300,
      bottom: 30,
      left: 63
    },
    series: [
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        animationDuration: 600,
        emphasis: {
          focus: 'series'
        }
      },
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        animationDuration: 600,
        emphasis: { focus: 'series' }
      },
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        animationDuration: 600,
        emphasis: { focus: 'series' }
      },
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        animationDuration: 600,
        emphasis: { focus: 'series'}
      },
      {
        type: 'pie',
        id: 'pie',
        radius: '28%',
        animationDuration: 600,
        animationDurationUpdate: 200,
        selectedMode: 'single',
        center: ['50%', '27%'],
        emphasis: {
          itemStyle: {
            focus: 'self',
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        label: {
          fontSize: 13,
          formatter: '{b}: \n{@2024.Q1} ({d}%)'
        },
        encode: {
          itemName: 'category',
          value: '2024.Q1',
          tooltip: '2024.Q1'
        }
      }
    ]
  };
  myChart.on('updateAxisPointer', function (event) {
    const xAxisInfo = event.axesInfo[0];
    if (xAxisInfo) {
      const dimension = xAxisInfo.value + 1;
      myChart.setOption({
        series: {
          id: 'pie',
          label: {
            formatter: '{b}: \n{@[' + dimension + ']} ({d}%)'
          },
          encode: {
            value: dimension,
            tooltip: dimension
          }
        }
      });
    }
  });
  myChart.setOption(option);
});

option && myChart.setOption(option);