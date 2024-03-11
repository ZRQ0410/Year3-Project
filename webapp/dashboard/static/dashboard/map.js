var chartDom = document.getElementById('lad-map');
var myChart = echarts.init(chartDom);
var option;

const districts = JSON.parse(document.getElementById('districts').textContent);
const data = [];
for (const d of districts) {
    data.push({'name': d, 'value': 1});
}

myChart.showLoading({maskColor: '#f5f6ff'});
// https://martinjc.github.io/UK-GeoJSON/
// in attributes (geojson): convert the key of the name value into 'name'!
// otherwise echarts will not be able to recognize the name of each region
$.get('../../static/dashboard/local_admin.json', function (geoJson) {
  myChart.hideLoading();
  echarts.registerMap('England', geoJson);

  option = {
    backgroundColor: '#f5f6ff',
    tooltip: {
      trigger: 'item',
      showDelay: 0,
      transitionDuration: 0.2,
      formatter: '{b}',
    },
    visualMap: {
      show: false,
      left: 40,
      top: 270,
      min: 0,
      max: 60,
      inRange: {
        color: [
          '#9ec6e6',
          // '#c3deee',
          // '#e0f3f8',
          // '#ffffbf',
        ]
      },
      // text: ['High', 'Low'],
      // calculable: true
    },
    toolbox: {
      show: true,
      orient: 'vertical',
      left: 25,
      top: 150,
      feature: {
        dataView: { readOnly: false },
        restore: {},
        saveAsImage: {}
      }
    },
    series: [
      {
        type: 'map',
        map: 'England',
        roam: true,
        left: 0,
        top: 15,
        width: '95%',
        emphasis: {
          itemStyle: {
            areaColor: '#f6ebb6'
        },
          label: {
            show: false,
            backgroundColor: 'white'
          },
        },
        select: 'disabled',
        data: data
      }
    ]
  };
  myChart.setOption(option);
  myChart.on('click', function(args) {
    if (districts.includes(args.data.name)) {
      // remove punctuation, replace whitespace with -
      // var punctuation = /[\.,?!]/g;
      // var s = args.data.name.replace(punctuation, "").replace(/ /g,"-");;
      location.href = '/gp-detail/lad/' + args.data.name;
    }
})
});

option && myChart.setOption(option);
