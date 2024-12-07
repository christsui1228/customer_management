<template>
  <n-card>
    <n-space vertical>
      <n-space>
        <n-button type="primary" @click="handleCreate">
          <template #icon>
            <n-icon><Add /></n-icon>
          </template>
          新建客户
        </n-button>
        <n-input
          v-model:value="filters.shop"
          placeholder="搜索店铺"
          clearable
          @clear="handleClearFilter('shop')"
        >
          <template #prefix>
            <n-icon><Search /></n-icon>
          </template>
        </n-input>
        <n-input
          v-model:value="filters.customer_id"
          placeholder="搜索客户"
          clearable
          @clear="handleClearFilter('customer_id')"
        >
          <template #prefix>
            <n-icon><Search /></n-icon>
          </template>
        </n-input>
      </n-space>
      <n-data-table
        :loading="customerStore.loading"
        :columns="columns"
        :data="tableData"
        :pagination="pagination"
        :bordered="true"
        :single-line="false"
      />
    </n-space>

    <!-- 新建/编辑客户对话框 -->
    <n-modal
      v-model:show="showModal"
      :title="isEditing ? '编辑客户' : '新建客户'"
      preset="dialog"
      :positive-text="isEditing ? '保存' : '创建'"
      :negative-text="'取消'"
      @positive-click="handleModalConfirm"
      @negative-click="handleModalCancel"
    >
      <n-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-placement="left"
        label-width="auto"
        require-mark-placement="right-hanging"
      >
        <n-form-item label="店铺" path="shop">
          <n-select v-model:value="formData.shop" :options="shops" />
        </n-form-item>
        <n-form-item label="客户ID" path="customer_id">
          <n-input v-model:value="formData.customer_id" placeholder="请输入客户ID" />
        </n-form-item>
        <n-form-item label="来源" path="source">
          <n-select v-model:value="formData.source" :options="customerSources" />
        </n-form-item>
        <n-form-item label="客户类型" path="customer_type">
          <n-select v-model:value="formData.customer_type" :options="customerTypes" />
        </n-form-item>
        <n-form-item label="需求量" path="demand">
          <n-input-number v-model:value="formData.demand" :min="1" />
        </n-form-item>
        <n-form-item label="需求描述" path="demand_description">
          <n-input v-model:value="formData.demand_description" type="textarea" placeholder="请输入需求描述" />
        </n-form-item>
        <n-form-item label="客户状态" path="customer_status">
          <n-select v-model:value="formData.customer_status" :options="customerStatuses" />
        </n-form-item>
        <n-form-item label="预计下单时间" path="expected_order_date">
          <n-date-picker v-model:value="formData.expected_order_date" type="date" clearable />
        </n-form-item>
        <n-form-item label="预计下单金额" path="expected_order_amount">
          <n-input-number v-model:value="formData.expected_order_amount" clearable />
        </n-form-item>
      </n-form>
    </n-modal>
  </n-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, h } from 'vue'
import {
  NDataTable,
  NButton,
  NInput,
  NInputNumber,
  NSelect,
  NDatePicker,
  useMessage,
  NIcon,
  NSpace,
  NCard,
  NModal,
  NForm,
  NFormItem,
  FormInst,
  FormRules
} from 'naive-ui'
import { TrashOutline, Search, Add, CreateOutline } from '@vicons/ionicons5'
import { Customer, customerService } from '../services/customerService'
import { useCustomerStore } from '../stores/customer'
import { 
  ShopBrandEnum, 
  CustomerSourceEnum, 
  CustomerTypeEnum, 
  CustomerStatusEnum,
  enumLabels 
} from '../config/enums'
import axios from 'axios'

const message = useMessage()
const customerStore = useCustomerStore()
const formRef = ref<FormInst | null>(null)

// 表单数据
const formData = reactive<Partial<Customer>>({
  shop: '',
  customer_id: '',
  source: '',
  customer_type: '',
  demand: 1,
  demand_description: '',
  customer_status: '',
  expected_order_date: null,
  expected_order_amount: null
})

// 表单验证规则
const rules: FormRules = {
  shop: {
    required: true,
    message: '请选择店铺',
    trigger: ['blur', 'change']
  },
  customer_id: {
    required: true,
    message: '请输入客户ID',
    trigger: ['blur', 'change']
  },
  source: {
    required: true,
    message: '请选择来源',
    trigger: ['blur', 'change']
  },
  customer_type: {
    required: true,
    message: '请选择客户类型',
    trigger: ['blur', 'change']
  },
  demand: {
    required: true,
    type: 'number',
    min: 1,
    message: '需求量必须大于0',
    trigger: ['blur', 'change']
  },
  customer_status: {
    required: true,
    message: '请选择客户状态',
    trigger: ['blur', 'change']
  }
}

// 对话框控制
const showModal = ref(false)
const isEditing = ref(false)
const editingCustomer = ref<Customer | null>(null)

// 筛选条件
const filters = ref({
  shop: '',
  customer_id: ''
})

// 店铺选项
const shops = Object.entries(ShopBrandEnum).map(([key]) => ({
  label: enumLabels.shop[key],
  value: key
}))

// 客户来源选项
const customerSources = Object.entries(CustomerSourceEnum).map(([key]) => ({
  label: enumLabels.source[key],
  value: key
}))

// 客户类型选项
const customerTypes = Object.entries(CustomerTypeEnum).map(([key]) => ({
  label: enumLabels.customerType[key],
  value: key
}))

// 客户状态选项
const customerStatuses = Object.entries(CustomerStatusEnum).map(([key]) => ({
  label: enumLabels.customerStatus[key],
  value: key
}))

// 加载客户列表
async function loadCustomers() {
  try {
    customerStore.customers = await customerService.getCustomers()
  } catch (error) {
    console.error('加载客户列表失败:', error)
    message.error('加载客户列表失败')
  }
}

// 表格数据
const tableData = computed(() => {
  return customerStore.customers.filter(customer => {
    const shopMatch = !filters.value.shop || 
      customer.shop.toLowerCase().includes(filters.value.shop.toLowerCase())
    const idMatch = !filters.value.customer_id || 
      customer.customer_id.toLowerCase().includes(filters.value.customer_id.toLowerCase())
    return shopMatch && idMatch
  })
})

// 处理新建客户
function handleCreate() {
  isEditing.value = false
  editingCustomer.value = null
  // 重置表单数据
  Object.assign(formData, {
    shop: '',
    customer_id: '',
    source: '',
    customer_type: '',
    demand: 1,
    demand_description: '',
    customer_status: '',
    expected_order_date: null,
    expected_order_amount: null
  })
  showModal.value = true
}

// 处理编辑客户
function handleEdit(row: Customer) {
  isEditing.value = true
  editingCustomer.value = row
  // 填充表单数据
  Object.assign(formData, {
    shop: row.shop,
    customer_id: row.customer_id,
    source: row.source,
    customer_type: row.customer_type,
    demand: row.demand,
    demand_description: row.demand_description,
    customer_status: row.customer_status,
    expected_order_date: row.expected_order_date,
    expected_order_amount: row.expected_order_amount
  })
  showModal.value = true
}

// 处理对话框确认
async function handleModalConfirm() {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    
    if (isEditing.value && editingCustomer.value) {
      // 更新客户
      const updateId = editingCustomer.value.id || editingCustomer.value.customer_id
      const updatedCustomer = await customerService.updateCustomer(updateId, formData)
      
      // 更新本地数据
      const index = customerStore.customers.findIndex(c => 
        (editingCustomer.value?.id && c.id === editingCustomer.value.id) || 
        c.customer_id === editingCustomer.value?.customer_id
      )
      if (index !== -1) {
        customerStore.customers[index] = updatedCustomer
      }
      
      message.success('客户更新成功')
    } else {
      // 创建客户
      const createdCustomer = await customerService.createCustomer(formData as Customer)
      customerStore.customers.push(createdCustomer)
      message.success('客户创建成功')
    }
    
    showModal.value = false
  } catch (error) {
    console.error(isEditing.value ? '更新客户失败:' : '创建客户失败:', error)
    if (axios.isAxiosError(error)) {
      const errorMessage = error.response?.data?.detail || 
                          error.response?.data?.message || 
                          '未知错误'
      message.error(`${isEditing.value ? '更新' : '创建'}客户失败：${errorMessage}`)
    } else {
      message.error(`${isEditing.value ? '更新' : '创建'}客户失败：未知错误`)
    }
  }
}

// 处理对话框取消
function handleModalCancel() {
  showModal.value = false
}

// 处理删除
async function handleDelete(row: Customer) {
  try {
    await customerService.deleteCustomer(row.customer_id)
    
    // 更新本地数据
    const index = customerStore.customers.findIndex(c => c.customer_id === row.customer_id)
    if (index !== -1) {
      customerStore.customers.splice(index, 1)
    }
    
    message.success('客户删除成功')
  } catch (error) {
    console.error('删除客户失败:', error)
    if (axios.isAxiosError(error)) {
      const errorMessage = error.response?.data?.detail || 
                          error.response?.data?.message || 
                          '未知错误'
      message.error(`删除客户失败：${errorMessage}`)
    } else {
      message.error('删除客户失败：未知错误')
    }
  }
}

// 清除筛选条件
function handleClearFilter(field: string) {
  filters.value[field] = ''
}

// 分页配置
const pagination = reactive({
  page: 1,
  pageSize: 10,
  onChange(page: number) {
    pagination.page = page
  },
  onUpdatePageSize(pageSize: number) {
    pagination.pageSize = pageSize
    pagination.page = 1
  }
})

// 表格列定义
const columns = [
  {
    title: '店铺',
    key: 'shop',
    render(row: Customer) {
      return h('span', null, enumLabels.shop[row.shop] || row.shop)
    }
  },
  {
    title: '客户ID',
    key: 'customer_id'
  },
  {
    title: '来源',
    key: 'source',
    render(row: Customer) {
      return h('span', null, enumLabels.source[row.source] || row.source)
    }
  },
  {
    title: '客户类型',
    key: 'customer_type',
    render(row: Customer) {
      return h('span', null, enumLabels.customerType[row.customer_type] || row.customer_type)
    }
  },
  {
    title: '需求量',
    key: 'demand'
  },
  {
    title: '需求描述',
    key: 'demand_description'
  },
  {
    title: '客户状态',
    key: 'customer_status',
    render(row: Customer) {
      return h('span', null, enumLabels.customerStatus[row.customer_status] || row.customer_status)
    }
  },
  {
    title: '预计下单时间',
    key: 'expected_order_date'
  },
  {
    title: '预计下单金额',
    key: 'expected_order_amount'
  },
  {
    title: '最新修改日期',
    key: 'last_modified_date'
  },
  {
    title: '创建日期',
    key: 'creation_date'
  },
  {
    title: '操作',
    key: 'actions',
    render(row: Customer) {
      return h(NSpace, null, {
        default: () => [
          h(
            NButton,
            {
              type: 'info',
              size: 'small',
              onClick: () => handleEdit(row)
            },
            {
              icon: () => h(NIcon, null, { default: () => h(CreateOutline) }),
              default: () => '编辑'
            }
          ),
          h(
            NButton,
            {
              type: 'error',
              size: 'small',
              onClick: () => handleDelete(row)
            },
            {
              icon: () => h(NIcon, null, { default: () => h(TrashOutline) }),
              default: () => '删除'
            }
          )
        ]
      })
    }
  }
]

// 在组件挂载时获取数据
onMounted(async () => {
  await loadCustomers()
})
</script>

<style scoped>
.n-input {
  min-width: 200px;
}
</style>