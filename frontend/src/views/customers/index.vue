<!-- views/customers/index.vue -->

import { createRouter, createWebHistory } from 'vue-router'

<template>
    <n-card>
      <n-space vertical>
        <n-space>
          <n-input
            v-model:value="customerStore.filters.customerName"
            placeholder="搜索客户"
            clearable
            @clear="customerStore.clearFilter('customerName')"
          >
            <template #prefix>
              <n-icon><Search /></n-icon>
            </template>
          </n-input>
        </n-space>
        <n-data-table
          :loading="customerStore.loading"
          :columns="columns"
          :data="customerStore.filteredCustomers"
          :pagination="pagination"
          @update:value="handleUpdateValue"
        />
      </n-space>
    </n-card>
  </template>
  
  <script setup lang="ts">
  import { ref, reactive, h, onMounted } from 'vue'
  import { useCustomerStore } from '@/stores/customerStore'
  import { customerTypes } from '@/constants'
  // ... 其他 import
  
  const customerStore = useCustomerStore()
  
  // 获取初始数据
  onMounted(() => {
    customerStore.fetchCustomers()
  })
  
  // columns定义基本相同,但需要使用store中的方法
  const columns = [
    {
      title: '店铺',
      key: 'store',
      render: (row: any) => {
        return h(NInput, {
          value: row.store,
          placeholder: '请输入店铺',
          onUpdateValue: (v) => {
            row.store = v
            if (v) row.isEmpty = false
            customerStore.ensureEmptyRows()
          }
        })
      }
    },
    // ... 其他列定义
  ]
  
  // 处理删除
  const handleDelete = async (row: any) => {
    try {
      await customerStore.deleteCustomer(row.id)
      message.success('删除成功')
    } catch (error) {
      message.error('删除失败')
    }
  }
  
  // 处理数据更新
  const handleUpdateValue = (customers: any[]) => {
    customerStore.$patch({ customers })
    customerStore.ensureEmptyRows()
  }
  </script>