<template>
    <div class="loader">
        <font-awesome-icon
            icon="fa-solid fa-spinner"
            size="2xl"
            color="var(--main-purple-lightened)"
            class="spinner"
        />
        <p>Loading...</p>
    </div>
</template>

<style scoped>
.loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 50vh;
}

.spinner {
    animation: spin 1.65s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}
</style>
