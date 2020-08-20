export const state = () => ({
    page_title: null,
})
export const mutations = {
    page_title(state, title) {
        state.page_title = title
    }
}
export const getters = {
    page_title(state) {
        return state.page_title
    }
}