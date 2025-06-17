<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { format, formatDistanceToNow } from 'date-fns'
import type { Ticket } from '../types'
import {
  ChatBubbleLeftIcon,
  ClockIcon,
  ExclamationTriangleIcon,
} from '@heroicons/vue/24/outline'

interface Props {
  ticket: Ticket
}

const props = defineProps<Props>()

const priorityColors = {
  low: 'bg-green-100 text-green-800',
  medium: 'bg-yellow-100 text-yellow-800',
  high: 'bg-orange-100 text-orange-800',
  urgent: 'bg-red-100 text-red-800',
}

const statusColors = {
  open: 'bg-blue-100 text-blue-800',
  in_progress: 'bg-purple-100 text-purple-800',
  pending: 'bg-yellow-100 text-yellow-800',
  resolved: 'bg-green-100 text-green-800',
  closed: 'bg-gray-100 text-gray-800',
}

const formattedDate = computed(() => {
  return formatDistanceToNow(new Date(props.ticket.created_at), { addSuffix: true })
})

const formattedDueDate = computed(() => {
  if (!props.ticket.due_date) return null
  return format(new Date(props.ticket.due_date), 'MMM dd, yyyy')
})
</script>

<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
    <div class="p-6">
      <div class="flex items-start justify-between mb-4">
        <div class="flex-1 min-w-0">
          <RouterLink
            :to="`/tickets/${ticket.id}`"
            class="text-lg font-semibold text-gray-900 hover:text-primary-600 transition-colors duration-200"
          >
            #{{ ticket.id }} - {{ ticket.title }}
          </RouterLink>
          <p class="text-sm text-gray-500 mt-1 line-clamp-2">
            {{ ticket.description }}
          </p>
        </div>
        <div class="flex items-center space-x-2 ml-4">
          <span
            :class="priorityColors[ticket.priority]"
            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
          >
            {{ ticket.priority }}
          </span>
          <span
            :class="statusColors[ticket.status]"
            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
          >
            {{ ticket.status.replace('_', ' ') }}
          </span>
        </div>
      </div>

      <div class="flex items-center justify-between text-sm text-gray-500">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-1">
            <span class="font-medium text-gray-900">{{ ticket.category.name }}</span>
          </div>
          <div class="flex items-center space-x-1">
            <span>Created by {{ ticket.created_by.username }}</span>
          </div>
          <div v-if="ticket.assigned_to" class="flex items-center space-x-1">
            <span>Assigned to {{ ticket.assigned_to.username }}</span>
          </div>
        </div>
        
        <div class="flex items-center space-x-3">
          <div v-if="ticket.comments_count" class="flex items-center space-x-1">
            <ChatBubbleLeftIcon class="w-4 h-4" />
            <span>{{ ticket.comments_count }}</span>
          </div>
          
          <div v-if="ticket.due_date" class="flex items-center space-x-1">
            <ClockIcon class="w-4 h-4" />
            <span :class="{ 'text-red-600': ticket.is_overdue }">
              {{ formattedDueDate }}
            </span>
            <ExclamationTriangleIcon v-if="ticket.is_overdue" class="w-4 h-4 text-red-600" />
          </div>
          
          <span>{{ formattedDate }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>