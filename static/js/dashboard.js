$(function () {


   // =====================================
  // Profit
  // =====================================
//   var chart = {
//     series: [
//       { name: "Earnings this month:", data: [355, 390, 300, 350, 390, 180, 355, 390] },
//       { name: "Expense this month:", data: [280, 250, 325, 215, 250, 310, 280, 250] },
//     ],

//     chart: {
//       type: "bar",
//       height: 345,
//       offsetX: -15,
//       toolbar: { show: true },
//       foreColor: "#adb0bb",
//       fontFamily: 'inherit',
//       sparkline: { enabled: false },
//     },


//     colors: ["#5D87FF", "#49BEFF"],


//     plotOptions: {
//       bar: {
//         horizontal: false,
//         columnWidth: "35%",
//         borderRadius: [6],
//         borderRadiusApplication: 'end',
//         borderRadiusWhenStacked: 'all'
//       },
//     },
//     markers: { size: 0 },

//     dataLabels: {
//       enabled: false,
//     },


//     legend: {
//       show: false,
//     },


//     grid: {
//       borderColor: "rgba(0,0,0,0.1)",
//       strokeDashArray: 3,
//       xaxis: {
//         lines: {
//           show: false,
//         },
//       },
//     },

//     xaxis: {
//       type: "category",
//       categories: ["16/08", "17/08", "18/08", "19/08", "20/08", "21/08", "22/08", "23/08"],
//       labels: {
//         style: { cssClass: "grey--text lighten-2--text fill-color" },
//       },
//     },


//     yaxis: {
//       show: true,
//       min: 0,
//       max: 400,
//       tickAmount: 4,
//       labels: {
//         style: {
//           cssClass: "grey--text lighten-2--text fill-color",
//         },
//       },
//     },
//     stroke: {
//       show: true,
//       width: 3,
//       lineCap: "butt",
//       colors: ["transparent"],
//     },


//     tooltip: { theme: "light" },

//     responsive: [
//       {
//         breakpoint: 600,
//         options: {
//           plotOptions: {
//             bar: {
//               borderRadius: 3,
//             }
//           },
//         }
//       }
//     ]


//   };

//   var chart = new ApexCharts(document.querySelector("#chart"), chart);
//   chart.render();




  // =====================================
  // Breakup
  // =====================================
// Menunggu dokumen HTML untuk dimuat sepenuhnya
document.addEventListener("DOMContentLoaded", function() {
  // Mendapatkan nilai jumlah_user dari elemen HTML
  var jumlah_user_element = document.getElementById("jumlah_users");
  
  // Memeriksa apakah elemen ditemukan sebelum mencoba mengakses innerText
  if (jumlah_user_element) {
      var jumlah_user = jumlah_user_element.innerText;

      // Objek untuk chart
      var breakup = {
          color: "#adb5bd",
          series: [jumlah_user],
          labels: ["Total Pengguna"],
          chart: {
              width: 180,
              type: "donut",
              fontFamily: "Plus Jakarta Sans', sans-serif",
              foreColor: "#adb0bb",
          },
          plotOptions: {
              pie: {
                  startAngle: 0,
                  endAngle: 360,
                  donut: {
                      size: '75%',
                  },
              },
          },
          stroke: {
              show: false,
          },
          dataLabels: {
              enabled: false,
          },
          legend: {
              show: false,
          },
          colors: ["#5D87FF"],
          responsive: [
              {
                  breakpoint: 991,
                  options: {
                      chart: {
                          width: 150,
                      },
                  },
              },
          ],
          tooltip: {
              theme: "dark",
              fillSeriesColor: false,
          },
      };

      var chart = new ApexCharts(document.querySelector("#jumlah_users"), breakup);
      chart.render();
  } else {
      console.error("Element dengan ID 'jumlah_users' tidak ditemukan.");
  }
});





  // =====================================
  // Earning
  // =====================================
  // Persiapkan data jumlah guru TK, SD, dan SMP yang telah melakukan prediksi
// var dataGuru = [30, 50, 20]; // Misalnya, 30 guru TK, 50 guru SD, dan 20 guru SMP

// // Konfigurasi grafik untuk diagram lingkaran
// var earning = {
//   chart: {
//     id: "sparkline3",
//     type: "pie",
//     height: 150,
//     sparkline: {
//       enabled: true,
//     },
//     group: "sparklines",
//     fontFamily: "Plus Jakarta Sans', sans-serif",
//     foreColor: "#adb0bb",
//   },
//   series: dataGuru,
//   labels: ['TK', 'SD', 'SMP'],
//   stroke: {
//     width: 0,
//   },
//   colors: ["#5D87FF", "#49BEFF", "#1E266D"], 
//   legend: {
//     show: true,
//     position: 'bottom',
//     fontSize: '12px',
//     fontFamily: 'Plus Jakarta Sans, sans-serif',
//     fontWeight: 400,
//     labels: {
//       colors: "#adb0bb"
//     },
//     markers: {
//       width: 12,
//       height: 12,
//       strokeWidth: 0,
//       radius: 12,
//     },
//     itemMargin: {
//       horizontal: 5,
//       vertical: 3
//     }
//   },
//   tooltip: {
//     theme: "dark",
//     fillSeriesColor: false,
//   },
// };

// // Render grafik
// new ApexCharts(document.querySelector("#earning"), earning).render();

 })