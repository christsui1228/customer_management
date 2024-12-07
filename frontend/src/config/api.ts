// API配置
export const API_BASE_URL = 'http://localhost:8000/api/v1'  // 后端服务地址

export const API_ENDPOINTS = {
    CUSTOMERS: {
        LIST: '/customers/',        // 集合资源，使用尾部斜杠
        CREATE: '/customers/',      // 集合资源，使用尾部斜杠
        UPDATE: (id: string) => `/customers/${id}`,   // 单个资源，不使用尾部斜杠
        UPDATE_BY_ID: (id: number) => `/customers/id/${id}`,   // 通过ID更新
        DELETE: (id: string) => `/customers/${id}`,   // 单个资源，不使用尾部斜杠
    }
}
