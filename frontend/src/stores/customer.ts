import { defineStore } from 'pinia'
import type { Customer } from '../services/customerService'

export const useCustomerStore = defineStore('customer', {
  state: () => ({
    customers: [] as Customer[],
    loading: false
  }),
  actions: {
    setCustomers(customers: Customer[]) {
      this.customers = customers
    },
    setLoading(loading: boolean) {
      this.loading = loading
    }
  }
})
