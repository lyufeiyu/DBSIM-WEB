<template>
    <div class="chart-card">
        <canvas ref="canvas" :id="chartId"></canvas>
    </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
    props: {
        chartId: {
            type: String,
            required: true,
        },
        chartData: {
            type: Array,
            required: true,
        },
        // This should also be an Array to correspond to the data points
        chartLabels: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            chart: null,
        };
    },
    mounted() {
        this.$nextTick(() => {
            this.initChart();
        });
    },
    activated() {
        // 当组件被重新激活时，重新初始化图表
        if (!this.chart) {
            this.initChart();
        }
    },
    // deactivated() {
    //     // 当组件失活时，销毁图表以防止内存泄漏
    //     if (this.chart) {
    //         this.chart.destroy();
    //         this.chart = null;
    //     }
    // },
    methods: {
        initChart() {
            this.$nextTick(() => {
                // 确保 DOM 更新完成
                // console.log("Canvas ID:", this.chartId);
                const canvas = this.$refs.canvas; // 使用 refs 而不是 getElementById
                // console.log("Canvas element:", canvas);
                if (canvas) {
                    const ctx = canvas.getContext("2d");
                    this.chart = new Chart(ctx, {
                        type: "line", // Change from 'bar' to 'line' to match the requirement
                        data: {
                            labels: [1, 2, 3, 4, 5], // Assign the array of labels to the chart
                            datasets: [
                                {
                                    label: this.chartId, // You might want to have a more descriptive label here
                                    data: this.chartData, // Assign the array of data points to the chart
                                    fill: false,
                                    borderColor: "rgb(75, 192, 192)",
                                    tension: 0.1,
                                },
                            ],
                        },
                        options: {
                            scales: {
                                y: {
                                    beginAtZero: true,
                                },
                            },
                        },
                    });
                } else {
                    console.error("Canvas element not found:", this.chartId);
                }
            });
        },
    },
    watch: {
        // Watch for changes to the data or labels and update the chart
        chartData(newVal) {
            if (this.chart) {
                this.chart.data.datasets[0].data = newVal;
                this.chart.update();
            }
        },
        chartLabels(newVal) {
            if (this.chart) {
                this.chart.data.labels = newVal;
                this.chart.update();
            }
        },
    },
    // beforeUnmount() {
    //     if (this.chart) {
    //         this.chart.destroy();
    //     }
    // },
};
</script>

<style scoped>
.chart-card {
    padding: 1rem;
    background-color: #ffffff; /* Dark background for the chart */
    border-radius: 0.25rem;
}
</style>
