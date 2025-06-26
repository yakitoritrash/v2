<template>
  <div>
    <h2>Admin Dashboard</h2>

    <section v-if="lots.length">
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

<script setup>
import { ref, onMounted } from "vue";
import api from "@/api/axios";

const lots = ref([]);

const fetchLots = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const res = await api.get("/admin/parking-lots", {
      headers: { Authorization: `Bearer ${token}` },
    });
    lots.value = res.data.parking_lots;
  } catch (e) {
    console.error("Failed to fetch parking lots:", e);
  }
};

onMounted(() => {
  fetchLots();
});
</script>

