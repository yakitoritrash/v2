<template>
  <div class="container py-5">
    <h2 class="mb-4">Admin Dashboard</h2>

    <div v-if="userRole !== 'admin'" class="alert alert-danger">
      You are not authorized to view this page.
    </div>

    <div v-else>
      <!-- Error Alert -->
      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </div>

      <!-- Add New Lot -->
      <div class="card mb-4 shadow-sm">
        <div class="card-body">
          <h5 class="card-title">Add New Parking Lot</h5>
          <form @submit.prevent="createLot">
            <div class="row g-2">
              <div class="col-md-3">
                <input v-model="newLot.name" class="form-control" placeholder="Location Name" required />
              </div>
              <div class="col-md-2">
                <input v-model.number="newLot.price" class="form-control" placeholder="Price" type="number" required />
              </div>
              <div class="col-md-3">
                <input v-model="newLot.address" class="form-control" placeholder="Address" required />
              </div>
              <div class="col-md-2">
                <input v-model="newLot.pincode" class="form-control" placeholder="Pincode" required />
              </div>
              <div class="col-md-2">
                <input v-model.number="newLot.number_of_spots" class="form-control" placeholder="Spots" type="number" required />
              </div>
              <div class="col-md-2">
                <button class="btn btn-primary w-100" type="submit">Add</button>
              </div>
            </div>
          </form>
        </div>
      </div>

      <!-- Parking Lot Table -->
      <div v-if="lots.length" class="card shadow-sm mb-4">
        <div class="card-body">
          <h5 class="card-title">Parking Lots</h5>
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>Name</th>
                <th>Price (₹/hr)</th>
                <th>Pincode</th>
                <th>Available Spots</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="lot in lots" :key="lot.id">
                <td>{{ lot.prime_location_name }}</td>
                <td>₹{{ lot.price }}</td>
                <td>{{ lot.pincode }}</td>
                <td>{{ lot.number_of_spots ?? 'N/A' }}</td>
                <td>
                  <button class="btn btn-sm btn-outline-info me-2" @click="viewSpots(lot.id)">View</button>
                  <button class="btn btn-sm btn-outline-warning me-2" @click="showEditModal(lot)">Edit</button>
                  <button class="btn btn-sm btn-outline-danger" @click="deleteLot(lot.id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
          <button class="btn btn-outline-secondary mt-2" @click="fetchLots">Refresh</button>
        </div>
      </div>

      <!-- Users Table -->
      <div class="card shadow-sm">
        <div class="card-body">
          <h5 class="card-title">Registered Users</h5>
          <table class="table table-striped" v-if="users.length">
            <thead>
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Role</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.phone_number }}</td>
                <td>{{ user.role }}</td>
              </tr>
            </tbody>
          </table>
          <div v-else class="text-muted">No users found.</div>
        </div>
      </div>
    </div>

    <!-- Spot View Modal -->
    <div v-if="spotModalVisible" class="modal-backdrop">
      <div class="modal-content">
        <h5>Parking Spots in {{ selectedLotName }}</h5>
        <table class="table table-sm">
          <thead>
            <tr>
              <th>Spot ID</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="spot in selectedSpots" :key="spot.id">
              <td>{{ spot.id }}</td>
              <td>
                <span :class="{'text-success': spot.status === 'A', 'text-danger': spot.status === 'O'}">
                  {{ spot.status === 'A' ? 'Available' : 'Occupied' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
        <button class="btn btn-secondary mt-2" @click="spotModalVisible = false">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/api/axios";

const lots = ref([]);
const users = ref([]);
const errorMessage = ref("");
const newLot = ref({ name: "", address: "", price: 0, pincode: "", number_of_spots: 0 });
const editLot = ref(null);
const selectedSpots = ref([]);
const spotModalVisible = ref(false);
const selectedLotName = ref("");
const userRole = ref("");

const token = localStorage.getItem("access_token");
const headers = { Authorization: `Bearer ${token}` };

const fetchUserRole = async () => {
  try {
    const res = await api.get("/auth/me", { headers });
    userRole.value = res.data.role;
  } catch (e) {
    userRole.value = "";
  }
};

const fetchLots = async () => {
  try {
    const res = await api.get("/admin/parking-lots", { headers });
    lots.value = res.data.parking_lots;
    errorMessage.value = "";
  } catch (e) {
    errorMessage.value =
      e.response?.status === 403
        ? "You are not authorized to view this page."
        : "Error fetching parking lots.";
    console.error(e);
  }
};

const createLot = async () => {
  try {
    await api.post(
      "/admin/parking-lot",
      newLot.value,
      { headers }
    );
    newLot.value = { name: "", price: 0, pincode: "", address: "", number_of_spots: 0 };
    await fetchLots();
  } catch (e) {
    alert("Failed to add parking lot.");
  }
};

const deleteLot = async (id) => {
  if (!confirm("Are you sure you want to delete this lot?")) return;
  try {
    await api.delete(`/admin/parking-lot/${id}`, { headers });
    await fetchLots();
  } catch (e) {
    alert("Failed to delete lot.");
  }
};

const showEditModal = (lot) => {
  editLot.value = { ...lot };
};

const updateLot = async () => {
  try {
    await api.put(`/admin/parking-lot/${editLot.value.id}`, editLot.value, {
      headers,
    });
    editLot.value = null;
    await fetchLots();
  } catch (e) {
    alert("Failed to update lot.");
  }
};

const fetchUsers = async () => {
  try {
    const res = await api.get("/admin/users", { headers });
    users.value = res.data.users;
  } catch (e) {
    console.error("Error fetching users", e);
    alert("Failed to fetch users.");
  }
};

const viewSpots = async (lotId) => {
  try {
    const lot = lots.value.find(l => l.id === lotId);
    selectedLotName.value = lot.prime_location_name;
    const res = await api.get(`/admin/parking-lot/${lotId}/spots`, { headers });
    selectedSpots.value = res.data.parking_spots;
    spotModalVisible.value = true;
  } catch (e) {
    alert("Failed to load parking spots.");
    console.error(e);
  }
};

onMounted(async () => {
  await fetchUserRole();
  if (userRole.value === "admin") {
    await fetchLots();
    await fetchUsers();
  }
});
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}
.modal-content {
  color: #212529;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}
</style>

