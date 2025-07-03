<template>
  <div class="container mt-4">
    <h2 class="mb-3">User Dashboard</h2>
    <button class="btn btn-secondary float-end mb-3" @click="logout">Logout</button>

    <!-- Active Reservation -->
    <div v-if="reservation" class="alert alert-info">
      <p><strong>Current Reservation:</strong></p>
      <p>Lot: {{ reservation.lot }}</p>
      <p>Spot ID: {{ reservation.spot_id }}</p>
      <p>Start Time: {{ reservation.start_time }}</p>
      <button class="btn btn-danger" @click="releaseSpot">Release Spot</button>
    </div>
    <div v-else class="alert alert-secondary">No active reservation.</div>

    <!-- Parking Lots -->
    <h4 class="mt-4">Available Parking Lots</h4>
    <div class="row">
      <div v-for="lot in lots" :key="lot.id" class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ lot.prime_location_name }}</h5>
            <p class="card-text">
              ₹{{ lot.price }} • {{ lot.pincode }}<br />
              Spots Available: {{ lot.available_spots }}
            </p>
            <button class="btn btn-primary" :disabled="reservation" @click="bookSpot(lot.id)">
              Book Spot
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- History -->
    <h4 class="mt-5">Reservation History</h4>
    <table class="table table-bordered" v-if="history.length">
      <thead>
        <tr>
          <th>Lot</th>
          <th>Start</th>
          <th>End</th>
          <th>Cost</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="res in history" :key="res.reservation_id">
          <td>{{ res.lot }}</td>
          <td>{{ res.start_time }}</td>
          <td>{{ res.end_time }}</td>
          <td>₹{{ res.total_cost }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else class="text-muted">No history found.</div>

    <!-- Export History -->
    <div class="mt-3">
      <button class="btn btn-outline-success" @click="exportHistory">Export CSV</button>
      <span class="text-success ms-2" v-if="exportMessage">{{ exportMessage }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const lots = ref([])
const reservation = ref(null)
const history = ref([])
const exportMessage = ref("")

const token = localStorage.getItem("access_token")
const headers = { Authorization: `Bearer ${token}` }

const fetchLots = async () => {
  try {
    const res = await api.get('/user/lots', { headers })
    lots.value = res.data.parking_lots
  } catch (e) {
    console.error('Error fetching lots', e)
  }
}

const fetchReservation = async () => {
  try {
    const res = await api.get('/user/my-reservation', { headers })
    reservation.value = res.data
  } catch (e) {
    reservation.value = null
  }
}

const fetchHistory = async () => {
  try {
    const res = await api.get('/user/history', { headers })
    history.value = res.data.history
  } catch (e) {
    console.error('Error fetching history', e)
  }
}

const bookSpot = async (lotId) => {
  try {
    const res = await api.post('/parking/reserve', { lot_id: lotId }, { headers })
    reservation.value = res.data
    await fetchLots()
  } catch (e) {
    alert('Booking failed.')
  }
}

const releaseSpot = async () => {
  try {
    await api.post(`/parking/leave`, {}, { headers })
    reservation.value = null
    await fetchLots()
    await fetchHistory()
  } catch (e) {
    alert('Failed to release spot.')
  }
}

const exportHistory = async () => {
  try {
    const res = await api.post('/user/export-history', {}, { headers })
    exportMessage.value = "Export started! Check your email."
  } catch (e) {
    exportMessage.value = "Failed to start export."
  }
}

const logout = () => {
  localStorage.removeItem("access_token")
  router.push("/login")
}

onMounted(() => {
  fetchLots()
  fetchReservation()
  fetchHistory()
})
</script>

