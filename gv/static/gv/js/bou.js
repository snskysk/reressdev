var ctx = document.getElementById("ChartDemo").getContext('2d');
var ChartDemo = new Chart(ctx, {
   type: 'bar',
   data: {
      labels: ["Item1", "Item2", "Item3", "Item4", "Item5", "Item6", "Item7"],
      datasets: [
      {
         label: "Chart-1",
         backgroundColor: 'rgb(255, 0, 0)',
         lineTension: 0,
         fill: false,
         data: [20, 26, 12, 43, 33, 21, 29],
      },
      {
      label: "Chart-2",
      lineTension: 0,
      fill: false,
      backgroundColor: 'rgb(0, 0, 255)',
      data: [28, 22, 32, 13, 33, 41, 19],
    },
      ]
   },
   options: {
      responsive: true,
      scales: {
    xAxes: [{
      ticks: { fontSize: 14,},
    }],
    yAxes: [{
      ticks: { fontSize: 18,},
    }],
  },
   }
});
