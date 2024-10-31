<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import Header from '@/components/header.vue'
import * as SeaInfomationApi from '@/api/GetSeaInfomation'
import { reverseWaveHeightDic, reverseWaveQualityDic } from '@/api/GetSeaInfomation'

// テーブルボディ
let sea_info_body = ref([])

const waveHeightOptions = [
  '',
  '頭オーバー',
  '頭',
  '肩',
  'ムネ',
  'ハラ',
  'コシ',
  'モモ',
  '膝',
  'フラット'
]
const waveQualityOptions = ['', 'とても良い', '良い', '悪い', 'とても悪い']

onMounted(() => {
  getWaveInfoList()
})

async function getWaveInfoList() {
  try {
    sea_info_body.value = await SeaInfomationApi.getSeaInfomationList()
  } catch (error) {
    console.error('データの取得に失敗しました。')
  }
}

const router = useRouter()

const headers = ref([
  { title: 'No.', sortable: true, align: 'center', key: 'id', width: '5%' },
  { title: '日付', sortable: true, align: 'center', key: 'time' },
  { title: '風向', sortable: false, align: 'center', key: 'wind_direction' },
  { title: '風(m)', sortable: false, align: 'center', key: 'wind' },
  { title: '波向', sortable: false, align: 'center', key: 'wave_direction' },
  { title: '沿岸波浪(m)', sortable: false, align: 'center', key: 'coastal_waves' },
  { title: '周期(秒)', sortable: false, align: 'center', key: 'period' },
  { title: '潮汐(cm)', sortable: false, align: 'center', key: 'tide' },
  { title: '波高', sortable: false, align: 'center', key: 'wave_height' },
  { title: '波質', sortable: false, align: 'center', key: 'wave_quality' }
])

const updateWaveHeight = (item: any) => {
  try {
    console.log('波高更新:', item.wave_height)
    const waveHeight = reverseWaveHeightDic.get(item.wave_height) || 0
    SeaInfomationApi.postWaveHeight(item.id, waveHeight)
  } catch (error) {
    console.log(error)
  }
}

const updateWaveQuality = (item: any) => {
  try {
    console.log('波質更新:', item.wave_quality)
    const waveQuality = reverseWaveQualityDic.get(item.wave_quality) || 0
    SeaInfomationApi.postWaveQuality(item.id, waveQuality)
  } catch (error) {
    console.log(error)
  }
}

const exportToCsv = () => {
  try {
    console.log('CSV出力処理開始')
    // ヘッダーの作成
    const header = headers.value.map((h) => h.key).join(',')
    const rows = sea_info_body.value.map((item) => headers.value.map((h) => item[h.key]).join(','))
    const csvContent = [header, ...rows].join('\n')

    // Blobを使用してCSVファイル出力
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)

    // ダウンロードリンクを生成
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'sea_info.csv')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (error) {
    console.log(error)
  }
}

const backToPage = () => {
  router.push('/')
}
</script>

<template>
  <v-app>
    <!-- ヘッダー -->
    <Header />

    <!-- メイン -->
    <v-main>
      <v-container>
        <v-row>
          <v-col cols="6">
            <div class="title">
              <h4>海情報一覧画面</h4>
            </div>
          </v-col>
        </v-row>
        <div class="text-right">
          <v-btn class="output-csv-btn" variant="tonal" @click="exportToCsv">CSV</v-btn>
          <v-btn class="return-btn" variant="tonal" @click="backToPage"> 戻る </v-btn>
        </div>

        <div class="outer-border">
          <v-data-table
            class="wave-quality-table"
            :headers="headers"
            :items="sea_info_body"
            items-per-page-text="表示行数"
            header-class="custom-header"
          >
            <template v-slot:item.wave_height="{ item }">
              <v-select
                v-model="item.wave_height"
                :items="waveHeightOptions"
                label="波高"
                @update:model-value="updateWaveHeight(item)"
                hide-details
              ></v-select>
            </template>
            <template v-slot:item.wave_quality="{ item }">
              <v-select
                v-model="item.wave_quality"
                :items="waveQualityOptions"
                label="波質"
                @update:model-value="updateWaveQuality(item)"
                hide-details
              ></v-select>
            </template>
          </v-data-table>
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>
<style scoped>
.title {
  margin-bottom: 15px;
  font-size: 50px;
}
.outer-border {
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-top: 10px;
  margin-bottom: 10px;
}
.v-data-table.wave-quality-table {
  font-size: 20px;
  padding: 10px;
}
.custom-header {
  background-color: #1976d2; /* 背景色: Vuetifyのデフォルトブルー */
  color: white; /* 文字色: 白 */
}
.v-btn.edit-btn {
  background-color: darkgreen;
  color: aliceblue;
}
.v-btn.output-csv-btn {
  background: #9999cc;
  font-size: 20px;
  width: 100px;
  height: 40px;
  margin-left: 10px;
}
.v-btn.return-btn {
  font-size: 20px;
  width: 100px;
  height: 40px;
  margin-left: 10px;
}
</style>
