<script setup lang="ts"></script>

<template>
    <div id="footer">
        <div class="container">
            <div class="icons">
                <a
                    target="_blank"
                    class="icon"
                    href="https://fr-fr.facebook.com/BeninExcellence/"
                >
                    <font-awesome-icon icon="fa-brands fa-facebook-f" />
                </a>
                <a
                    target="_blank"
                    class="icon"
                    href="https://twitter.com/excellencebenin"
                >
                    <font-awesome-icon icon="fa-brands fa-twitter" />
                </a>
                <a target="_blank" class="icon" href="#i">
                    <font-awesome-icon icon="fa-brands fa-instagram" />
                </a>
                <a
                    class="icon"
                    target="_blank"
                    rel="noreferrer"
                    href="https://www.linkedin.com/company/benin-excellence/"
                >
                    <font-awesome-icon icon="fa-brands fa-linkedin-in" />
                </a>
            </div>
            <ul class="copyright">
                <li>&copy; Fondation Vallet</li>
                <li>
                    <a
                        target="_blank"
                        rel="noreferrer"
                        href="https://www.fondationvallet.org/eeia/"
                    >
                        École d'Été en Intelligence Artificielle (EEIA)
                    </a>
                </li>
                <li>
                    <a target="_blank" rel="noreferrer" href="#i">
                        Bénin Excellence
                    </a>
                </li>
            </ul>
        </div>
    </div>
</template>

<style scoped>
#footer {
    height: fit-content;
    background-color: #f6f6f6;
}

#footer .container .copyright {
    display: flex;
    flex-wrap: wrap;
}

.icons {
    color: #aaa;
    font-size: 2.7em;
    text-align: center;
    padding-top: 1em;
    padding-bottom: 0.5em;
}

.icon {
    color: #aaa;
    margin-left: 15px;
    margin-right: 15px;
    cursor: pointer;
}

.icon:hover,
.icon:active {
    color: #555;
}

.copyright {
    list-style: none;
    color: #aaa;
    text-align: center;
    margin: 0;
    padding: 0 0 15px 0;
}

.copyright li:first-child {
    border: none;
}

.copyright li {
    border-left: solid 1px rgba(144, 144, 144, 0.25);
    padding: 15px;
    flex: 1;
}

@media only screen and (max-width: 600px) {
    #footer .container {
        height: 300px;
    }

    #footer .container .icons {
        font-size: 2em;
    }

    .copyright {
        flex-direction: column;
    }

    .copyright li {
        border: none;
        padding: 0;
        margin-block: 15px;
    }
}

.copyright li a {
    text-decoration: none;
    color: #aaa;
}

.copyright li a:hover,
.copyright li a:active {
    color: #555;
}
</style>
