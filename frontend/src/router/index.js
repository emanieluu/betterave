import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import HomePage from '../views/HomePage.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import TeacherDashboard from '../views/TeacherDashboard.vue'
import AssoDashboard from '../views/AssoDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import Photochart from '../views/Photochart.vue'
import ClassPage from '../views/ClassPage.vue'
import ClassTeached from '../views/ClassTeached.vue'
import MainLayout from '../views/MainLayout.vue'
import axios from 'axios';

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '', 
        name: 'homepage',
        component: HomePage
      },
      {
        path: 'student-dashboard', 
        name: 'student-dashboard',
        component: StudentDashboard
      },
      {
        path: 'teacher-dashboard', 
        name: 'teacherDashboard',
        component: TeacherDashboard
      },
      {
        path: 'asso-dashboard', 
        name: 'assoDashboard',
        component: AssoDashboard
      },
      {
        path: 'admin-dashboard', 
        name: 'adminDashboard',
        component: AdminDashboard
      },
      
      {
        path: 'class-teached', 
        name: 'classTeached',
        component: ClassTeached
      },
      {
        path: 'class/:classId', // dynamic segment for class id
        name: 'class-details',
        component: ClassPage
      },
      {
        path: '/photochart',
        name: 'Photochart',
        component: Photochart,
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  // If the user is navigating to the login page, just continue.
  if (to.name === 'Login') {
    next();
    return;
  }

  // Otherwise, check if the user is authenticated.
  try {
    const response = await axios.get('http://127.0.0.1:5000/check-auth', {
      withCredentials: true,
    });
    if (response.data.status === 'authenticated') {
      next();
    } else {
      next({ name: 'Login' });  // Redirect to login
    }
  } catch (error) {
    console.log(error);
    next({ name: 'Login' });  // Redirect to login in case of error
  }
});

export default router;
