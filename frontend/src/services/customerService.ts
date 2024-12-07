import axios from 'axios'
import { API_BASE_URL, API_ENDPOINTS } from '../config/api'
import { ShopBrandEnum, CustomerSourceEnum, CustomerTypeEnum, CustomerStatusEnum } from '../config/enums'

// 创建axios实例
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

// 枚举转换映射
const enumConversionMap = {
  shop: {
    'YI': '依',
    'LI': '丽',
    'MO': '末'
  },
  source: {
    'NATURAL_FLOW': '自然流量',
    'RECOMMENDED': '推荐'
  },
  customerType: {
    'NEW': '新客户',
    'OLD': '老客户',
    'OLD_CHANGED_ID': '换号'
  },
  customerStatus: {
    'CONSULTING': '咨询中',
    'SAMPLE': '样品',
    'PREPARING_ORDER': '准备下单',
    'DEAD': '死了'
  }
}

// 枚举转换工具函数
function convertToFrontendEnum(enumType: string, value: string): string {
  const conversionMap = enumConversionMap[enumType]
  if (!conversionMap) return value

  return conversionMap[value] || value
}

// 客户类型定义
export interface Customer {
    id?: string
    shop: typeof ShopBrandEnum[keyof typeof ShopBrandEnum]
    customer_id: string
    source: typeof CustomerSourceEnum[keyof typeof CustomerSourceEnum]
    customer_type: typeof CustomerTypeEnum[keyof typeof CustomerTypeEnum]
    demand: number
    demand_description?: string | null
    customer_status: typeof CustomerStatusEnum[keyof typeof CustomerStatusEnum]
    expected_order_date?: string | null
    expected_order_amount?: number | null
    last_modified_date?: string | null
    creation_date?: string | null
    isEmpty?: boolean
}

// 客户服务
export const customerService = {
    // 获取客户列表
    async getCustomers() {
        try {
            const response = await apiClient.get(API_ENDPOINTS.CUSTOMERS.LIST)
            return response.data
        } catch (error) {
            console.error('Error fetching customers:', error)
            if (axios.isAxiosError(error) && error.response) {
                console.error('Error details:', error.response.data)
            }
            throw error
        }
    },

    // 创建客户
    async createCustomer(customer: Omit<Customer, 'id' | 'last_modified_date' | 'creation_date'>) {
      try {
        // 验证 customer_id 格式
        if (!customer.customer_id || !/^[a-zA-Z0-9_-]{3,50}$/.test(customer.customer_id)) {
          throw new Error('客户ID必须是3-50个字符，只能包含字母、数字、下划线和连字符')
        }

        const backendCustomer = {
          customer_id: customer.customer_id,
          shop: customer.shop,         // 直接使用枚举键（英文值）
          source: customer.source,     // 直接使用枚举键（英文值）
          customer_type: customer.customer_type,  // 直接使用枚举键（英文值）
          customer_status: customer.customer_status,  // 直接使用枚举键（英文值）
          demand: customer.demand || 1,
          demand_description: customer.demand_description || null,
          expected_order_date: customer.expected_order_date || null,
          expected_order_amount: customer.expected_order_amount || null
        }

        console.log('创建客户 - 发送数据:', backendCustomer)
        const response = await apiClient.post(API_ENDPOINTS.CUSTOMERS.CREATE, backendCustomer)
        console.log('创建客户 - 响应:', response.data)
        return response.data
      } catch (error) {
        console.error('创建客户失败:', error)
        throw error
      }
    },

    // 更新客户
    async updateCustomer(id: string | number, customer: Partial<Customer>) {
        try {
            if (customer.customer_id && !/^[a-zA-Z0-9_-]{3,50}$/.test(customer.customer_id)) {
                throw new Error('客户ID必须是3-50个字符，只能包含字母、数字、下划线和连字符')
            }

            const backendCustomer: Partial<Customer> = {}
            
            // 直接使用枚举键（英文值）
            if (customer.shop) backendCustomer.shop = customer.shop
            if (customer.source) backendCustomer.source = customer.source
            if (customer.customer_type) backendCustomer.customer_type = customer.customer_type
            if (customer.customer_status) backendCustomer.customer_status = customer.customer_status
            
            // 其他字段直接复制
            if (customer.customer_id) backendCustomer.customer_id = customer.customer_id
            if (customer.demand) backendCustomer.demand = customer.demand
            if (customer.demand_description) backendCustomer.demand_description = customer.demand_description
            if (customer.expected_order_date) backendCustomer.expected_order_date = customer.expected_order_date
            if (customer.expected_order_amount) backendCustomer.expected_order_amount = customer.expected_order_amount

            console.log('更新客户 - 发送数据:', { id, backendCustomer })
            
            // 优先使用数字ID更新
            let response
            if (typeof id === 'number') {
              response = await apiClient.put(API_ENDPOINTS.CUSTOMERS.UPDATE_BY_ID(id), backendCustomer)
            } else {
              response = await apiClient.put(API_ENDPOINTS.CUSTOMERS.UPDATE(id), backendCustomer)
            }
            
            console.log('更新客户 - 响应:', response.data)
            return response.data
        } catch (error) {
            console.error('更新客户失败:', error)
            throw error
        }
    },

    // 删除客户
    async deleteCustomer(id: string) {
        try {
            const response = await apiClient.delete(API_ENDPOINTS.CUSTOMERS.DELETE(id))
            return response.data
        } catch (error) {
            console.error('Error deleting customer:', error)
            if (axios.isAxiosError(error) && error.response) {
                console.error('Error details:', error.response.data)
            }
            throw error
        }
    }
}
