var chartDom = document.getElementById('top-err');
var myChart = echarts.init(chartDom);
var option;

const result_overall = JSON.parse(document.getElementById('result_overall').textContent);
const num_A_err = result_overall['num_A_err'];
const num_AA_err = result_overall['num_AA_err'];
const num_AAA_err = result_overall['num_AAA_err'];

const top_A = result_overall['top_A_err'];
const top_AA = result_overall['top_AA_err'];
const top_AAA = result_overall['top_AAA_err'];
const colors = {'A': '#ee6666', 'AA': '#fac858', 'AAA': '#73c0de'};

option = {
  tooltip: {
    formatter(params) {
      return `
      Level ${params.data.groupId} </br>
      <strong>${params.data.value}</strong>`;
    },
    axisPointer: {
      type: 'shadow',
    }
  },
  grid: {
    bottom: 50,
  },
  xAxis: {
    name: null,
    data: ['A', 'AA', 'AAA']
  },
  yAxis: {},
  dataGroupId: '',
  animationDurationUpdate: 500,
  series: {
    type: 'bar',
    data: [
      {
        value: num_A_err,
        itemStyle: {
          color: colors['A']
        },
        groupId: 'A'
      },
      {
        value: num_AA_err,
        itemStyle: {
          color: colors['AA']
        },
        groupId: 'AA'
      },
      {
        value: num_AAA_err,
        itemStyle: {
          color: colors['AAA']
        },
        groupId: 'AAA'
      }
    ],
    universalTransition: {
      enabled: true,
      divideShape: 'clone'
    }
  },
  graphic: [
    {
      id: 'title_1',
      type: 'text',
      left: 'center',
      top: 18,
      style: {
        text: 'Number of Errors in Each Level',
        fontSize: 18,
        fontFamily: 'Microsoft YaHei',
        fontWeight: 'bold'
      }
    }]
};
const drilldownData = [
  {
    dataGroupId: 'A',
    data: [
      [top_A[0]['id'], top_A[0]['num']],
      [top_A[1]['id'], top_A[1]['num']],
      [top_A[2]['id'], top_A[2]['num']],
      [top_A[3]['id'], top_A[3]['num']],
      [top_A[4]['id'], top_A[4]['num']],
    ]
  },
  {
    dataGroupId: 'AA',
    data: [
      [top_AA[0]['id'], top_AA[0]['num']],
      [top_AA[1]['id'], top_AA[1]['num']],
      [top_AA[2]['id'], top_AA[2]['num']],
      [top_AA[3]['id'], top_AA[3]['num']],
      [top_AA[4]['id'], top_AA[4]['num']],
    ]
  },
  {
    dataGroupId: 'AAA',
    data: [
      [top_AAA[0]['id'], top_AAA[0]['num']],
      [top_AAA[1]['id'], top_AAA[1]['num']],
      [top_AAA[2]['id'], top_AAA[2]['num']],
      [top_AAA[3]['id'], top_AAA[3]['num']],
      [top_AAA[4]['id'], top_AAA[4]['num']],
    ]
  }
];
myChart.on('click', function (event) {
  if (event.data) {
    var subData = drilldownData.find(function (data) {
      return data.dataGroupId === event.data.groupId;
    });
    if (!subData) {
      return;
    }
    myChart.setOption({
      tooltip: {
        extraCssText: 'max-width:240px;max-height:300px;white-space:normal',
        formatter(params) {
          return `
          ${params.data.title} </br>
          <b>Number:</b> ${params.data.value}`;
        },
        axisPointer: {
          type: 'shadow',
        }
      },
      xAxis: {
        name: 'Issue ID',
        nameGap: 25,
        nameLocation: 'center',
        data: subData.data.map(function (item) {
          return item[0];

        })
      },
      series: {
        type: 'bar',
        color: colors[subData.dataGroupId],
        dataGroupId: subData.dataGroupId,
        data: get_descr(subData.dataGroupId),
        universalTransition: {
          enabled: true,
          divideShape: 'clone'
        }
      },
      graphic: [
        {
          id: 'title_1',
          $action: 'remove'
        },
        {
          id: 'title_2',
          type: 'text',
          left: 'center',
          top: 18,
          style: {
            text: 'Top 5 Errors in ' + subData.dataGroupId + ' Level',
            fontSize: 18,
            fontFamily: 'Microsoft YaHei',
            fontWeight: 'bold'
          },
        },
        {
          id: 'text1',
          type: 'text',
          left: 50,
          top: 20,
          style: {
            text: 'Back',
            fontSize: 16,
            fontFamily: 'Microsoft YaHei'
          },
          onclick: function () {
            myChart.setOption(option);
            myChart.setOption({graphic: [{id:'text1', $action: 'remove'}, {id:'title_2', $action: 'remove'}]});
          }
        },
      ], 
    });
  }
});

function get_descr(groupId) {
  var data = [];
  if (groupId === 'A') {
    for (const i of top_A) {
      var content = '<b>ID:</b> ' + i['id'] + '</br><b>SC:</b> ' + i['sc'] + '</br><b>Error:</b> ' + i['msg'] + '</br><b>Description:</b> ' + i['descr']
      data.push({title: content, value: i['num']})
    }
  }
  else if (groupId === 'AA') {
    for (const i of top_AA) {
      var content = '<b>ID:</b> ' + i['id'] + '</br><b>SC:</b> ' + i['sc'] + '</br><b>Error:</b> ' + i['msg'] + '</br><b>Description:</b> ' + i['descr']
      data.push({title: content, value: i['num']})
    }
  }
  else if (groupId === 'AAA') {
    for (const i of top_AAA) {
      var content = '<b>ID:</b> ' + i['id'] + '</br><b>SC:</b> ' + i['sc'] + '</br><b>Error:</b> ' + i['msg'] + '</br><b>Description:</b> ' + i['descr']
      data.push({title: content, value: i['num']})
    }
  }
  return data;
}

option && myChart.setOption(option);
