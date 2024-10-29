<script setup lang="ts">
import Header from '@/components/header.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const inputWaveQuality = () => {
  router.push('/SeaInfomation')
}
</script>

<template>
  <v-app>
    <!-- ヘッダー -->
    <Header />

    <!-- メイン -->
    <v-main>
      <v-container class="d-flex align-center justify-center" style="min-height: 100vh; padding: 0">
        <v-row>
          <v-col cols="12">
            <v-btn @click="inputWaveQuality">海情報一覧画面</v-btn>
          </v-col>
          <v-col cols="12">
            <v-btn>モデル作成</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped>
.v-col {
  display: flex;
  align-items: center;
  justify-content: center;
}
.v-btn {
  height: 50px;
  width: 250px;
  font-size: large;
}
</style>
