var chartDom = document.getElementById('trend-err');
var myChart = echarts.init(chartDom);
var option;

const quarterCount = 6;
const categoryCount = 6;
const xAxisData = ['Error', 'Likely', 'Potential', 'Error A', 'Error AA', 'Error AAA'];
const customData = [];
const legendData = ['trend', '2024.Q1', '2024.Q2', '2024.Q3', '2024.Q4', '2025.Q1', '2025.Q2'];
const dataList = [
    // rows: quarters, columns: types of errors
    [45889, 108843, 482374, 21301, 16343, 8245],
    [43681, 104225, 472035, 22460, 13205, 8016],
    [49427, 105831, 454369, 25642, 15439, 8346],
    [48643, 107353, 465318, 24531, 15677, 8435],
    [47257, 104435, 475246, 22645, 16492, 8120],
    [42178, 102346, 463159, 18643, 15348, 8187],
];
const encodeY = [];
for (var i = 0; i < quarterCount; i++) {
  encodeY.push(1 + i);
}
for (var i = 0; i < categoryCount; i++) {
  var customVal = [i];
  customData.push(customVal);
  for (var j = 0; j < dataList.length; j++) {
    var value = dataList[j][i];
    dataList[j].push(value);
    customVal.push(value);
  }
}
option = {
  title: {
    text: 'Number of Errors over Time',
    left: 'center',
    top: 10
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
        type: 'shadow'
    }
  },
  legend: {
    data: legendData,
    top: 50
  },
  dataZoom: [
    {
      type: 'slider',
      start: 0,
      end: 30
    },
    {
      type: 'inside',
      start: 50,
      end: 70
    }
  ],
  grid: {
    top: 120,
    left: '12%',
    width: '80%'
  },
  xAxis: {
    data: xAxisData
  },
  yAxis: {},
  series: [
    {
      type: 'custom',
      name: 'trend',
      renderItem: function (params, api) {
        var xValue = api.value(0);
        var currentSeriesIndices = api.currentSeriesIndices();
        var barLayout = api.barLayout({
          barGap: '30%',
          barCategoryGap: '20%',
          count: currentSeriesIndices.length - 1
        });
        var points = [];
        for (var i = 0; i < currentSeriesIndices.length; i++) {
          var seriesIndex = currentSeriesIndices[i];
          if (seriesIndex !== params.seriesIndex) {
            var point = api.coord([xValue, api.value(seriesIndex)]);
            point[0] += barLayout[i - 1].offsetCenter;
            point[1] -= 15;
            points.push(point);
          }
        }
        var style = api.style({
          stroke: api.visual('color'),
          fill: 'none'
        });
        return {
          type: 'polyline',
          shape: {
            points: points
          },
          style: style
        };
      },
      itemStyle: {
        borderWidth: 2
      },
      encode: {
        x: 0,
        y: encodeY
      },
      data: customData,
      z: 100,
      tooltip: {
        show: false
      }
    },
    ...dataList.map(function (data, index) {
      return {
        type: 'bar',
        animation: false,
        name: legendData[index + 1],
        itemStyle: {
          opacity: 0.6
        },
        data: data
      };
    })
  ]
};

option && myChart.setOption(option);