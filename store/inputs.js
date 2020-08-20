export const state = () => ({
    hs_code: "",
    pntl_weight: 50,
    ease_weight: 50,
    risk_weight: 50,
    pntl_weights: [25, 25, 25, 25],
    ease_weights: [33, 33, 34],
    econ_weights: [33, 33, 34],
    polt_weights: [25, 25, 25, 25],
    modified: true
})

export const mutations = {
    hs_code (state, data) {
        state.hs_code = data
        state.modified = true
    },
    pntl_weight (state, data) {
        state.pntl_weight = data
        state.modified = true
    },
    ease_weight (state, data) {
        state.ease_weight = data
        state.modified = true
    },
    risk_weight (state, data) {
        state.risk_weight = data
        state.modified = true
    },
    pntl_weights (state, data) {
        state.pntl_weights = data
        state.modified = true
    },
    ease_weights (state, data) {
        state.ease_weights = data
        state.modified = true
    },
    econ_weights (state, data) {
        state.econ_weights = data
        state.modified = true
    },
    polt_weights (state, data) {
        state.polt_weights = data
        state.modified = true
    }
}