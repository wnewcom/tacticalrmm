<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Layout from '../components/Layout.vue'
import { useTicketsStore } from '../stores/tickets'
import { useAuthStore } from '../stores/auth'
import {
  TicketIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  UserIcon,
  ChartBarIcon,
} from '@heroicons/vue/24/outline'

const ticketsStore = useTicketsStore()
const authStore = useAuthStore()

const recentTickets = ref([])

onMounted(async () => {
  await ticketsStore.fetchDashboardStats()
  const response = await ticketsStore.fetchTickets({ page_size: 5 })
  recentTickets.value = response.results
})

const stats = [
  {
    name: 'Total Tickets',
    value: () => ticketsStore.dashboardStats?.total_tickets || 0,
    icon: TicketIcon,
    color: 'text-blue-600',
    bgColor: 'bg-blue-100',
  },
  {
    name: 'Open Tickets',
    value: () => ticketsStore.dashboardStats?.open_tickets || 0,
    icon: ClockIcon,
    color: 'text-yellow-600',
    bgColor: 'bg-yellow-100',
  },
  {
    name: 'In Progress',
    value: () => ticketsStore.dashboardStats?.in_progress_tickets || 0,
    icon: ChartBarIcon,
    color: 'text-purple-600',
    bgColor: 'bg-purple-100',
  },
  {
    name: 'Resolved',
    value: () => ticketsStore.dashboardStats?.resolved_tickets || 0,
    icon: CheckCircleIcon,
    color: 'text-green-600',
    bgColor: 'bg-green-100',
  },
  {
    name: 'My Tickets',
    value: () => ticketsStore.dashboardStats?.my_tickets || 0,
    icon: UserIcon,
    color: 'text-indigo-600',
    bgColor: 'bg-indigo-100',
  },
  {
    name: 'High Priority',
    value: () => ticketsStore.dashboardStats?.urgent_priority || 0,
    icon: ExclamationTriangleIcon,
    color: 'text-red-600',
    bgColor: 'bg-red-100',
  },
]

const statusColors = {
  open: 'bg-blue-100 text-blue-800',
  in_progress: 'bg-purple-100 text-purple-800',
  pending: 'bg-yellow-100 text-yellow-800',
  resolved: 'bg-green-100 text-green-800',
  closed: 'bg-gray-100 text-gray-800',
}
</script>

<template>
  <Layout>
    <template #title>Dashboard</template>
    
    <div class="space-y-6">
      <!-- Welcome Section -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h1 class="text-2xl font-bold text-gray-900 mb-2">
          Welcome back, {{ authStore.user?.first_name || authStore.user?.username }}!
        </h1>
        <p class="text-gray-600">
          Here's an overview of your ticketing system activity.
        </p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="stat in stats"
          :key="stat.name"
          class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200"
        >
          <div class="flex items-center">
            <div :class="[stat.bgColor, 'p-3 rounded-lg']">
              <component :is="stat.icon" :class="[stat.color, 'w-6 h-6']" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">{{ stat.name }}</p>
              <p class="text-2xl font-bold text-gray-900">{{ stat.value() }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Tickets -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Recent Tickets</h2>
        </div>
        <div class="divide-y divide-gray-200">
          <div
            v-for="ticket in recentTickets"
            :key="ticket.id"
            class="p-6 hover:bg-gray-50 transition-colors duration-200"
          >
            <div class="flex items-center justify-between">
              <div class="flex-1 min-w-0">
                <RouterLink
                  :to="`/tickets/${ticket.id}`"
                  class="text-sm font-medium text-gray-900 hover:text-primary-600 transition-colors duration-200"
                >
                  #{{ ticket.id }} - {{ ticket.title }}
                </RouterLink>
                <p class="text-sm text-gray-500 mt-1">
                  {{ ticket.category.name }} • Created by {{ ticket.created_by.username }}
                </p>
              </div>
              <div class="flex items-center space-x-2 ml-4">
                <span
                  :class="statusColors[ticket.status]"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                >
                  {{ ticket.status.replace('_', ' ') }}
                </span>
              </div>
            </div>
          </div>
          
          <div v-if="recentTickets.length === 0" class="p-6 text-center text-gray-500">
            No tickets found. <RouterLink to="/tickets/create" class="text-primary-600 hover:text-primary-700">Create your first ticket</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>