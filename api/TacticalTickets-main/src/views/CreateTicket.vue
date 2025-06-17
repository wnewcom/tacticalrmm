<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import Layout from '../components/Layout.vue'
import { useTicketsStore } from '../stores/tickets'
import type { TicketCreate } from '../types'

const router = useRouter()
const ticketsStore = useTicketsStore()

const form = ref<TicketCreate>({
  title: '',
  description: '',
  priority: 'medium',
  category_id: 0,
  assigned_to_id: null,
  due_date: null,
})

const users = ref([])
const isLoading = ref(false)
const errors = ref<Record<string, string>>({})

const handleSubmit = async () => {
  try {
    isLoading.value = true
    errors.value = {}
    
    await ticketsStore.createTicket(form.value)
    router.push('/tickets')
  } catch (error: any) {
    if (error.response?.data) {
      errors.value = error.response.data
    }
  } finally {
    isLoading.value = false
  }
}

const fetchUsers = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/users/')
    if (response.ok) {
      const data = await response.json()
      users.value = data.results
    }
  } catch (error) {
    console.error('Error fetching users:', error)
  }
}

onMounted(async () => {
  await ticketsStore.fetchCategories()
  await fetchUsers()
})
</script>

<template>
  <Layout>
    <template #title>Create New Ticket</template>
    
    <div class="max-w-2xl mx-auto">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h1 class="text-2xl font-bold text-gray-900 mb-6">Create New Ticket</h1>
        
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700 mb-1">
              Title *
            </label>
            <input
              id="title"
              v-model="form.title"
              type="text"
              required
              class="form-input"
              :class="{ 'border-red-500': errors.title }"
              placeholder="Brief description of the issue"
            />
            <p v-if="errors.title" class="mt-1 text-sm text-red-600">{{ errors.title }}</p>
          </div>

          <div>
            <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
              Description *
            </label>
            <textarea
              id="description"
              v-model="form.description"
              required
              rows="4"
              class="form-textarea"
              :class="{ 'border-red-500': errors.description }"
              placeholder="Detailed description of the issue"
            />
            <p v-if="errors.description" class="mt-1 text-sm text-red-600">{{ errors.description }}</p>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <label for="priority" class="block text-sm font-medium text-gray-700 mb-1">
                Priority
              </label>
              <select
                id="priority"
                v-model="form.priority"
                class="form-select"
                :class="{ 'border-red-500': errors.priority }"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
              <p v-if="errors.priority" class="mt-1 text-sm text-red-600">{{ errors.priority }}</p>
            </div>

            <div>
              <label for="category" class="block text-sm font-medium text-gray-700 mb-1">
                Category *
              </label>
              <select
                id="category"
                v-model="form.category_id"
                required
                class="form-select"
                :class="{ 'border-red-500': errors.category_id }"
              >
                <option value="">Select a category</option>
                <option v-for="category in ticketsStore.categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
              <p v-if="errors.category_id" class="mt-1 text-sm text-red-600">{{ errors.category_id }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <label for="assigned_to" class="block text-sm font-medium text-gray-700 mb-1">
                Assign to
              </label>
              <select
                id="assigned_to"
                v-model="form.assigned_to_id"
                class="form-select"
                :class="{ 'border-red-500': errors.assigned_to_id }"
              >
                <option :value="null">Unassigned</option>
                <option v-for="user in users" :key="user.id" :value="user.id">
                  {{ user.username }} ({{ user.email }})
                </option>
              </select>
              <p v-if="errors.assigned_to_id" class="mt-1 text-sm text-red-600">{{ errors.assigned_to_id }}</p>
            </div>

            <div>
              <label for="due_date" class="block text-sm font-medium text-gray-700 mb-1">
                Due Date
              </label>
              <input
                id="due_date"
                v-model="form.due_date"
                type="datetime-local"
                class="form-input"
                :class="{ 'border-red-500': errors.due_date }"
              />
              <p v-if="errors.due_date" class="mt-1 text-sm text-red-600">{{ errors.due_date }}</p>
            </div>
          </div>

          <div class="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200">
            <RouterLink to="/tickets" class="btn-secondary">
              Cancel
            </RouterLink>
            <button
              type="submit"
              :disabled="isLoading"
              class="btn-primary"
            >
              <span v-if="isLoading">Creating...</span>
              <span v-else>Create Ticket</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Layout>
</template>