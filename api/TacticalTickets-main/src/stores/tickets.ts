import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'
import type { Ticket, TicketCreate, Category, DashboardStats } from '../types'

export const useTicketsStore = defineStore('tickets', () => {
  const tickets = ref<Ticket[]>([])
  const categories = ref<Category[]>([])
  const dashboardStats = ref<DashboardStats | null>(null)
  const isLoading = ref(false)

  const fetchTickets = async (params?: any) => {
    isLoading.value = true
    try {
      const response = await api.get('/tickets/', { params })
      tickets.value = response.data.results
      return response.data
    } catch (error) {
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const fetchTicket = async (id: number) => {
    try {
      const response = await api.get(`/tickets/${id}/`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  const createTicket = async (ticketData: TicketCreate) => {
    try {
      const response = await api.post('/tickets/', ticketData)
      tickets.value.unshift(response.data)
      return response.data
    } catch (error) {
      throw error
    }
  }

  const updateTicket = async (id: number, ticketData: Partial<Ticket>) => {
    try {
      const response = await api.patch(`/tickets/${id}/`, ticketData)
      const index = tickets.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tickets.value[index] = response.data
      }
      return response.data
    } catch (error) {
      throw error
    }
  }

  const deleteTicket = async (id: number) => {
    try {
      await api.delete(`/tickets/${id}/`)
      tickets.value = tickets.value.filter(t => t.id !== id)
    } catch (error) {
      throw error
    }
  }

  const fetchCategories = async () => {
    try {
      const response = await api.get('/categories/')
      categories.value = response.data.results
      return response.data
    } catch (error) {
      throw error
    }
  }

  const fetchDashboardStats = async () => {
    try {
      const response = await api.get('/tickets/dashboard_stats/')
      dashboardStats.value = response.data
      return response.data
    } catch (error) {
      throw error
    }
  }

  const addComment = async (ticketId: number, content: string) => {
    try {
      const response = await api.post(`/tickets/${ticketId}/add_comment/`, { content })
      return response.data
    } catch (error) {
      throw error
    }
  }

  return {
    tickets,
    categories,
    dashboardStats,
    isLoading,
    fetchTickets,
    fetchTicket,
    createTicket,
    updateTicket,
    deleteTicket,
    fetchCategories,
    fetchDashboardStats,
    addComment
  }
})