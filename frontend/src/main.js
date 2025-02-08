/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App
 */

// Plugins
import { registerPlugins } from "@/plugins";
import router from "./router";
import vuetify from "./plugins/vuetify";

// Components
import App from "./App.vue";

// Composables
import { createApp } from "vue";

const app = createApp(App);

import { createPinia } from "pinia";
const pinia = createPinia();
app.use(pinia);

// Register plugins both through the helper and manually
registerPlugins(app);
app.use(router);
app.use(vuetify);

app.mount("#app");
