<script setup lang="ts">
import { useMessage } from 'naive-ui'

const message = useMessage()

function handleClick() {
  message.success('测试成功！')
}
</script>

<template>
  <n-button type="primary" @click="handleClick">
    点击显示消息
  </n-button>
</template>