import axios, { AxiosError, AxiosResponse } from 'axios'

const waveHeghtDic: Map<Number, String> = new Map([
  [1, '頭オーバー'],
  [2, '頭'],
  [3, '肩'],
  [4, 'ムネ'],
  [5, 'ハラ'],
  [6, 'コシ'],
  [7, 'モモ'],
  [8, '膝'],
  [9, 'フラット']
])
// 逆辞書を作成
export const reverseWaveHeightDic: Map<String, Number> = new Map(
  [...waveHeghtDic.entries()].map(([key, value]) => [value, key])
)

const waveQualityDic: Map<Number, String> = new Map([
  [1, 'と手も良い'],
  [2, '良い'],
  [3, '悪い'],
  [4, 'とても悪い']
])
// 逆辞書を作成
export const reverseWaveQualityDic: Map<String, Number> = new Map(
  [...waveQualityDic.entries()].map(([key, value]) => [value, key])
)

export interface ApiResponse<T> {
  response: T
  error: {
    error_code: string
    error_msg: string
  }
}

export interface GetWaveQualityList {
  response: {
    requests: Array<Request>
  }
}

export const getSeaInfomationList = async () => {
  return await axios
    .get('/api/sea/info/list/')
    .then((res: AxiosResponse<ApiResponse<GetWaveQualityList['response']>>) => {
      const data = res.data
      data.forEach((element: any) => {
        if (element.wave_height) {
          element.wave_height = waveHeghtDic.get(element.wave_height) || null
        }
        if (element.wave_quality) {
          element.wave_quality = waveQualityDic.get(element.wave_quality) || null
        }
      })
      return data
    })
    .catch((err: AxiosError<any>) => {
      const data: any = err.response?.data ?? {
        status: 'FIELD',
        message: err.message
      }
      return data
    })
}

export const postWaveHeight = async (id: Number, waveHeight: Number) => {
  return await axios
    .post(`/api/wave/info/wave_height/${id}`, null, {
      params: { waveHeight }
    })
    .then((res) => res)
    .catch((err) => {
      throw err
    })
}

export const postWaveQuality = async (id: Number, waveQuality: Number) => {
  return await axios
    .post(`/api/wave/info/wave_quality/${id}`, null, {
      params: { waveQuality }
    })
    .then((res) => res)
    .catch((err) => {
      throw err
    })
}