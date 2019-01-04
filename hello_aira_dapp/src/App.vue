<template>
  <div id="app">
    <v-app id="inspire">
      <v-content>
        <v-container grid-list-md style="margin: 18px auto 15px;">
          <v-layout justify-center row wrap>
            <v-flex sm12 md10 lg6>
              <v-layout row wrap>
                <v-flex xs12 sm6 class="text-xs-center text-sm-left">
                  <router-link to="/">
                    <img alt="" src="static/assets/i/logo.svg" style="height: 45px;"/>
                  </router-link>
                </v-flex>
                <v-flex xs12 sm6 class="text-xs-center text-sm-right">
                  <v-btn to="/" outline>Hello</v-btn>
                  <v-btn to="/trade" outline>Trade</v-btn>
                </v-flex>
              </v-layout>
            </v-flex>
          </v-layout>
        </v-container>
        <web3-check :networks="network" @changeNetwork="onChangeNetwork" @changeAccount="onChangeAccount">
          <router-view />
        </web3-check>
      </v-content>
    </v-app>
  </div>
</template>

<script>
import * as config from './config'

const network = Object.keys(config.ROBONOMICS).map((item) => {
  return Number(item)
})

export default {
  name: 'App',
  data () {
    return {
      network: network
    }
  },
  methods: {
    onChangeNetwork (data) {
      if (data.check === true) {
        window.location.reload(false)
      }
    },
    onChangeAccount () {
      window.location.reload(false)
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
  .application .theme--light.v-card, .theme--light .v-card {
    border: 1px solid #707070;
    border-radius: 0;
    box-shadow: none;
  }
</style>
