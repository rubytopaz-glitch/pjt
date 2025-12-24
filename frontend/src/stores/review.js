import { defineStore } from 'pinia'

export const useReviewStore = defineStore('review', {
  state: () => ({
    reloadKey: 0,
  }),
  actions: {
    bumpReload() {
      this.reloadKey += 1
    },
  },
})
