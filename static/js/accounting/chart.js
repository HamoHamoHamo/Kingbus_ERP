const totalSalsValue = document.querySelector(".totalSalsValue")
const orderSalseValue = document.querySelector(".orderSalseBox .SalseValue")
const regularlySalseValue = document.querySelector(".regularlySalseBox .SalseValue")
const orderAccountsReceivableValue = document.querySelector(".orderAccountsReceivableBox .accountsReceivableValue")
const regularlyAccountsReceivableValue = document.querySelector(".regularlyAccountsReceivableBox .accountsReceivableValue")
const count = document.querySelectorAll(".kategoriData tr td:nth-child(2)")
const busCount = document.querySelectorAll(".kategoriData tr td:nth-child(3)")
const amount = document.querySelectorAll(".kategoriData tr td:nth-child(4)")
const createTable = document.querySelector(".createTable")


function monthAmount() {
    orderSalseValue.innerText = monthlySales.order_sales
    regularlySalseValue.innerText = monthlySales.regularly_sales
    orderAccountsReceivableValue.innerText = monthlySales.order_outstanding
    regularlyAccountsReceivableValue.innerText = monthlySales.regularly_outstanding
    totalSalsValue.innerText = parseInt(orderSalseValue.innerText) + parseInt(regularlySalseValue.innerText)
    orderSalseValue.innerText = `${orderSalseValue.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")} 원`;
    regularlySalseValue.innerText = `${regularlySalseValue.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")} 원`;
    orderAccountsReceivableValue.innerText = `${orderAccountsReceivableValue.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")} 원`;
    regularlyAccountsReceivableValue.innerText = `${regularlyAccountsReceivableValue.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")} 원`;
    totalSalsValue.innerText = `${totalSalsValue.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")} 원`;
}

monthAmount()

function yearChart() {
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
                data: [yearlySales[0].order_sales, yearlySales[1].order_sales, yearlySales[2].order_sales, yearlySales[3].order_sales, yearlySales[4].order_sales, yearlySales[5].order_sales, yearlySales[6].order_sales, yearlySales[7].order_sales, yearlySales[8].order_sales, yearlySales[9].order_sales, yearlySales[10].order_sales, yearlySales[11].order_sales]
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
                data: [yearlySales[0].regularly_sales, yearlySales[1].regularly_sales, yearlySales[2].regularly_sales, yearlySales[3].regularly_sales, yearlySales[4].regularly_sales, yearlySales[5].regularly_sales, yearlySales[6].regularly_sales, yearlySales[7].regularly_sales, yearlySales[8].regularly_sales, yearlySales[9].regularly_sales, yearlySales[10].regularly_sales, yearlySales[11].regularly_sales]
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
                data: [yearlySales[0].total_sales, yearlySales[1].total_sales, yearlySales[2].total_sales, yearlySales[3].total_sales, yearlySales[4].total_sales, yearlySales[5].total_sales, yearlySales[6].total_sales, yearlySales[7].total_sales, yearlySales[8].total_sales, yearlySales[9].total_sales, yearlySales[10].total_sales, yearlySales[11].total_sales]
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
}

yearChart()









function orderType() {
    let keyArr = []
    let valueArr = []
    for (i = 0; i < Object.keys(order.bus_cnt).length; i++){
        keyArr.push(Object.keys(order.bus_cnt)[i])
        valueArr.push(Object.values(order.bus_cnt)[i])
    };
    
    const kategoriChart = new Chart(
        document.getElementById('kategoriChart'),
        {
            plugins: [ChartDataLabels], // chartjs-plugin-datalabels 불러오기
            type: 'bar', // 차트 타입 지정
            data: {
                labels: keyArr,
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
                    data: valueArr
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
                        color: "white",
                    },
                },
                indexAxis: "y",
                responsive: false,
            },
        }
    );
}

orderType()




function table() {
    let nameArr = []
    let countArr = []
    let busArr = []
    let amountArr = []
    for (i = 0; i < Object.keys(order.bus_cnt).length; i++){
        nameArr.push(Object.keys(order.bus_cnt)[i])
        countArr.push(Object.values(order.type_cnt)[i])
        busArr.push(Object.values(order.bus_cnt)[i])
        let amount = Object.values(order.sales)[i]
        amount = amount.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
        amountArr.push(amount)
    };
    for (i = 0; i < Object.keys(order.bus_cnt).length; i++){
        const orderTr = document.createElement("tr")
        orderTr.setAttribute("class", "table-list_body-tr")
        createTable.appendChild(orderTr)

        const orderTd1 = document.createElement("td")
        orderTd1.setAttribute("class", "table-list_body-tr_td")
        orderTd1.innerText = nameArr[i]
        orderTr.appendChild(orderTd1)

        const orderTd2 = document.createElement("td")
        orderTd2.setAttribute("class", "table-list_body-tr_td")
        orderTd2.innerText = countArr[i]
        orderTr.appendChild(orderTd2)

        const orderTd3 = document.createElement("td")
        orderTd3.setAttribute("class", "table-list_body-tr_td")
        orderTd3.innerText = busArr[i]
        orderTr.appendChild(orderTd3)

        const orderTd4 = document.createElement("td")
        orderTd4.setAttribute("class", "table-list_body-tr_td")
        orderTd4.innerText = amountArr[i]
        orderTr.appendChild(orderTd4)
    };
    
}
table()






function driveType() {
    const otherChartWay = new Chart(
        document.getElementById('otherChartWay'),
        {
            plugins: [ChartDataLabels], // chartjs-plugin-datalabels 불러오기
            type: 'doughnut', // 차트 타입 지정
            data: {
                labels: [
                    '출근',
                    '일반',
                    '퇴근'
                ],
                datasets: [{
                    label: 'My First dataset',
                    backgroundColor: ["#1E64CC", "#677283", "#61B4E5"],
                    borderColor: 'rgba(255, 255, 255, 1)',
                    data: [workTypeCnt.attendance, workTypeCnt.order, workTypeCnt.leave],
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
                            return value;
                        },
                        align: 'center', // 도넛 차트에서 툴팁이 잘리는 경우 사용
                        color: "white"
                    },
                },
                responsive: false,
            },
        }
    );
}

driveType()











function payment() {
    const otherChartPayment = new Chart(
        document.getElementById('otherChartPayment'),
        {
            plugins: [ChartDataLabels], // chartjs-plugin-datalabels 불러오기
            type: 'doughnut', // 차트 타입 지정
            data: {
                labels: [
                    '카드',
                    '현금',
                    '계좌'
                ],
                datasets: [{
                    label: 'My First dataset',
                    backgroundColor: ["#1E64CC", "#677283", "#61B4E5"],
                    borderColor: 'rgba(255, 255, 255, 1)',
                    data: [6, 7, paymentDatas.계좌],
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
                            let percent = 100 * value / ((6 >= 1 ? parseInt(6) : 0) + (7 >= 1 ? parseInt(7) : 0) + (paymentDatas.계좌 >= 1 ? parseInt(paymentDatas.계좌) : 0))
                            percent = Math.round(percent * 100) / 100
                            return (percent >= 1 ? percent : 0) + '%';
                        },
                        align: 'center', // 도넛 차트에서 툴팁이 잘리는 경우 사용
                        color: "white"
                    },
                },
                responsive: false,
            },
        }
    );
}

payment()