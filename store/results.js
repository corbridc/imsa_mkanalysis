export const state = () => ({
    product_title: "",
    data_exists: false,
    raw: ""
})

export const mutations = {
    product_title (state, data) {
        state.product_title = data
    },
    data_exists (state, data) {
        state.data_exists = data
    },
    custom_exists (state, data) {
        state.custom_exists = data
    },
    raw (state, data) {
        state.raw = data
    }
}