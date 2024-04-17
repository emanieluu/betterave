<template>
  <div class="notification-container">
    <div v-if="notification.length === 0" class="notification-item">
      No notification yet.
    </div>
    <div
      v-for="ntf in notification"
      :key="ntf.notification_id"
      class="notification-box"
    >
      <div class="notification-header">
        <span class="notification-title">{{ ntf.title }}</span>
      </div>
      <div class="notification-content">{{ ntf.type }}</div>
    </div>
  </div>
</template>

<script>
import { apiClient } from "@/apiConfig";

export default {
  props: {
    class_id: {
      type: Number,
      required: false,
    },
  },
  data() {
    return {
      notification: [],
    };
  },
  async mounted() {
    try {
      // If class_id is not provided, fetch all notification
      const response = await apiClient.get("/users/me/notifications");

      // Reverse the list
      response.data.reverse();
      this.notification = response.data;
    } catch (error) {
      console.error("Error fetching notification:", error);
    }
  },
};
</script>

<style scoped>
.notification-container {
  position: relative;
  max-height: 65vh;
  overflow: auto;
}

.notification-box {
  display: flex;
  flex-direction: column;
  padding: 10px;
  border-radius: 10px;
  background-color: #dcdcdc; /* Couleur grise pour la boîte de notification */
  color: #333; /* Couleur du texte */
  margin-top: 10px;
  cursor: pointer;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  font-size: 0.7rem;
}

.notification-title {
  font-weight: bold;
}

.notification-content {
  font-size: 0.8rem;
}
</style>
