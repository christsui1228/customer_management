// utils/request.ts
import axios from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 5000
})

request.interceptors.request.use(
  config => {
    // 请求拦截
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

request.interceptors.response.use(
  response => {
    // 响应拦截
    return response.data
  },
  error => {
    return Promise.reject(error)
  }
)

export default request