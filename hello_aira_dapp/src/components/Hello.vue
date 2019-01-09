<template>
  <div>
    <h1 class="text-xs-center">Hello AIRA</h1>
    <v-container v-if="!robonomicsStatus" fluid fill-height class="px-3">
      <v-layout
        justify-center
        align-center
      >
        <v-flex text-xs-center>
          <h1>Load robonomics</h1>
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-flex>
      </v-layout>
    </v-container>

    <v-container v-if="robonomicsStatus" grid-list-md class="px-3">
      <v-layout justify-center row wrap>
        <v-flex xs12 md10 lg6>
          <v-card>
            <v-card-text>
              <v-container grid-list-md class="px-3">
                <v-layout row wrap>
                  <v-flex md12 class="text-xs-center">
                    Lighthouse: <a :href="`https://etherscan.io/address/${lighthouse.address}`" target="blank">{{ lighthouse.name }}</a>
                    <v-btn
                      :loading="loadingOrder"
                      :disabled="loadingOrder"
                      color="primary"
                      @click.native="order"
                    >
                      Say hello to Aira
                    </v-btn>
                    <v-alert
                      v-if="msg"
                      :value="true"
                      type="success"
                    >
                      {{msg}}
                    </v-alert>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import { Token } from 'robonomics-js'
import getRobonomics from '../utils/robonomics'
import * as config from '../config'

let robonomics

export default {
  name: 'hello',
  data () {
    return {
      robonomicsStatus: false,
      token: null,
      loadingOrder: false,
      msg: '',
      model: config.MODEL_HELLO,
      lighthouse: {
        name: '',
        address: ''
      }
    }
  },
  created () {
    getRobonomics()
      .then((r) => {
        robonomics = r
        robonomics.ready().then(() => {
          if (config.TOKEN) {
            this.token = new Token(robonomics.web3, config.TOKEN)
          } else {
            this.token = robonomics.xrt
          }
          this.lighthouse.name = robonomics.lighthouse.name
          this.lighthouse.address = robonomics.lighthouse.address
          robonomics.getDemand(this.model, (msg) => {
            console.log('demand', msg)
          })
          this.robonomicsStatus = true
        })
      })
  },
  methods: {
    order () {
      this.msg = ''
      this.loadingOrder = true
      web3.eth.getBlock('latest', (e, r) => {
        const demand = {
          objective: config.OBJECTIVE_HELLO,
          token: this.token.address,
          cost: config.PRICE,
          lighthouse: robonomics.lighthouse.address,
          validator: '0x0000000000000000000000000000000000000000',
          validatorFee: 0,
          deadline: r.number + 1000
        }
        robonomics.post('demand', this.model, demand)
          .then(() => {
            this.loadingOrder = false
            this.msg = 'Message sent, look in Aira console now'
          })
          .catch((e) => {
            this.loadingOrder = false
          })
      })
    }
  }
}
</script>
