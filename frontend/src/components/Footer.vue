<script setup lang="ts"></script>

<template>
    <div id="footer">
        <div class="container">
            <div class="icons">
                <a class="icon" href="https://fr-fr.facebook.com/BeninExcellence/">
                    <font-awesome-icon icon="fa-brands fa-facebook-f" />
                </a>
                <a class="icon" href="https://twitter.com/excellencebenin">
                    <font-awesome-icon icon="fa-brands fa-twitter" />
                </a>
                <a class="icon" href="#i">
                    <font-awesome-icon icon="fa-brands fa-instagram" />
                </a>
                <a class="icon" target="_blank" rel="noreferrer"
                    href="https://www.linkedin.com/company/benin-excellence/">
                    <font-awesome-icon icon="fa-brands fa-linkedin-in" />
                </a>
            </div>
            <ul class="copyright">
                <li>&copy; Fondation Vallet</li>
                <li>
                    <a target="_blank" rel="noreferrer" href="https://www.fondationvallet.org/eeia/">
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
    background-color: #f6f6f6;
}

.icons {
    color: #aaa;
    font-size: 2.7em;
    text-align: center;
    padding-top: 1em;
    padding-bottom: .5em;
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
    list-style: disc;
    color: #aaa;
    text-align: center;
    margin: 0;
    padding: 0 0 15px 0;
}

.copyright li:first-child {
    border: none;
}

.copyright li {
    display: inline-block;
    border-left: solid 1px rgba(144, 144, 144, 0.25);
    padding: 15px;
}

@media only screen and (max-width: 600px) {
    .copyright li {
        display: block;
        border: none;
        padding: 0;
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
