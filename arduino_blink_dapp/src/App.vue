<template>
  <div id="app">
    <v-app id="inspire">
      <header role="banner">
        <div class="secw-narrow">
          <div id="header-logo"><a href="/"><img class="img-block" alt="" src="static/assets/i/logo.svg"/></a></div>
        </div>
      </header>
      <v-content>
        <v-container fluid grid-list-md>
          <v-layout row wrap>
            <v-flex md12>
              <web3-check :networks="[network]">
                <router-view />
              </web3-check>
            </v-flex>
          </v-layout>
        </v-container>
      </v-content>
    </v-app>
  </div>
</template>

<script>
import * as config from './config'

export default {
  name: 'App',
  data () {
    return {
      network: config.NETWORK
    }
  }
}
</script>

<style>
  body {
    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    font-size: 14px;
    line-height: 1.42857143;
    color: #333;
    background-color: #f2f2f2;
  }
  .application.theme--light {
    background: #f2f2f2;
    color: rgba(0,0,0,.87);
  }
  #header-logo .img-block {
    max-width: 400px;
  }
  .img-block {
    display: block;
    max-width: 100%;
    margin-left: auto;
    margin-right: auto;
  }
  .secw-narrow {
    max-width: 680px;
    padding-left: 20px;
    padding-right: 20px;
    margin: 0 auto;
  }
  header[role=banner] {
    padding-top: 20px;
    padding-bottom: 40px;
  }
  .application .theme--light.card, .theme--light .card {
    border: 1px solid #707070;
    border-radius: 0;
    box-shadow: none;
  }
</style>
