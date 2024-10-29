<script setup lang="ts">
import { ref } from 'vue'

const progress = ref<number>(0)
const isDisabled = ref(false)

const RealTime = () => {
  isDisabled.value = true
  const ws = new WebSocket('ws://localhost:3000/weather/')

  ws.onmessage = (event: MessageEvent) => {
    const data = event.data
    if (data.includes('Progress')) {
      progress.value = parseInt(data.split(': ')[1])
    } else if (data === 'Complete') {
      console.log('Data upload complete')
    }
  }

  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
  }

  ws.onclose = () => {
    console.log('WebSocket connection closed')
    isDisabled.value = false
  }
}
</script>

<template>
  <div>
    <v-btn @click="RealTime" :disabled="isDisabled">波情報データ受信</v-btn>
    <p>{{ progress }}%</p>
    <progress :value="progress" max="100"></progress>
  </div>
</template>
