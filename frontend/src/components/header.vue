<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref } from 'vue'
const title = ref('波予測システム')
const drawer = ref(false)
const group = ref<null | string>(null)

const router = useRouter()
const goToHome = () => {
  router.push('/')
}
const goToSeaInfomationView = () => {
  router.push('/SeaInfomation')
}
const goToCreateModelView = () => {
  router.push('/Learning')
}
</script>

<template>
  <v-card class="mx-auto overflow-hidden">
    <v-app-bar color="deep-purple" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>{{ title }}</v-toolbar-title>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app>
      <v-list nav dense>
        <v-list-item-group v-model="group" active-class="deep-purple--text text--accent-4">
          <v-list-item @click="goToHome">
            <v-list-item-icon>
              <v-icon>mdi-home</v-icon>
            </v-list-item-icon>
            <v-list-item-title>ホーム</v-list-item-title>
          </v-list-item>

          <v-list-item @click="goToSeaInfomationView">
            <v-list-item-icon>
              <v-icon>mdi-waves</v-icon>
            </v-list-item-icon>
            <v-list-item-title>海情報一覧画面</v-list-item-title>
          </v-list-item>

          <v-list-item @click="goToCreateModelView">
            <v-list-item-icon>
              <v-icon>mdi-robot-angry-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-title>モデル作成</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
  </v-card>
</template>
