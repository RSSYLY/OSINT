import { defineStore } from 'pinia'

export const useMainStore = defineStore('myStore', {
    state: () => ({
        pageInfo: {
            title: "OSINT",
            drawer:{
                items:[
                    {
                        title:'认证',
                        items:[
                            {
                                title:'登录',
                                link:'/login'
                            }
                        ]
                    }
                ]
            }
        }
    })
})
