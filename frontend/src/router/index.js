/**
 * router/index.js
 *
 * Router configuration with automatic and manual routes
 */

// Composables
import { createRouter, createWebHistory } from "vue-router";
import { setupLayouts } from "virtual:generated-layouts";
import { routes as autoRoutes } from "vue-router/auto-routes";
import DisputeDetails from "@/pages/DisputeDetails.vue";
import AIDisputeDetails from "@/pages/AIAutoClosed.vue";
import DisputeDashboard from "@/pages/Dashboard.vue";

// Manual routes configuration
const routes = [
  {
    path: "/disputes/:id",
    name: "DisputeDetails",
    component: () => import("@/pages/DisputeDetails.vue"),
    props: true,
  },
];
const manualRoutes = [
  {
    path: "/disputes/:id",
    name: "DisputeDetails",
    component: DisputeDetails,
  },
  {
    path: "/disputes/:id",
    name: "AIDisputeDetails",
    component: AIDisputeDetails,
  },

  {
    path: "/disputes/:id",
    name: "DisputeDashboard",
    component: DisputeDashboard,
  },
];

// Combine automatic and manual routes
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [...setupLayouts(autoRoutes), ...manualRoutes],
});

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.("Failed to fetch dynamically imported module")) {
    if (!localStorage.getItem("vuetify:dynamic-reload")) {
      console.log("Reloading page to fix dynamic import error");
      localStorage.setItem("vuetify:dynamic-reload", "true");
      location.assign(to.fullPath);
    } else {
      console.error("Dynamic import error, reloading page did not fix it", err);
    }
  } else {
    console.error(err);
  }
});

router.isReady().then(() => {
  localStorage.removeItem("vuetify:dynamic-reload");
});

export default router;
