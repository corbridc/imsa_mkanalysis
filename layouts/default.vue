<template>
  <v-app>
    <v-navigation-drawer
      color="primary"
      :permanent="nav_visible"
      fixed
      app
    >
      <v-list-item>
        <v-list-item-content>
          <v-img 
            src="/logo-ihub.png" 
            max-height="75"
            max-width="256"
            position="top center"
            class="my-4"
            contain
          ></v-img>
          <v-list-item-subtitle class="white--text font-weight-medium text-center mb-3">Market Analysis Tool</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list rounded>
        <v-list-item to="/data/product_info" color="white">
          <v-list-item-icon>
            <v-icon color="white">mdi-barcode-scan</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="white--text" >Product Info</v-list-item-title>
            <v-list-item-subtitle v-show="$store.state.results.data_exists" class="white--text overline" >(HS Code: {{ $store.state.inputs.hs_code }})</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mb-2"></v-divider>
        <v-list-group
          color="white"
          prepend-icon="mdi-database"
          :value="true"
          to="/data/hs"
          disabled
        >
          <template v-slot:activator color="white">
            <v-list-item-title class="white--text">Data</v-list-item-title>
          </template>
          <v-list-item to="/data/market_potential" :disabled="!$store.state.results.data_exists">
            <v-list-item-icon>
              <v-icon color="white"></v-icon>
            </v-list-item-icon>
            <v-list-item-title class="font-weight-light white--text" >Market Potential</v-list-item-title>
          </v-list-item>
          <v-list-item to="/data/business_ease" :disabled="!$store.state.results.data_exists">
            <v-list-item-icon>
              <v-icon color="white"></v-icon>
            </v-list-item-icon>
            <v-list-item-title class="font-weight-light white--text" >Ease of Business</v-list-item-title>
          </v-list-item>
          <v-list-item to="/data/economic_risk" :disabled="!$store.state.results.data_exists">
            <v-list-item-icon>
              <v-icon color="white"></v-icon>
            </v-list-item-icon>
            <v-list-item-title class="font-weight-light white--text" >Economic Risk</v-list-item-title>
          </v-list-item>
          <v-list-item to="/data/political_risk" :disabled="!$store.state.results.data_exists">
            <v-list-item-icon>
              <v-icon color="white"></v-icon>
            </v-list-item-icon>
            <v-list-item-title class="font-weight-light white--text" >Political Risk</v-list-item-title>
          </v-list-item>
        </v-list-group>
        <v-divider class="my-2"></v-divider>
        <v-list-item to="/results" color="white" :disabled="!$store.state.results.data_exists">
          <v-list-item-icon>
            <v-icon color="white">mdi-chart-bar</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="white--text" >Results</v-list-item-title>
        </v-list-item>   
        <v-divider class="mb-2"></v-divider>
        <v-list-item to="/" color="white">
          <v-list-item-icon>
            <v-icon color="white">mdi-help</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="white--text" >Instructions</v-list-item-title>
        </v-list-item>   
        <v-divider></v-divider>   
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      color="secondary"
      :flat="true"
      fixed
      app
    >
      <v-app-bar-nav-icon :disabled="!nav_changeable" @click.stop="nav_visible = !nav_visible" />
      <v-toolbar-title>{{ $store.state.page_title }}</v-toolbar-title>
      <v-spacer />
    </v-app-bar>

    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>

  </v-app>
</template>

<script>
export default {
  created() {
    window.addEventListener("load", this.adjustNavButton);
    window.addEventListener("resize", this.adjustNavButton);
  },
  destroyed() {
    window.removeEventListener("load", this.adjustNavButton);
    window.removeEventListener("resize", this.adjustNavButton);
  },
  methods: {
    adjustNavButton() {
      if (window.innerWidth >= 1265) {
        this.nav_changeable = false
      }
      else {
        this.nav_changeable = true
      }
    }
  },
  data() {
    return {
      nav_visible: false,
      nav_changeable: true,
      fixed: false
    }
  }
}
</script>