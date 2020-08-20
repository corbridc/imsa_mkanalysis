<template>
  <v-app>
        <v-card flat>
          <v-card-text>
          
            <div class="text-center">
              <h1 class="display-1 black--text mb-4">Market Analysis Tool</h1>
              <p class="mb-4">
                This tool analyzes the potential for exporting and selling all types of products in foreign markets. Results are calculated using various quantitative data sources and advanced statistical analysis. It is intended for small/medium-sized businesses or educational groups.<br />
                Provided to you for free by BYU InternationalHub.
              </p>
              <small class="mb-4">
                Tip: For getting started quick, use the hovering button in the bottom-right corner of the page to navigate the pages and do your analysis.
              </small>
            </div>
            
            <v-card-title class="headline black--text">Background Information</v-card-title>
            <v-expansion-panels
              :accordion="accordion"
              :popout="popout"
              :inset="inset"
              :multiple="multiple"
              :focusable="focusable"
              :disabled="disabled"
              :readonly="readonly"
              :flat="flat"
              :hover="hover"
              :tile="tile"
            >

              <v-expansion-panel>
                <v-expansion-panel-header class="subtitle-1">Is this analysis right for my specific business?</v-expansion-panel-header>
                <v-expansion-panel-content class="mt-3">
                  The iHub Market Analysis Tool is very useful to small/medium businesses who sell a physical product. Many such companies have already used this system to aid in their market 
                  research efforts and have seen great success from expanding sales abroad.<br>
                  <br>
                  If you sell a service or a software, this analysis may still be useful to you if there are complimentary products that have a strong correlation with demand for 
                  your service/software. We rely heavily on import/export data to gauge demand. UN Comtrade, where we get this data, does not track international services or software sales. 
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header class="subtitle-1">What is an HS Code?</v-expansion-panel-header>
                <v-expansion-panel-content class="mt-3">
                  The HS (Harmonized System) Code is a numerical method to classify products for international trade. The first six digits of any code are standardized
                   across all countries. The HS is managed by the World Customs Organization. For example, the HS Code for fresh grapes is 080610. <br>
                  <br>
                  Keep in mind that only physical products have HS Codes. The HS does not track the flow of services or non-physical products, like software, 
                  across borders. Unfortunately, this analysis tool is not very useful for analyzing the markets for services or software products.
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header class="subtitle-1">How can I find the HS Code for my product?</v-expansion-panel-header>
                <v-expansion-panel-content class="mt-3">
                  HS Codes are found on <a target="_blank" href="https://uscensus.prod.3ceonline.com/#!#current-question-pos">this search engine</a> created by the US Census 
                  Bureau. Training videos are available on the site if you need assistance. (The HS Code is the first 6 digits of the Schedule B)<br>
                  <br>
                  Only physical products have HS Codes. The HS does not track the flow of services or software sales across borders. Unfortunately, this analysis tool is not 
                  very useful for analyzing foreign markets for services or software products.
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header class="subtitle-1">There is no HS Code for my product, now what?</v-expansion-panel-header>
                <v-expansion-panel-content class="mt-3">
                  All physical products have an HS Code, but sometimes the categories are very broad. The more broad the category, the weaker the analysis. However, the 
                  results we provide still give a starting point for your market research.<br>
                  <br>  
                  One option is to perform an analysis for the HS Code of a complimentary product. For example, if you sell a baby monitor for new parents, you may look at 
                  the HS Code for diapers or toys. If these HS Codes are specific to children's products, then they will give you a better indication of demand than 
                  the HS Code for monitors, which inculdes all kinds of monitors, like those for industrial uses.<br>   
                  <br>
                  Moving forward in your market research, we would encourage you to find other quantitative variables that may be helpful for targeting the right countries.
                   For example, if you are selling ski equipment you will want to look at factors like the number of ski resorts, ski competitions, and professional atheletes 
                   per country to help gauge demand.<br>
                  <br>
                  We have considered adding an option for users to add their on quanititative variables to this tool. If this is something you are interested in, please 
                  contact InternationalHub and let us know. 
                </v-expansion-panel-content>
              </v-expansion-panel>

            </v-expansion-panels>

            <v-card-title class="headline black--text">Using this Tool</v-card-title>
            <v-expansion-panels
              :accordion="accordion"
              :popout="popout"
              :inset="inset"
              :multiple="multiple"
              :focusable="focusable"
              :disabled="disabled"
              :readonly="readonly"
              :flat="flat"
              :hover="hover"
              :tile="tile"
            >

              <v-expansion-panel>
                <v-expansion-panel-header class="subtitle-1">Selecting Category Weights </v-expansion-panel-header>
                <v-expansion-panel-content class="mt-3">
                  To select a category weight, assess how much you value Market Potential, Ease of Doing Business, and Economic and Political Risk compaired to one another.
                  Then move the slider until the desired value is next to the category name. In the example below the user 
                  weighs Market Potential at 70 versus Ease of Doing Business at 30. In other words, Market Potential is considerably more important than Ease of 
                  Doing Business to that users business. <br>

                  <v-img width="1000" height="200" src="category weight.PNG" aspect-ratio="1.7" contain></v-img><br>
                  
                  This analysis divides global trade and market data into three main categories; Market Potential, Ease of Doing Business, and Economic/Political Risk. 
                  Every business is different and will have different preferences and risk tolerances.<br>
                  <br>
                  Businesses hoping to only export will usually have a much higher risk tolerance, since the only risk they face is a loss of inventory.<br>
                  <br>  
                  Businesses looking to send employees abroad, hire local talent, invest in capital, and other in-country investments are going to be much more sensitive to
                   political and economic risks.<br>
                  <br>
                  Weigh your valuation of each category against one another, and we will take care of the rest. To do so, move the slider so that the This analysis uses a 
                  parametric weights analysis. 
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header class="subtitle-1">Selecting Indicator Weights </v-expansion-panel-header>
                <v-expansion-panel-content class="mt-3">
                  To select indicator weights, assess how much you value the given indicators in comparison to one another. Then input values for the indicator weights
                  that reflect those preferences (Note that these weights must add to exactly 100%).<br>
                  <br>
                  As an example, many companies sell products to consumers (B2C). Because their customers are everyday people - they want their international business investments
                   to go toward countries with the biggest populations. The image below shows an example of how a company like this might weigh their Market Potential Indicators. 

                  <v-img width="1000" height="200" src="indicator weight.PNG" aspect-ratio="1.7" contain></v-img><br>

                  Within each category are a set of indicators. Each indicator is given a percent weight, and the weights of all indicators within a category need to add to 100%. 
                  The heigher the weight, the more you value the given indicator.<br>
                  <br>
                  Recrence the "i" icon on each page for a description of the indicators. If you are unsure of what to set these weights to, leave them at their default values. 
                </v-expansion-panel-content>
              </v-expansion-panel>

            </v-expansion-panels>

            <v-card-title class="headline black--text">Acknowledgements</v-card-title>
            <p class="text-left mx-3">
             Thank you to the World Trade Center Utah, who originaly developed the methodology used in this tool, and to the BYU Global Management Center who helped fund its 
             development.   
            </p>

          <v-row>
            <v-spacer></v-spacer>
            <v-img width="50" height="70" src="byu-logo.png" aspect-ratio="1.7" contain></v-img>
            <v-img width="60" height="50" src="wtc-logo.png" aspect-ratio="1.7" contain></v-img>
            <v-spacer></v-spacer>
          </v-row>

          <div class=" text-center mb-4">
            <small>&copy; InternationalHub {{ new Date().getFullYear() }}</small>
          </div>

          </v-card-text>
        </v-card>

  </v-app>
</template>




<script>
  export default {
    data: () => ({
      length: 3,
      window: 0,
      showArrows: false,
      vertical: false,
      reverse: false,
      autorun: false,
      accordion: true,
      popout: false,
      inset: false,
      multiple: true,
      disabled: false,
      readonly: false,
      focusable: false,
      flat: false,
      hover: true,
      tile: false,
    }),

    created () {
      setInterval(() => {
        if (!this.autorun) return
        if (++this.window >= this.length) this.window = 0
      }, 1000)
    },
  }



</script>