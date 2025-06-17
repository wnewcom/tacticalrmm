<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import Layout from '../components/Layout.vue'
import TicketCard from '../components/TicketCard.vue'
import { useTicketsStore } from '../stores/tickets'
import { MagnifyingGlassIcon, PlusIcon, FunnelIcon } from '@heroicons/vue/24/outline'

const ticketsStore = useTicketsStore()

const searchQuery = ref('')
const selectedStatus = ref('')
const selectedPriority = ref('')
const selectedCategory = ref('')
const showFilters = ref(false)

const filteredTickets = computed(() => {
  let filtered = ticketsStore.tickets

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(ticket =>
      ticket.title.toLowerCase().includes(query) ||
      ticket.description.toLowerCase().includes(query)
    )
  }

  if (selectedStatus.value) {
    filtered = filtered.filter(ticket => ticket.status === selectedStatus.value)
  }

  if (selectedPriority.value) {
    filtered = filtered.filter(ticket => ticket.priority === selectedPriority.value)
  }

  if (selectedCategory.value) {
    filtered = filtered.filter(ticket => ticket.category.id === parseInt(selectedCategory.value))
  }

  return filtered
})

const statusOptions = [
  { value: '', label: 'All Status' },
  { value: 'open', label: 'Open' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'pending', label: 'Pending' },
  { value: 'resolved', label: 'Resolved' },
  { value: 'closed', label: 'Closed' },
]

const priorityOptions = [
  { value: '', label: 'All Priorities' },
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
  { value: 'urgent', label: 'Urgent' },
]

const handleSearch = () => {
  // Search is handled by computed property
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedStatus.value = ''
  selectedPriority.value = ''
  selectedCategory.value = ''
}

onMounted(async () => {
  await ticketsStore.fetchTickets()
  await ticketsStore.fetchCategories()
})
</script>

<template>
  <Layout>
    <template #title>Tickets</template>
    
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">All Tickets</h1>
          <p class="text-gray-600 mt-1">Manage and track your support tickets</p>
        </div>
        <RouterLink to="/tickets/create" class="btn-primary">
          <PlusIcon class="w-5 h-5 mr-2" />
          Create Ticket
        </RouterLink>
      </div>

      <!-- Search and Filters -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex flex-col sm:flex-row gap-4">
          <div class="flex-1 relative">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search tickets..."
              class="form-input pl-10"
              @input="handleSearch"
            />
          </div>
          <button
            @click="showFilters = !showFilters"
            class="btn-outline"
          >
            <FunnelIcon class="w-5 h-5 mr-2" />
            Filters
          </button>
        </div>

        <!-- Filter Controls -->
        <Transition name="slide-up">
          <div v-show="showFilters" class="mt-4 pt-4 border-t border-gray-200">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select v-model="selectedStatus" class="form-select">
                  <option v-for="option in statusOptions" :key="option.value" :value="option.value">
                    {{ option.label }}
                  </option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                <select v-model="selectedPriority" class="form-select">
                  <option v-for="option in priorityOptions" :key="option.value" :value="option.value">
                    {{ option.label }}
                  </option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
                <select v-model="selectedCategory" class="form-select">
                  <option value="">All Categories</option>
                  <option v-for="category in ticketsStore.categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select>
              </div>
              
              <div class="flex items-end">
                <button @click="clearFilters" class="btn-secondary w-full">
                  Clear Filters
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </div>

      <!-- Tickets List -->
      <div v-if="ticketsStore.isLoading" class="text-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
        <p class="text-gray-600 mt-2">Loading tickets...</p>
      </div>

      <div v-else-if="filteredTickets.length === 0" class="text-center py-12">
        <TicketIcon class="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">No tickets found</h3>
        <p class="text-gray-600 mb-4">
          {{ searchQuery || selectedStatus || selectedPriority || selectedCategory 
             ? 'Try adjusting your search or filters' 
             : 'Get started by creating your first ticket' }}
        </p>
        <RouterLink to="/tickets/create" class="btn-primary">
          Create Ticket
        </RouterLink>
      </div>

      <div v-else class="space-y-4">
        <TicketCard
          v-for="ticket in filteredTickets"
          :key="ticket.id"
          :ticket="ticket"
        />
      </div>
    </div>
  </Layout>
</template>