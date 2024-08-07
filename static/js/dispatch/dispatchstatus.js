// Vehicle chart
const ctxVehicle = document.getElementById("vehicleChart").getContext("2d");
const vehicleChart = new Chart(ctxVehicle, {
  type: "bar",
  data: {
    labels: ["사용중인 차량", "사용 가능한 차량", "사용 불가능한 차량"],
    datasets: [
      {
        label: "학교 차량",
        data: [15, 7.5, 5],
        backgroundColor: "yellow",
        stack: "Stack 0",
      },
      {
        label: "20인승 하단",
        data: [15, 7.5, 5],
        backgroundColor: "skyblue",
        stack: "Stack 0",
      },
      {
        label: "학교 차량",
        data: [12.5, 10, 7.5],
        backgroundColor: "yellow",
        stack: "Stack 1",
      },
      {
        label: "30인승 하단",
        data: [12.5, 10, 7.5],
        backgroundColor: "blue",
        stack: "Stack 1",
      },
      {
        label: "학교 차량",
        data: [5, 5, 2.5],
        backgroundColor: "yellow",
        stack: "Stack 2",
      },
      {
        label: "40인승 하단",
        data: [5, 5, 2.5],
        backgroundColor: "darkblue",
        stack: "Stack 2",
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        stacked: true,
      },
      x: {
        stacked: true,
      },
    },
  },
});

// Distance chart
const ctxDistance = document.getElementById("distanceChart").getContext("2d");
const distanceChart = new Chart(ctxDistance, {
  type: "bar",
  data: {
    labels: ["제로 공차", "1-5 KM", "6-10 KM", "11-15 KM", "16-20 KM"],
    datasets: [
      {
        label: "제로 공차",
        data: [40, 0, 0, 0, 0], // 제로 공차 데이터는 첫 번째 항목만
        backgroundColor: "red",
      },
      {
        label: "공차",
        data: [0, 20, 10, 20, 10], // 나머지 공차 데이터
        backgroundColor: "navy",
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});

// Tonnage chart
const ctxTonnage = document.getElementById("tonnageChart").getContext("2d");
const tonnageChart = new Chart(ctxTonnage, {
  type: "bar",
  data: {
    labels: [
      "1T",
      "2T",
      "3T",
      "4T",
      "5T",
      "6T",
      "7T",
      "8T",
      "9T",
      "10T",
      "11T",
      "12T",
      "13T",
    ],
    datasets: [
      {
        label: "탑수",
        data: [16, 9, 0, 4, 5, 0, 9, 7, 5, 6, 2, 0, 1],
        backgroundColor: "#4e79a7",
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});
