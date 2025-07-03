<script setup>
import { ref, onMounted } from "vue";
import api from "@/api/axios";

const lots = ref([]);
const errorMessage = ref("");

const fetchLots = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const res = await api.get("/admin/parking-lots", {
      headers: { Authorization: `Bearer ${token}` },
    });
    lots.value = res.data.parking_lots;
    errorMessage.value = "";  // clear any previous error
  } catch (e) {
    if (e.response?.status === 403) {
      errorMessage.value = "You are not authorized to view this page.";
    } else {
      errorMessage.value = "An error occurred while fetching data.";
      console.error("Fetch error:", e);
    }
  }
};

onMounted(() => {
  fetchLots();
});
</script>

<template>
  <div>
    <h2>Admin Dashboard</h2>

    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>

    <section v-else-if="lots.length">
      <h3>Parking Lots</h3>
      <ul>
        <li v-for="lot in lots" :key="lot.id">
          {{ lot.prime_location_name }} – ₹{{ lot.price }} – {{ lot.pincode }}
        </li>
      </ul>
    </section>

    <button @click="fetchLots">Refresh Lots</button>
  </div>
</template>

<style scoped>
.error {
  color: red;
  font-weight: bold;
  margin: 10px 0;
}
</style>

