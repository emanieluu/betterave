<template>
    <v-container class="fill-height" fluid>
      <div class="content-container">
        <!-- Left Side Columns -->
        <div class="columns-container">
          <InfoColumn title="Next appointment" :list="upcomingAppointment" />
          <InfoColumn title="To do" :list="todoList" />
          <InfoColumn title="Notifications" :list="notifications" />
        </div>
  
        <!-- Right Side Calendar -->
        <div class="calendar-box">
          <UserCalendar />
        </div>
      </div>
      
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  import UserCalendar from '@/components/UserCalendar.vue';
  import ProfilePill from '@/components/ProfilePill.vue';
  import InfoColumn from '@/components/InfoColumn.vue';
  
  export default {
    components: {
      UserCalendar,
      ProfilePill,
      InfoColumn,
    },
    data() {
      return {
        user: {
          name: '',
          surname:'',
          email: ''
        },
        upcomingAppointment: [{ id: 1, text: "Conseil d'études 2A" , color: "#FF5733" }, { id: 2, text: "Réunion projet Stat App" }],
        todoList: [{ id: 1, text: "Préparer cours" }, { id: 2, text: "Correction copies des 2A" }],
        notifications: [{ id: 1, text: "Séminaire statistique demain" }, { id: 2, text: "Conférence directeur INSEE" }]
      };
    },
    async mounted() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/profile', { withCredentials: true });
        this.user = response.data;
        console.log("teacher Response:",response.data);
        this.$emit('updateTitle', "Hello, Asso " + this.user.name + "!");
      } catch (error) {
        console.error("There was an error fetching user data:", error);
      }
    },
    methods: {
  
    }
  }
  </script>
  
  <style scoped>
  
  .calendar-box {
    background-color: #f5f5f5; /* light background color */
    border-radius: 10px; /* rounded corners */
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1); /* subtle shadow for modern effect */
    width: calc(50% - 40px); /* adjust for padding */
    overflow: hidden; /* hide overflow for nested elements to ensure corners are rounded */
    height: 70vh;
  }
  
  .content-container {
    flex: 1;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 20px;
    width: 100%;
  }
  
  .columns-container {
    display: flex;
    justify-content: space-between;
    width: calc(50% - 40px); /* adjust for padding */
    height: 70vh;
  }
  
  </style>
  