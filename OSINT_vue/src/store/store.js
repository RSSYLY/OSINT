import { defineStore } from 'pinia'

export const useMainStore = defineStore('myStore', {
    state: () => ({
        pageInfo: {
            title: "OSINT"
        }
    })
})
