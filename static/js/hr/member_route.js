new Chart(document.getElementById("mixed-chart"), {
    type: 'bar',
    data: {
        labels: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
        datasets: [{
            label: "팀 별 숙지 평균",
            type: "line",
            borderColor: "orange",
            data: [10, 20, 43, 75, 75, 75, 75, 75, 75, 80, 87, 100],
            fill: false
        }, {
            label: "총 숙지 평균",
            type: "line",
            borderColor: "blue",
            data: [1, 20, 37, 43, 52, 61, 70, 75, 80, 80, 80, 100],
            fill: false
        }, {
            label: "개인 숙지 현황",
            type: "bar",
            backgroundColor: "green",
            data: [10, 20, 43, 75, 75, 75, 75, 75, 75, 80, 87, 100],
        }
        ]
    },
    options: {
        responsive: false,
        aspectRatio: 5,
        title: {
            display: false,
        },
        legend: { display: false },
        maintainAspectRatio: false,
    }
});