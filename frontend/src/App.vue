<script setup lang="ts">
import { NConfigProvider, NMessageProvider } from 'naive-ui'
import NaiveTest from './components/CustomerList.vue'
</script>

<template>
  <n-config-provider>
    <n-message-provider>
      <NaiveTest />
    </n-message-provider>
  </n-config-provider>
</template>