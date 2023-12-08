import { defineStore } from 'pinia'

export const useMainStore = defineStore('myStore', {
    state: () => ({
        pageInfo: {
            title: "OSINT",
            drawer:{
                items:[
                    {
                        title:'错误，请检查前端配置',
                    }
                ]
            }
        },
        userInfo: {
            id: 0,
            username: "",
            email: "",
            phone: "",
            token: "",
            is_superuser: false,
            is_staff: false,
            is_active: false,
        },
        userStatus: {
            isLogin: false
        },
    })
})
