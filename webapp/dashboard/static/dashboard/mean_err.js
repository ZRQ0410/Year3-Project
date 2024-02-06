var chartDom = document.getElementById('mean-err');
var myChart = echarts.init(chartDom);
var option;

const result_district = JSON.parse(document.getElementById('result_district').textContent);
// const result_overall = JSON.parse(document.getElementById('result_overall').textContent);
const mean_err = [];
for (const [key, value] of Object.entries(result_district)) {
    mean_err.push({'name': key, 'value': value['mean_err'].toFixed(2)});
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
      text: 'Average Number of Accessibility Problems',
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
      max: 60,
      inRange: {
        color: [
          '#476185',
          '#6592cd',
          '#8fbedc',
          '#9ec6e6',
          '#abd9e9',
          '#c3deee',
          
          '#e0f3f8',
          '#ffffbf',
          '#fee090',
          '#fdae61',
          '#f46d43',
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
        name: 'Mean',
        type: 'map',
        map: 'England',
        roam: true,
        left: 'center',
        top: 35,
        width: '88%',
        emphasis: {
          label: {
            show: true,
          },
        },
        
        data: mean_err
      }
    ]
  };
  myChart.setOption(option);
});

option && myChart.setOption(option);


