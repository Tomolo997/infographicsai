import { defineStore } from 'pinia'

export const useBillingStore = defineStore('billing', {
  state: () => ({
    plans: [],
    currentSubscription: null,
    creditBalance: 0,
    creditTransactions: [],
    invoices: [],
    loading: false
  }),

  getters: {
    hasActiveSubscription: (state) => state.currentSubscription && state.currentSubscription.status === 'active',
    currentPlan: (state) => state.currentSubscription?.plan
  },

  actions: {
    async fetchPlans() {
      try {
        const { $api } = useNuxtApp()
        this.plans = await $api('/billing/plans/')
        return this.plans
      } catch (error) {
        console.error('Error fetching plans:', error)
        throw error
      }
    },

    async fetchCurrentSubscription() {
      try {
        const { $api } = useNuxtApp()
        const response = await $api('/billing/subscriptions/current/')
        this.currentSubscription = response.subscription
        return this.currentSubscription
      } catch (error) {
        console.error('Error fetching subscription:', error)
        return null
      }
    },

    async subscribeToPlan(planId) {
      this.loading = true
      try {
        const { $api } = useNuxtApp()
        const response = await $api('/billing/subscriptions/subscribe/', {
          method: 'POST',
          body: { plan_id: planId }
        })
        return response
      } catch (error) {
        throw error
      } finally {
        this.loading = false
      }
    },

    async cancelSubscription() {
      this.loading = true
      try {
        const { $api } = useNuxtApp()
        const response = await $api('/billing/subscriptions/cancel/', {
          method: 'POST'
        })
        this.currentSubscription = response
        return response
      } catch (error) {
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchCreditBalance() {
      try {
        const { $api } = useNuxtApp()
        const response = await $api('/billing/credits/balance/')
        this.creditBalance = response.credits
        return response
      } catch (error) {
        console.error('Error fetching credit balance:', error)
        return { credits: 0 }
      }
    },

    async fetchCreditTransactions() {
      try {
        const { $api } = useNuxtApp()
        this.creditTransactions = await $api('/billing/credits/transactions/')
        return this.creditTransactions
      } catch (error) {
        console.error('Error fetching credit transactions:', error)
        return []
      }
    },

    async purchaseCredits(creditAmount) {
      this.loading = true
      try {
        const { $api } = useNuxtApp()
        const response = await $api('/billing/credits/purchase/', {
          method: 'POST',
          body: { credit_amount: creditAmount }
        })
        return response
      } catch (error) {
        throw error
      } finally {
        this.loading = false
      }
    },

    async useCredits(amount, description) {
      try {
        if (this.creditBalance >= amount) {
          this.creditBalance -= amount
          
          // Add transaction to local state
          this.creditTransactions.unshift({
            id: Date.now(),
            transaction_type: 'usage',
            amount: -amount,
            description: description,
            created_at: new Date().toISOString()
          })
          
          return true
        }
        return false
      } catch (error) {
        console.error('Error using credits:', error)
        return false
      }
    },

    async initializeBilling() {
      await Promise.all([
        this.fetchPlans(),
        this.fetchCurrentSubscription(),
        this.fetchCreditBalance()
      ])
    }
  }
})