<script setup lang="ts">
import { ref } from 'vue'

const per = ref<number>(0)
const isDisabled = ref(false)
const showProgress = ref(false)

const links = ['Get Wave Data', 'About Us']

function getWaveData() {
  isDisabled.value = true
  showProgress.value = true
  const ws = new WebSocket('ws://localhost:3000/weather/')

  ws.onmessage = (event: MessageEvent) => {
    const data = event.data
    if (data.includes('Progress')) {
      per.value = parseInt(data.split(': ')[1])
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
    showProgress.value = false
  }
}
</script>

<template>
  <v-footer class="bg-grey-lighten-1">
    <v-row justify="center" no-gutters>
      <v-col cols="12" class="text-center">
        <v-btn
          v-for="link in links"
          :key="link"
          class="mx-2"
          color="white"
          rounded="xl"
          variant="text"
          @click="link === 'Get Wave Data' ? getWaveData() : null"
          :isDisabled="link === 'Get Wave Data' ? isDisabled : false"
        >
          <v-icon v-if="link === 'Get Wave Data'" left>mdi-waves</v-icon>
          {{ link }}
        </v-btn>

        <!-- Get Wave Data ボタンの下にプログレスバーを表示 -->
        <v-progress-linear
          v-if="showProgress"
          indeterminate
          class="mt-2"
          color="blue"
        ></v-progress-linear>
      </v-col>

      <v-col class="text-center mt-4" cols="12">
        {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
      </v-col>
    </v-row>
  </v-footer>
</template>
