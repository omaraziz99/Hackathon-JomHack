// router/index.js
import { createRouter, createWebHistory } from "vue-router";
import { setupLayouts } from "virtual:generated-layouts";
import { routes as autoRoutes } from "vue-router/auto-routes";

// Import components directly from views folder
import DisputeDetails from "@/pages/DisputeDetails.vue";
import AIDisputeDetails from "@/pages/AIDisputeDetails.vue";
import DisputeDashboard from "@/pages/Dashboard.vue";

const manualRoutes = [
  {
    path: "/disputes/dashboard",
    name: "DisputeDashboard",
    component: DisputeDashboard,
  },
  {
    path: "/disputes/active/:id",
    name: "DisputeDetails",
    component: DisputeDetails,
  },
  {
    path: "/disputes/ai/:id",
    name: "AIDisputeDetails",
    component: AIDisputeDetails,
  },
  // Add default redirect
  {
    path: "/",
    redirect: "/disputes/dashboard",
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [...setupLayouts(autoRoutes), ...manualRoutes],
});

export default router;
