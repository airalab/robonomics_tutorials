<template>
  <v-app id="inspire">
    <header role="banner">
      <div class="secw-narrow">
        <div id="header-logo"><img class="img-block" alt="" src="static/assets/i/logo.svg"/></div>
      </div>
    </header>
    <v-content>
      <v-container fluid grid-list-md>
        <v-layout row wrap>
          <v-flex md12>
            <h1>{{ name }}</h1>
            <Order />
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Order from './Order'

export default {
  name: 'Page',
  components: {
    Order
  }
}
</script>
