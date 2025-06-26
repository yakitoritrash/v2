<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" />
      <input v-model="email" type="email" placeholder="Email" />
      <input v-model="phone" placeholder="Phone Number" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from '@/api/axios'

const username = ref("");
const email = ref("");
const phone = ref("");
const password = ref("");
const router = useRouter();

const register = async () => {
  try {
    await api.post("/auth/register", {
      username: username.value,
      email: email.value,
      password: password.value,
      phone_number: phone.value,
    });

    // Optional: auto-login or redirect to login
    router.push("/login");
  } catch (err) {
    console.error("Registration failed:", err);
    alert("Error registering: " + err?.response?.data?.message || "Unknown error");
  }
};
</script>

