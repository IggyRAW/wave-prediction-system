<script setup lang="ts">
import Progress from '@/components/progress.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const backToPage = () => {
  router.push('/')
}
</script>

<template>
  <v-app>
    <v-main>
      <h1>これはモデル作成ページ</h1>
      <v-container class="d-flex align-center justify-center" style="min-height: 100vh; padding: 0">
        <Progress />
      </v-container>
      <v-btn @click="backToPage"> 戻る </v-btn>
    </v-main>
  </v-app>
</template>
