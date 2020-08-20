<template>
  <v-app>
    <v-card 
      class="ma-3"
      max-width="1024"
      elevation="3"
      border="left"
    >
      <v-tooltip right>
        <template v-slot:activator="{ on }">
          <v-icon color="grey" class="pa-5 float-right" dark v-on="on">mdi-information</v-icon>
        </template>
        <span>Tooltip</span>
      </v-tooltip>
      <v-card-title class="headline">Product Code</v-card-title>
      <v-form ref="form" v-on:submit.prevent="fetch">
        <v-row class="px-5">
          <v-col cols="3">
            <v-text-field
              v-model="hs_code"
              label="HS Code"
              type="text"
              clearable
              :rules="[rules.hs_code]"
            ></v-text-field>
          </v-col>
          <v-col class="mt-4">
            =
            <v-chip class="ml-5">{{ product_title }}</v-chip>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
    <v-card 
      max-width="1024"
      elevation="3"
      class="ma-3"
    >
      <v-tooltip right>
        <template v-slot:activator="{ on }">
          <v-icon color="grey" class="pa-5 float-right" dark v-on="on">mdi-information</v-icon>
        </template>
        <span>Tooltip</span>
      </v-tooltip>
      <v-card-title class="headline">Category Weights</v-card-title>
        <v-row class="mx-5 mt-5">
          <v-col class="pa-0 caption">Market Potential</v-col>
          <v-col class="pa-0 caption text-right">Ease of Business</v-col>
        </v-row>
        <v-row class="mx-5">
          <v-slider 
            v-model="pntl_slider"
            @change="save"
          >
            <template v-slot:prepend>
              <v-text-field
                :value="pntl_slider"
                class="mt-0 pt-0"
                single-line
                type="number"
                style="width: 40px"
                disabled
                dense
              ></v-text-field>
            </template>
            <template v-slot:append>
              <v-text-field
                :value="100 - pntl_slider"
                class="mt-0 pt-0"
                single-line
                type="number"
                style="width: 40px"
                disabled
                dense
              ></v-text-field>
            </template>
          </v-slider>
        </v-row>
        <v-row class="mx-5 mt-5">
          <v-col class="pa-0 caption">Ease of Business</v-col>
          <v-col class="pa-0 caption text-right">Economic/Political Risk</v-col>
        </v-row>
        <v-row class="mx-5">
          <v-slider 
            v-model="ease_slider"
            @change="save"
          >
            <template v-slot:prepend>
              <v-text-field
                :value="ease_slider"
                class="mt-0 pt-0"
                single-line
                type="number"
                style="width: 40px"
                disabled
                dense
              ></v-text-field>
            </template>
            <template v-slot:append>
              <v-text-field
                :value="100 - ease_slider"
                class="mt-0 pt-0"
                single-line
                type="number"
                style="width: 40px"
                disabled
                dense
              ></v-text-field>
            </template>
          </v-slider>
        </v-row>
        <v-row class="mx-5 mt-5">
          <v-col class="pa-0 caption">Economic/Political Risk</v-col>
          <v-col class="pa-0 caption text-right">Market Potential</v-col>
        </v-row>
        <v-row class="mx-5">
          <v-slider 
            v-model="risk_slider"
            @change="save"
          >
            <template v-slot:prepend>
              <v-text-field
                :value="risk_slider"
                class="mt-0 pt-0"
                single-line
                type="number"
                style="width: 40px"
                disabled
                dense
              ></v-text-field>
            </template>
            <template v-slot:append>
              <v-text-field
                :value="100 - risk_slider"
                class="mt-0 pt-0"
                single-line
                type="number"
                style="width: 40px"
                disabled
                dense
              ></v-text-field>
            </template>
          </v-slider>
        </v-row>
    </v-card>
    <v-snackbar
      v-model="error"
      bottom
      right
      dark
      multi-line
      :timeout="0"
    >Error! {{ this.error_msg }} Please try again.
      <v-btn
        class="ml-2"
        dark
        text
        @click="error = false"
      >Close</v-btn>
    </v-snackbar>
    <v-speed-dial
      v-model="fab"
      right
      bottom
      fixed
      direction="top"
      transition=slide-y-reverse-transition
    >
      <template v-slot:activator>
        <v-btn
          v-model="fab"
          color="primary"
          dark
          fab
        >
          <v-icon v-if="fab">mdi-close</v-icon>
          <v-icon v-else>mdi-chevron-up</v-icon>
        </v-btn>
      </template>
      <v-btn
        fab
        dark
        small
        color="accent"
        v-show="$store.state.results.data_exists"
        v-on:click="next"
      >
        <v-icon>mdi-arrow-right-thick</v-icon>
      </v-btn>
      <v-btn
        fab
        dark
        small
        color="grey"
        v-on:click="reset"
      >
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
      <v-btn
        fab
        dark
        small
        color="primary"
        v-on:click="fetch"
      >
        <v-icon>mdi-content-save-outline</v-icon>
      </v-btn>
    </v-speed-dial>
    <v-overlay
      absolute
      :value="loading"
      class="text-center black--text"
      opacity="0.75"
      color="white"
    >
      <v-progress-circular 
        indeterminate 
        size="64"
        color="primary">
      </v-progress-circular>
      <br />
      Loading product information.<br />
      This may take several minutes.
    </v-overlay>
  </v-app>
</template>

<script>
export default {
  async fetch ({ store, params }) {
    await store.commit('page_title', 'Product Information')
  },
  methods: {
    async fetch() {
      if (this.$refs.form.validate()) {
        if (this.hs_code !== this.$store.state.inputs.hs_code) {
          this.loading = true
          var resp = await this.$axios.$post('https://api.internationalhub.org/marketpntl/fetch', {"hs": this.hs_code})
          if (resp.message == "Success") {
            await this.$store.commit('results/raw', resp.result)
            await this.$store.commit('results/product_title', resp.message)
            await this.$store.commit('results/data_exists', true)
            await this.$store.commit('inputs/hs_code', this.hs_code)
          }
          else {
            this.error = true
            this.error_msg = resp.result
          }
        }
        this.save()
      }
    },
    async save() {
      await this.$store.commit('inputs/pntl_weight', this.pntl_slider)
      await this.$store.commit('inputs/ease_weight', this.ease_slider)
      await this.$store.commit('inputs/risk_weight', this.risk_slider)
      this.loading = false
    },
    reset() {
      this.$refs.form.resetValidation()
      this.hs_code = ""
      this.pntl_slider = 50
      this.ease_slider = 50
      this.risk_slider = 50
    },
    next() {
      this.$router.replace({ path: '/data/market_potential' })
    }
  },
  computed: {
    product_title() {
      if (this.$store.state.results.product_title == "")
        return "None (no product code entered)"
      else
        return this.$store.state.results.product_title
    }
  },
  data() {
    return {
      hs_code: this.$store.state.inputs.hs_code,
      pntl_slider: this.$store.state.inputs.pntl_weight,
      ease_slider: this.$store.state.inputs.ease_weight,
      risk_slider: this.$store.state.inputs.risk_weight,
      completed: this.$store.state.results.basic_exists,
      loading: false,
      fab: false,
      error: false,
      error_msg: "",
      rules: {
        hs_code: value => {
          const pattern = /^\d{6}$/
          return pattern.test(value) || 'Invalid HS code.'
        }
      }
    }
  }
}
</script>
