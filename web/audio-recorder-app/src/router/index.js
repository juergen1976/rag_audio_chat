// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import Admin from '../views/AdminView.vue';
import Recorder from '../views/RecorderView.vue';

const routes = [
  {
    path: '/',
    name: 'Recorder',
    component: Recorder,
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;