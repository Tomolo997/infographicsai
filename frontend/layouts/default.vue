<template>
    <div class="app-layout ">
         <slot/>
    </div>
</template>

<script>
</script>

<style scoped>
.app-layout {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-repeat: repeat;
    background-size: 100px 100px; /* Adjust this value to match the size of your SVG */
}

.main-content {
    display: flex;
    flex: 1;
    max-height: calc(100vh - 56px);
}


.page-content {
    flex: 1;
    overflow-y: auto;
    max-height: 100vh;
}

</style>
