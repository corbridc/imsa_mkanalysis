export default function ({ store, redirect }) {
    if (!store.state.results.data_exists) {
      return redirect('/')
    }
  }