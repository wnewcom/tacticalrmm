import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'
import type { User } from '../types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!user.value)

  const login = async (username: string, password: string) => {
    isLoading.value = true
    try {
      const response = await api.post('/auth/login/', { username, password })
      user.value = response.data.user
      return response.data
    } catch (error) {
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      await api.post('/auth/logout/')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      user.value = null
    }
  }

  const checkAuth = async () => {
    try {
      const response = await api.get('/auth/user/')
      user.value = response.data
    } catch (error) {
      user.value = null
    }
  }

  return {
    user,
    isLoading,
    isAuthenticated,
    login,
    logout,
    checkAuth
  }
})