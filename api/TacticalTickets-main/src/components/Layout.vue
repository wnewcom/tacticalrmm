<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import {
  Bars3Icon,
  HomeIcon,
  TicketIcon,
  PlusIcon,
  UserIcon,
  ArrowRightOnRectangleIcon,
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const router = useRouter()
const sidebarOpen = ref(false)

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Tickets', href: '/tickets', icon: TicketIcon },
  { name: 'Create Ticket', href: '/tickets/create', icon: PlusIcon },
]
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Mobile sidebar -->
    <Transition name="fade">
      <div v-show="sidebarOpen" class="fixed inset-0 z-40 lg:hidden">
        <div class="fixed inset-0 bg-gray-600 bg-opacity-75" @click="sidebarOpen = false"></div>
        <div class="fixed inset-y-0 left-0 flex flex-col w-64 bg-white shadow-xl">
          <div class="flex items-center justify-between h-16 px-4 bg-primary-600">
            <h1 class="text-xl font-bold text-white">TicketFlow</h1>
            <button @click="sidebarOpen = false" class="text-white hover:text-gray-200">
              <span class="sr-only">Close sidebar</span>
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <nav class="flex-1 px-4 py-4 space-y-2">
            <RouterLink
              v-for="item in navigation"
              :key="item.name"
              :to="item.href"
              class="flex items-center px-3 py-2 text-sm font-medium text-gray-700 rounded-lg hover:bg-gray-100 hover:text-gray-900"
              active-class="bg-primary-100 text-primary-700"
              @click="sidebarOpen = false"
            >
              <component :is="item.icon" class="w-5 h-5 mr-3" />
              {{ item.name }}
            </RouterLink>
          </nav>
        </div>
      </div>
    </Transition>

    <!-- Desktop sidebar -->
    <div class="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
      <div class="flex flex-col flex-1 min-h-0 bg-white border-r border-gray-200">
        <div class="flex items-center h-16 px-4 bg-primary-600">
          <h1 class="text-xl font-bold text-white">TicketFlow</h1>
        </div>
        <nav class="flex-1 px-4 py-4 space-y-2">
          <RouterLink
            v-for="item in navigation"
            :key="item.name"
            :to="item.href"
            class="flex items-center px-3 py-2 text-sm font-medium text-gray-700 rounded-lg hover:bg-gray-100 hover:text-gray-900 transition-colors duration-200"
            active-class="bg-primary-100 text-primary-700"
          >
            <component :is="item.icon" class="w-5 h-5 mr-3" />
            {{ item.name }}
          </RouterLink>
        </nav>
      </div>
    </div>

    <!-- Main content -->
    <div class="lg:pl-64">
      <!-- Top navigation -->
      <div class="sticky top-0 z-10 flex h-16 bg-white border-b border-gray-200 shadow-sm">
        <button
          @click="sidebarOpen = true"
          class="px-4 text-gray-500 lg:hidden hover:text-gray-900"
        >
          <span class="sr-only">Open sidebar</span>
          <Bars3Icon class="w-6 h-6" />
        </button>
        
        <div class="flex items-center justify-between flex-1 px-4">
          <div class="flex items-center">
            <h2 class="text-lg font-semibold text-gray-900">
              <slot name="title">Dashboard</slot>
            </h2>
          </div>
          
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <UserIcon class="w-5 h-5 text-gray-400" />
              <span class="text-sm text-gray-700">{{ authStore.user?.username }}</span>
            </div>
            <button
              @click="handleLogout"
              class="flex items-center space-x-2 text-sm text-gray-700 hover:text-gray-900"
            >
              <ArrowRightOnRectangleIcon class="w-5 h-5" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Page content -->
      <main class="p-6">
        <slot></slot>
      </main>
    </div>
  </div>
</template>