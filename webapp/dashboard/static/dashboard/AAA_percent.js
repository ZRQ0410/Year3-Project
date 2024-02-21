var chartDom = document.getElementById('AAA-percent');
var myChart = echarts.init(chartDom);
var option;

const result_district = JSON.parse(document.getElementById('result_district').textContent);
const AAA_percent = [];
for (const [key, value] of Object.entries(result_district)) {
  AAA_percent.push({'name': key, 'value': value['AAA_percent'].toFixed(2)});
}

myChart.showLoading();
// https://martinjc.github.io/UK-GeoJSON/
// in attributes (geojson): convert the key of the name value into 'name'!
// otherwise echarts will not be able to recognize the name of each region
$.get('../static/dashboard/local_admin.json', function (geoJson) {
  myChart.hideLoading();
  echarts.registerMap('England', geoJson);

  option = {
    title: {
      text: 'Percentage that Meet AAA Conformance',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      showDelay: 0,
      transitionDuration: 0.2,
    },
    visualMap: {
      left: 40,
      top: 270,
      min: 0,
      max: 1,
      inRange: {
        color: [
          '#f46d43',
          '#fdae61',
          '#fee090',
          '#ffffbf',
          '#e0f3f8',

          '#c3deee',
          '#abd9e9',
          '#9ec6e6',
          '#8fbedc',
          '#6592cd',
          '#476185',
        ]
      },
      text: ['High', 'Low'],
      calculable: true
    },
    toolbox: {
      show: true,
      orient: 'vertical',
      left: 'right',
      top: 50,
      feature: {
        dataView: { readOnly: false },
        restore: {},
        saveAsImage: {}
      }
    },
    series: [
      {
        name: 'Percentage (AAA)',
        type: 'map',
        map: 'England',
        roam: true,
        left: 'center',
        top: 35,
        width: '88%',
        emphasis: {
          label: {
            show: true,
            backgroundColor: 'white'
          },
        },
        
        data: AAA_percent
      }
    ]
  };
  myChart.setOption(option);
});

option && myChart.setOption(option);


