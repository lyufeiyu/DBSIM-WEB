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
    },
    data() {
        return {
            chart: null,
        };
    },
    mounted() {
        this.initChart();
    },
    methods: {
        initChart() {
            const ctx = this.$refs.canvas.getContext('2d');
            const gradient = ctx.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, 'rgba(75, 192, 192, 0.2)');
            gradient.addColorStop(1, 'rgba(75, 192, 192, 0)');
            
            this.chart = new Chart(ctx, {
                type: 'line',
                data: {
                    // 因为不显示横轴标签，可以传入一个与数据等长的空数组
                    labels: this.chartData.map(() => ''),
                    datasets: [{
                        label: this.chartId,
                        data: this.chartData,
                        fill: true,
                        backgroundColor: gradient,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.4,
                        pointRadius: 0, // 不显示点
                    }]
                },
                options: {
                    scales: {
                        x: {
                            display: false, // 不显示横轴
                        },
                        y: {
                            beginAtZero: true,
                        }
                    },
                    plugins: {
                        legend: {
                            display: false // 如果您不想显示图例
                        }
                    },
                    maintainAspectRatio: false, // 可以添加这个选项来防止图表按比例缩放
                }
            });
        },
    },
};
</script>

<style scoped>
.chart-card {
    position: relative; /* 为了 maintainAspectRatio */
    height: 20vh; /* 或者你希望的任何高度 */
    padding: 1rem;
    background-color: #000; /* 暗色背景 */
    border-radius: 0.25rem;
}
.chart-card {
    padding: 1rem;
    background-color: #ffffff; /* Dark background for the chart */
    border-radius: 0.25rem;
}
</style>
