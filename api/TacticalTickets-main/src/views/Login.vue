<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  try {
    error.value = ''
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Login failed'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Sign in to TicketFlow
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Streamline your support workflow
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="space-y-4">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              Username
            </label>
            <input
              id="username"
              v-model="username"
              type="text"
              required
              class="form-input mt-1"
              placeholder="Enter your username"
            />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              class="form-input mt-1"
              placeholder="Enter your password"
            />
          </div>
        </div>

        <div v-if="error" class="text-red-600 text-sm text-center">
          {{ error }}
        </div>

        <div>
          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="w-full btn-primary"
          >
            <span v-if="authStore.isLoading">Signing in...</span>
            <span v-else>Sign in</span>
          </button>
        </div>
      </form>
      
      <div class="text-center text-sm text-gray-600">
        <p>Demo credentials:</p>
        <p>Username: <code class="bg-gray-100 px-1 rounded">admin</code></p>
        <p>Password: <code class="bg-gray-100 px-1 rounded">admin</code></p>
      </div>
    </div>
  </div>
</template>