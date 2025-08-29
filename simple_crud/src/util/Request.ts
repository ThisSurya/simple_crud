'use server'
import axios, { AxiosError } from 'axios'
// import Cookies from 'js-cookie'
// import axios from "./BaseRequest";
interface requestparams {
  type: 'get' | 'post' | 'put' | 'delete' | 'patch'
  url?: string
  datas?: { [key: string]: any }
  headers?: { [key: string]: any }
  params?: { [key: string]: any }
}

export async function RequestHttp({
  type = 'get',
  url = '',
  datas = {},
  headers = { 'Content-Type': 'application/json' },
  params = {},
}: requestparams): Promise<any> {
  // const authkey = cookies().get('token')?.value ?? "";
  const token = localStorage.getItem('token')
  // return authkey
  const config = {
    method: type,
    url: import.meta.env.VITE_API_URL + url,
    headers: {
      ...headers,
      Authorization: `Bearer ${token}`,
    },
    params: { ...params },
    data: datas,
  }

  let statusCode = 200 // Default status code

  try {
    const res = await axios.request(config)
    statusCode = res.status
    return res.data
  } catch (err) {
    const errorAxios = err as AxiosError
    if (errorAxios.response) {
      const status = errorAxios.response.status
      switch (status) {
        case 400:
          statusCode = status
          return errorAxios.response.data
        case 401:
          statusCode = status
          return errorAxios.response.data
        case 404:
          statusCode = status
          return errorAxios.response.data
        case 500:
          statusCode = status
          return errorAxios.response.data
        default:
          statusCode = status
          return errorAxios.response.data
      }
    } else if (errorAxios.request) {
      throw new Error('No response from server - Check network connection.')
    } else {
      throw new Error(`Request setup failed - Check configuration, ${errorAxios.message}`)
    }
  }
}
