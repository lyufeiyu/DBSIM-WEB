<!-- DataTestChart.vue -->
<template>
    <div>
        <canvas ref="canvas"></canvas>
    </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import Chart from "chart.js/auto";

const props = defineProps({
    chartData: Object,
    options: Object,
});

const canvas = ref(null);

onMounted(() => {
    const ctx = canvas.value.getContext("2d");
    new Chart(ctx, {
        type: "bar",
        data: props.chartData,
        options: props.options,
    });
});
</script>
