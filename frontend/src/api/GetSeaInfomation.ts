import axios, { AxiosError, AxiosResponse } from 'axios'

export interface ApiResponse<T> {
  response: T
  error: {
    error_code: string
    error_msg: string
  }
}

export interface GetSeaInfomationList {
  response: {
    requests: Array<Request>
  }
}

export interface GetSeaInfomationCSV {
  response: {
    requests: any
  }
}

export const getSeaInfomationList = async () => {
  return await axios
    .get('/api/sea/info/list/')
    .then((res: AxiosResponse<ApiResponse<GetSeaInfomationList['response']>>) => {
      const data = res.data
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

export const getSeaInfomationCSV = async () => {
  return await axios
    .get('/api/sea/list/output/csv/', {
      responseType: 'blob'
    })
    .then((res: any) => res)
    .catch((err: AxiosError<any>) => {
      const data: any = err.response?.data ?? {
        status: 'FIELD',
        message: err.message
      }
      return data
    })
}

export const postWaveHeight = async (id: Number, waveHeight: String) => {
  return await axios
    .post(`/api/wave/info/wave_height/${id}`, {
      wave_height: waveHeight
    })
    .then((res) => res)
    .catch((err) => {
      throw err
    })
}

export const postWaveQuality = async (id: Number, waveQuality: String) => {
  return await axios
    .post(`/api/wave/info/wave_quality/${id}`, {
      wave_quality: waveQuality
    })
    .then((res) => res)
    .catch((err) => {
      throw err
    })
}
