<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { format, formatDistanceToNow } from 'date-fns'
import Layout from '../components/Layout.vue'
import { useTicketsStore } from '../stores/tickets'
import { useAuthStore } from '../stores/auth'
import type { Ticket } from '../types'
import {
  ChatBubbleLeftIcon,
  ClockIcon,
  UserIcon,
  CalendarIcon,
  ExclamationTriangleIcon,
} from '@heroicons/vue/24/outline'

const route = useRoute()
const ticketsStore = useTicketsStore()
const authStore = useAuthStore()

const ticket = ref<Ticket | null>(null)
const newComment = ref('')
const isLoading = ref(false)
const isSubmittingComment = ref(false)

const ticketId = computed(() => parseInt(route.params.id as string))

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
  if (!ticket.value) return ''
  return format(new Date(ticket.value.created_at), 'MMM dd, yyyy at h:mm a')
})

const formattedDueDate = computed(() => {
  if (!ticket.value?.due_date) return null
  return format(new Date(ticket.value.due_date), 'MMM dd, yyyy at h:mm a')
})

const handleStatusChange = async (newStatus: string) => {
  if (!ticket.value) return
  
  try {
    const updatedTicket = await ticketsStore.updateTicket(ticket.value.id, { status: newStatus })
    ticket.value = updatedTicket
  } catch (error) {
    console.error('Error updating ticket status:', error)
  }
}

const handleAddComment = async () => {
  if (!ticket.value || !newComment.value.trim()) return
  
  try {
    isSubmittingComment.value = true
    await ticketsStore.addComment(ticket.value.id, newComment.value)
    newComment.value = ''
    
    // Refresh ticket to get updated comments
    const updatedTicket = await ticketsStore.fetchTicket(ticket.value.id)
    ticket.value = updatedTicket
  } catch (error) {
    console.error('Error adding comment:', error)
  } finally {
    isSubmittingComment.value = false
  }
}

const formatCommentDate = (dateString: string) => {
  return formatDistanceToNow(new Date(dateString), { addSuffix: true })
}

onMounted(async () => {
  try {
    isLoading.value = true
    ticket.value = await ticketsStore.fetchTicket(ticketId.value)
  } catch (error) {
    console.error('Error fetching ticket:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <Layout>
    <template #title>
      <span v-if="ticket">Ticket #{{ ticket.id }}</span>
      <span v-else>Loading...</span>
    </template>
    
    <div v-if="isLoading" class="text-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
      <p class="text-gray-600 mt-2">Loading ticket...</p>
    </div>

    <div v-else-if="ticket" class="max-w-4xl mx-auto space-y-6">
      <!-- Ticket Header -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="flex-1 min-w-0">
            <h1 class="text-2xl font-bold text-gray-900 mb-2">
              #{{ ticket.id }} - {{ ticket.title }}
            </h1>
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <div class="flex items-center space-x-1">
                <UserIcon class="w-4 h-4" />
                <span>Created by {{ ticket.created_by.username }}</span>
              </div>
              <div class="flex items-center space-x-1">
                <CalendarIcon class="w-4 h-4" />
                <span>{{ formattedDate }}</span>
              </div>
              <div v-if="ticket.due_date" class="flex items-center space-x-1">
                <ClockIcon class="w-4 h-4" />
                <span :class="{ 'text-red-600': ticket.is_overdue }">
                  Due: {{ formattedDueDate }}
                </span>
                <ExclamationTriangleIcon v-if="ticket.is_overdue" class="w-4 h-4 text-red-600" />
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-2 ml-4">
            <span
              :class="priorityColors[ticket.priority]"
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
            >
              {{ ticket.priority }}
            </span>
            <span
              :class="statusColors[ticket.status]"
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
            >
              {{ ticket.status.replace('_', ' ') }}
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-gray-50 rounded-lg">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <p class="text-sm text-gray-900">{{ ticket.category.name }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Assigned to</label>
            <p class="text-sm text-gray-900">
              {{ ticket.assigned_to ? ticket.assigned_to.username : 'Unassigned' }}
            </p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              :value="ticket.status"
              @change="handleStatusChange($event.target.value)"
              class="form-select text-sm"
            >
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="pending">Pending</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Ticket Description -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Description</h2>
        <div class="prose max-w-none">
          <p class="text-gray-700 whitespace-pre-wrap">{{ ticket.description }}</p>
        </div>
      </div>

      <!-- Comments Section -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900 flex items-center">
            <ChatBubbleLeftIcon class="w-5 h-5 mr-2" />
            Comments ({{ ticket.comments?.length || 0 }})
          </h2>
        </div>
        
        <div class="divide-y divide-gray-200">
          <div
            v-for="comment in ticket.comments"
            :key="comment.id"
            class="p-6"
          >
            <div class="flex items-start space-x-3">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                  <span class="text-primary-600 text-sm font-medium">
                    {{ comment.author.username.charAt(0).toUpperCase() }}
                  </span>
                </div>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center space-x-2 mb-1">
                  <span class="text-sm font-medium text-gray-900">{{ comment.author.username }}</span>
                  <span class="text-sm text-gray-500">{{ formatCommentDate(comment.created_at) }}</span>
                </div>
                <p class="text-gray-700 whitespace-pre-wrap">{{ comment.content }}</p>
              </div>
            </div>
          </div>
          
          <div v-if="!ticket.comments?.length" class="p-6 text-center text-gray-500">
            No comments yet. Be the first to comment!
          </div>
        </div>

        <!-- Add Comment Form -->
        <div class="p-6 border-t border-gray-200 bg-gray-50">
          <form @submit.prevent="handleAddComment" class="space-y-4">
            <div>
              <label for="comment" class="block text-sm font-medium text-gray-700 mb-1">
                Add a comment
              </label>
              <textarea
                id="comment"
                v-model="newComment"
                rows="3"
                class="form-textarea"
                placeholder="Type your comment here..."
                required
              />
            </div>
            <div class="flex justify-end">
              <button
                type="submit"
                :disabled="isSubmittingComment || !newComment.trim()"
                class="btn-primary"
              >
                <span v-if="isSubmittingComment">Posting...</span>
                <span v-else>Post Comment</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <p class="text-gray-600">Ticket not found.</p>
    </div>
  </Layout>
</template>