<template>
    <div class="fetch-error">
        <font-awesome-icon
            icon="fa-solid fa-triangle-exclamation"
            size="2xl"
            color="var(--main-purple-lightened)"
            class="warning-icon"
        />
        <br />
        <p>Sorry, something went wrong...</p>
    </div>
</template>

<style scoped>
.fetch-error {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 50vh;
}

.warning-icon {
    font-size: 4em;
}

p {
    font-style: italic;
}
</style>
