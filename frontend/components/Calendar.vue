<template>
    <input type="date" class="gui-calendar" :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)" />
</template>

<script setup>
defineProps({
    modelValue: String,
});
defineEmits(['update:modelValue']);
</script>


<style scoped>
.gui-calendar {
    font-size: 12px;
    border: 1px solid #aaa;
    background: linear-gradient(to bottom, #fff, #ddd);
    padding: 3px 8px;
    box-shadow: inset 0 0 0 1px #fff;
    font-family: 'Segoe UI', Tahoma, sans-serif;
    margin: 2px;
    min-width: 100px;
}

.gui-calendar:focus {
    outline: none;
    box-shadow: inset 0 0 0 1px #4a90e2;
}
</style>
