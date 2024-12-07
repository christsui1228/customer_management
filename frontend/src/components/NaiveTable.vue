<script setup lang="ts">
import { h, ref } from 'vue'
import { NButton, NDataTable } from 'naive-ui'

// 定义数据类型
interface RowData {
  key: number
  name: string
  age: number
  address: string
}

// 表格数据
const data = ref<RowData[]>([
  {
    key: 1,
    name: '张三',
    age: 28,
    address: '北京市朝阳区'
  },
  {
    key: 2,
    name: '李四',
    age: 32,
    address: '上海市浦东新区'
  },
  {
    key: 3,
    name: '王五',
    age: 25,
    address: '广州市天河区'
  }
])

// 定义列
const columns = [
  {
    title: '姓名',
    key: 'name'
  },
  {
    title: '年龄',
    key: 'age'
  },
  {
    title: '地址',
    key: 'address'
  },
  {
    title: '操作',
    key: 'actions',
    render(row: RowData) {
      return h(
        NButton,
        {
          size: 'small',
          onClick: () => handleEdit(row)
        },
        { default: () => '编辑' }
      )
    }
  }
]

// 处理编辑点击
function handleEdit(row: RowData) {
  console.log('编辑:', row)
}
</script>

<template>
  <div>
    <n-data-table
      :columns="columns"
      :data="data"
      :bordered="false"
      :single-line="false"
    />
  </div>
</template>