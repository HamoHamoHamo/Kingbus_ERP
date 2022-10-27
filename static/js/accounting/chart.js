var chartdata = {
    labels: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
    datasets: [
        {
            label: "일반매출",
            lineTension: 0.1,
            borderColor: 'rgba(255, 99, 132, 0)',
            backgroundColor: '#F69F3C',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            data: [1000, 2000, 3000, 4000]
        }, {
            label: "출/퇴근매출",
            lineTension: 0.1,
            borderColor: 'rgba(255, 199, 132, 0.1)',
            backgroundColor: '#1E64CC',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            data: [1000, 2000, 3000, 4000]
        }, {
            label: "총 매출",
            type: "line",//다중 그래프이기 때문에 기본 bar타입이 아닌 line타입으로 따로 설정해줌. 단일 그래프시 불필요
            lineTension: 0.1,
            borderColor: '#4CAF50',
            backgroundColor: '#4CAF50',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            data: [2000, 4000, 6000, 8000]
        }
    ]
};

var chartOptions = {
    scales: {
        xAxes: [
            {
                ticks: {
                    beginAtZero: true
                },
                scaleLabel: {
                    display: true,
                    labelString: "x축 텍스트",
                    fontColor: "red"
                },
                stacked: true
            }
        ],
        yAxes: [
            {
                scaleLabel: {
                    display: true,
                    labelString: "y축 텍스트",
                    fontColor: "green"
                },
                ticks: {
                    // max: 7000,
                    min: 0,
                    // stepSize: 1000,
                    autoSkip: true
                },
                stacked: true
            }
        ]
    },
    plugins: {
        legend: {
            display: true,
            labels: {
                color: 'black',
                boxWidth: 16,
                boxHeight: 16,
                font: {
                    size: 14
                }
            }
        }
    },
    responsive: true
};

var ctx = document.getElementById("yearChart");
JsChartBar = new Chart(ctx, {
    type: 'bar',
    data: chartdata,
    options: chartOptions
});












const kategoriChart = new Chart(
    document.getElementById('kategoriChart'),
    {
        plugins: [ChartDataLabels], // chartjs-plugin-datalabels 불러오기
        type: 'bar', // 차트 타입 지정
        data: {
            labels: [
                "워크샵", "콘서트, 단체관람", "체험학습, 수학여행", "산악회, 동호회 모임", "결혼식", "기타"
            ],
            datasets: [{
                label: "이용 유형(건)",
                lineTension: 0.1,
                borderColor: 'rgba(255, 99, 132, 0)',
                backgroundColor: '#1E64CC',
                pointBorderColor: "rgba(75,192,192,1)",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                data: [20, 40, 30, 32, 27, 42]
            }]
        },
        options: {
            scales: {
                xAxes: [
                    {
                        ticks: {
                            beginAtZero: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: "x축 텍스트",
                            fontColor: "red"
                        },
                        stacked: true
                    }
                ],
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: "y축 텍스트",
                            fontColor: "green"
                        },
                        ticks: {
                            // max: 7000,
                            min: 0,
                            // stepSize: 1000,
                            autoSkip: true
                        },
                        stacked: true
                    }
                ]
            },
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: 'black',
                        boxWidth: 16,
                        boxHeight: 16,
                        font: {
                            size: 14
                        }
                    },
                    position: "top"
                },
                tooltip: { // 기존 툴팁 사용 안 함
                    enabled: false
                },
                animation: { // 차트 애니메이션 사용 안 함 (옵션)
                    duration: 0,
                },
                datalabels: { // datalables 플러그인 세팅
                    formatter: function (value) {
                        // 출력 텍스트
                        return value;
                    }, // 도넛 차트에서 툴팁이 잘리는 경우 사용
                    color: "black",
                    anchor: "end",
                    align: "end"
                },
            },
            indexAxis: "y",
            responsive: false,
        },
    }
);









const otherChartWay = new Chart(
    document.getElementById('otherChartWay'),
    {
        plugins: [ChartDataLabels], // chartjs-plugin-datalabels 불러오기
        type: 'doughnut', // 차트 타입 지정
        data: {
            labels: [
                '왕복',
                '편도'
            ],
            datasets: [{
                label: 'My First dataset',
                backgroundColor: ["#1E64CC", "#677283"],
                borderColor: 'rgba(255, 255, 255, 1)',
                data: [38, 62],
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: '운행종류',
                    position: "bottom",
                    fontSize: 50,
                    fontColor: "black"
                },
                legend: {
                    display: true,
                    labels: {
                        color: 'black',
                        boxWidth: 20,
                        boxHeight: 20,
                        font: {
                            size: 14
                        }
                    },
                    position: "right"
                },
                animation: { // 차트 애니메이션 사용 안 함 (옵션)
                    duration: 0,
                },
                datalabels: { // datalables 플러그인 세팅
                    formatter: function (value) {
                        // 출력 텍스트
                        return value + '%';
                    },
                    align: 'center', // 도넛 차트에서 툴팁이 잘리는 경우 사용
                    color: "white"
                },
            },
            responsive: false,
        },
    }
);











const otherChartPayment = new Chart(
    document.getElementById('otherChartPayment'),
    {
        plugins: [ChartDataLabels], // chartjs-plugin-datalabels 불러오기
        type: 'doughnut', // 차트 타입 지정
        data: {
            labels: [
                '카드',
                '현금'
            ],
            datasets: [{
                label: 'My First dataset',
                backgroundColor: ["#1E64CC", "#677283"],
                borderColor: 'rgba(255, 255, 255, 1)',
                data: [38, 62],
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: '결재종류',
                    position: "bottom",
                    fontSize: 16,
                    fontColor: "black",
                    fontStyle: "bold"
                },
                legend: {
                    display: true,
                    labels: {
                        color: 'black',
                        boxWidth: 20,
                        boxHeight: 20,
                        font: {
                            size: 14
                        }
                    },
                    position: "right"
                },
                animation: { // 차트 애니메이션 사용 안 함 (옵션)
                    duration: 0,
                },
                datalabels: { // datalables 플러그인 세팅
                    formatter: function (value) {
                        // 출력 텍스트
                        return value + '%';
                    },
                    align: 'center', // 도넛 차트에서 툴팁이 잘리는 경우 사용
                    color: "white"
                },
            },
            responsive: false,
        },
    }
);