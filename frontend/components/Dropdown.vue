<template>
    <select class="gui-dropdown" :value="modelValue" @change="$emit('update:modelValue', $event.target.value)">
        <option v-for="opt in options" :key="opt.value || opt" :value="opt.value || opt">
            {{ opt.label || opt }}
        </option>
    </select>
</template>

<script setup>
defineProps({
    modelValue: [String, Number],
    options: {
        type: Array,
        required: true,
    },
});
defineEmits(['update:modelValue']);
</script>


<style scoped>
.gui-dropdown {
    appearance: none;
    border: 1px solid #aaa;
    background: linear-gradient(to bottom, #fff, #ddd);
    font-size: 12px;
    padding: 3px 8px;
    font-family: 'Segoe UI', Tahoma, sans-serif;
    box-shadow: inset 0 0 0 1px #fff;
    margin: 2px;
    min-width: 100px;
}

.gui-dropdown:focus {
    outline: none;
    box-shadow: inset 0 0 0 1px #4a90e2;
}
</style>
