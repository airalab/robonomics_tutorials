<template>
  <div>
    <h1 class="text-xs-center">Trade AIRA</h1>
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
                      Order
                    </v-btn>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>

      <v-layout justify-center row wrap v-if="liability">
        <v-flex xs12 md10 lg6>
          <v-card>
            <v-card-title primary-title>
              <div>
                <h3 class="headline mb-0">Result</h3>
              </div>
            </v-card-title>
            <v-card-text>
              <Liability :liability="liability" />
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>

      <v-layout justify-center row wrap v-if="demand !== null">
        <v-flex xs12 md10 lg6>
          <v-card>
            <v-card-title primary-title>
              <div>
                <h3 class="headline mb-0">Demand</h3>
              </div>
            </v-card-title>
            <v-card-text>
              <p class="t-break">
                <b>account: </b>{{ demand.account }}<br/>
                <b>model: </b>{{ demand.model }}<br/>
                <b>objective: </b>{{ demand.objective }}<br/>
                <b>token: </b>{{ demand.token }}<br/>
                <b>cost: </b>{{ demand.cost }}<br/>
                <b>deadline: </b>{{ demand.deadline }}
              </p>
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
import Liability from './Liability'
import * as config from '../config'

let robonomics

export default {
  name: 'trade',
  components: {
    Liability
  },
  data () {
    return {
      robonomicsStatus: false,
      token: null,
      loadingOrder: false,
      model: config.MODEL_TRADE,
      lighthouse: {
        name: '',
        address: ''
      },
      liability: null,
      demand: null
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
            if (msg.account === robonomics.account) {
              this.demand = msg
            }
          })
          robonomics.getResult((msg) => {
            console.log('result unverified', msg)
            if (this.liability !== null && msg.liability === this.liability.address) {
              this.setResult(msg.result, false)
            }
          })
          this.robonomicsStatus = true
        })
      })
  },
  methods: {
    setResult (result, check = true) {
      this.liability = {
        ...this.liability,
        result,
        check
      }
    },
    newLiability (liability) {
      console.log('liability demand', liability.address)
      return liability.getInfo()
        .then((info) => {
          this.liability = {
            address: liability.address,
            worker: liability.worker,
            ...info
          }
          liability.watchResult((result) => {
            console.log('result', result)
            this.setResult(result, true)
          })
          return true
        })
        .catch((e) => {
          console.log(e)
          setTimeout(() => {
            this.newLiability(liability)
          }, 2000)
        })
    },
    order () {
      this.demand = null
      this.liability = null
      this.loadingOrder = true
      web3.eth.getBlock('latest', (e, r) => {
        const demand = {
          objective: config.OBJECTIVE_TRADE,
          token: this.token.address,
          cost: config.PRICE,
          lighthouse: robonomics.lighthouse.address,
          validator: '0x0000000000000000000000000000000000000000',
          validatorFee: 0,
          deadline: r.number + 1000
        }
        robonomics.postDemand(this.model, demand)
          .then((liability) => this.newLiability(liability))
          .then(() => {
            this.loadingOrder = false
          })
          .catch((e) => {
            this.loadingOrder = false
          })
      })
    }
  }
}
</script>
