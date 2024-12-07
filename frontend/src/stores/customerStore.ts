import { defineStore } from 'pinia'
import { ref } from 'vue'

interface Customer {
  id?: number
  shop_id: string
  customer_id: string
  customer_type: string
  customer_needs: string
  situation_desc: string
  expected_order_time: string | null
  expected_order_amount: number | null
}

// 确保使用 export const
export const useCustomerStore = defineStore('customer', () => {
  const customers = ref<Customer[]>([])
  const loading = ref(false)
  const currentCustomer = ref<Customer | null>(null)

  async function fetchCustomers() {
    loading.value = true
    try {
      const response = await fetch('/api/customers')
      const data = await response.json()
      customers.value = data
    } catch (error) {
      console.error('获取客户列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function createCustomer(customerData: Customer): Promise<Customer> {
    try {
      const response = await fetch('/api/customers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(customerData)
      })
      const data = await response.json()
      customers.value.push(data)
      return data
    } catch (error) {
      console.error('创建客户失败:', error)
      throw error
    }
  }

  async function updateCustomer(id: number, customerData: Customer): Promise<Customer> {
    try {
      const response = await fetch(`/api/customers/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(customerData)
      })
      const data = await response.json()
      const index = customers.value.findIndex(c => c.id === id)
      if (index !== -1) {
        customers.value[index] = data
      }
      return data
    } catch (error) {
      console.error('更新客户失败:', error)
      throw error
    }
  }

  async function deleteCustomer(id: number): Promise<void> {
    try {
      await fetch(`/api/customers/${id}`, {
        method: 'DELETE'
      })
      const index = customers.value.findIndex(c => c.id === id)
      if (index !== -1) {
        customers.value.splice(index, 1)
      }
    } catch (error) {
      console.error('删除客户失败:', error)
      throw error
    }
  }

  function setCurrentCustomer(customer: Customer): void {
    currentCustomer.value = customer
  }

  return {
    customers,
    loading,
    currentCustomer,
    fetchCustomers,
    createCustomer,
    updateCustomer,
    deleteCustomer,
    setCurrentCustomer
  }
})