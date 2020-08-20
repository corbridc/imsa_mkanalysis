<template>
  <v-app>
    <v-card 
      class="ma-3"
      max-width="1024"
      elevation="3"
    >
      <v-tooltip right>
        <template v-slot:activator="{ on }">
          <v-icon color="grey" class="pa-5 float-right" dark v-on="on">mdi-information</v-icon>
        </template>
        <span>Tooltip</span>
      </v-tooltip>
      <v-card-title class="headline">Indicator Weights</v-card-title>
      <v-row class="px-5">
        <v-col class="pt-0">
          <v-text-field
            v-model="weights[0]"
            label="Short-term Political Risk %"
            type="number"
            @change="sumWeights"
          ></v-text-field>
        </v-col>
        <v-col class="pt-0">
          <v-text-field
            v-model="weights[1]"
            label="Long-term Political Risk %"
            type="number"
            @change="sumWeights"
          ></v-text-field>  
        </v-col>
        <v-col class="pt-0">
          <v-text-field
            v-model="weights[2]"
            label="OEAP Political Risk %"
            type="number"
            @change="sumWeights"
          ></v-text-field>
        </v-col>
        <v-col class="pt-0">
          <v-text-field
            v-model="weights[3]"
            label="Political Violence Risk %"
            type="number"
            @change="sumWeights"
          ></v-text-field>
        </v-col>
        <v-col class="pt-3 text-right">
          Total: 
          <v-chip 
            :color="weight_color" 
            text-color="white"
          >{{ weight_total }}%</v-chip>
        </v-col>      </v-row>
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
        <span>
          <strong>Average Import Value</strong>: The average value of goods imported for your HS code for the past 3 years.<br />
          <strong>Import Growth</strong>: The average percent change of imported goods for your HS code for the past 3 years.<br />
          <strong>Population</strong>: I won't insult your intelligence explaining this one.<br />
          <strong>GDP Per Capita</strong>: I won't insult your intelligence explaining this one.<br />
        </span>
      </v-tooltip>
      <v-card-title class="headline">Data</v-card-title>
      <v-data-table
        :headers="headers"
        :items="data"
        elevation="0"
        hide-default-footer
        :items-per-page="50"
        flat
      ></v-data-table>
    </v-card>
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
    </v-speed-dial>
  </v-app>  
</template>

<script>
export default {
  middleware: 'default',
  async fetch ({ store, params }) {
    await store.commit('page_title', 'Data: Political Risk')
  },
  methods: {
    sumWeights() {
      this.weight_total = this.weights.reduce(function(a, b){
        return Number(a) + Number(b);
      }, 0);
      if (this.weight_total === 100) {
        this.weight_color = "grey"
        this.save()
      }
      else {
        this.weight_color = "red"
      }
    },
    async save() {
      if (this.weight_total === 100) {
        await this.$store.commit('inputs/polt_weights', [...this.weights])
      }
    },
    reset() {
      this.weights = [33, 33, 34]
      this.weight_color = "grey"
    },
    next() {
      this.$router.replace({ path: '/results' })
    }
  },
  data () {
    return {
      weights: [...this.$store.state.inputs.polt_weights],
      weight_total: 100,
      weight_color: "grey",
      fab: false,
      headers: [
        {
          text: 'Country',
          align: 'start',
          sortable: true,
          value: 'country',
        },
        { text: 'Total Imported Trade Value', value: 'tradevalue' },
        { text: '% Change from Previous Year', value: 'change' },
      ],
      data: this.$store.state.results.raw
    }
  },
}
</script>