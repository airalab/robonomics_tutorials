<template>
  <div>
    <h1 class="text-md-center">Hello AIRA</h1>
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
        <v-flex xs12 md6>
          <v-card>
            <v-card-text>
              <v-container grid-list-md class="px-3">
                <v-layout row wrap>
                  <v-flex md12 class="text-md-center">
                    Lighthouse: <a :href="`https://etherscan.io/address/${lighthouse.address}`" target="blank">{{ lighthouse.name }}</a>
                    <v-btn
                      v-if="approveTrade.value >= price.value"
                      :loading="loadingOrder"
                      :disabled="loadingOrder || balance.value < price.value"
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
import { formatDecimals, watchTx } from '../utils/utils'
import * as config from '../config'

let robonomics

export default {
  name: 'hello',
  data () {
    return {
      token: null,
      decimals: 9,
      symbol: 'XRT',
      robonomicsStatus: false,
      loadingApprove: false,
      loadingOrder: false,
      msg: '',
      price: {
        value: config.PRICE,
        valueStr: `${formatDecimals(config.PRICE, 9)} XRT`
      },
      balance: {
        address: '',
        value: 0,
        valueStr: '0 XRT'
      },
      approveTrade: {
        value: 0,
        valueStr: '0 XRT'
      },
      model: config.MODEL_HELLO,
      account: '',
      lighthouse: {
        name: '',
        address: ''
      },
      liability: null,
      demands: [],
      offers: []
    }
  },
  created () {
    getRobonomics()
      .then((r) => {
        robonomics = r
        robonomics.ready().then(() => {
          let ready
          if (config.TOKEN) {
            this.token = new Token(robonomics.web3, config.TOKEN)
            ready = this.token.call('decimals')
              .then((decimals) => {
                this.decimals = decimals
                return this.token.call('symbol')
              })
              .then((symbol) => {
                this.symbol = symbol
                this.price.valueStr = `${formatDecimals(this.price.value, this.decimals)} ${this.symbol}`
                return this.fetchData()
              })
          } else {
            this.token = robonomics.xrt
            ready = this.fetchData()
          }
          ready.then(() => {
            this.robonomicsStatus = true
            this.balance.address = this.token.address
            this.lighthouse.name = robonomics.lighthouse.name
            this.lighthouse.address = robonomics.lighthouse.address
            this.account = robonomics.account

            robonomics.getDemand(this.model, (msg) => {
              this.demands = [{ ...msg }, ...this.demands.slice(0, 10)]
            })
            robonomics.getOffer(this.model, (msg) => {
              this.offers = [{ ...msg }, ...this.offers.slice(0, 10)]
            })
            robonomics.getResult((msg) => {
              console.log('result unverified', msg)
              if (this.liability !== null && msg.liability === this.liability.address) {
                this.setResult(msg.result, false)
              }
            })
          })
        })
      })
  },
  methods: {
    fetchData () {
      return this.token.call('balanceOf', [robonomics.account])
        .then((balanceOf) => {
          this.balance.value = balanceOf
          this.balance.valueStr = `${formatDecimals(balanceOf, this.decimals)} ${this.symbol}`
          if (balanceOf > 0) {
            return this.token.call('allowance', [robonomics.account, robonomics.factory.address])
          }
          return false
        })
        .then((allowance) => {
          if (allowance) {
            this.approveTrade.value = allowance
            this.approveTrade.valueStr = `${formatDecimals(allowance, this.decimals)} ${this.symbol}`
          }
        })
    },
    sendApproveTrade () {
      this.loadingApprove = true
      return this.token.send('approve', [robonomics.factory.address, (this.price.value * 100)], { from: robonomics.account })
        .then((r) => watchTx(r))
        .then(() => {
          this.loadingApprove = false
          return this.fetchData()
        })
        .catch(() => {
          this.loadingApprove = false
        })
    },
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
      this.msg = ''
      this.liability = null
      this.loadingOrder = true
      web3.eth.getBlock('latest', (e, r) => {
        const demand = {
          objective: config.OBJECTIVE,
          token: this.token.address,
          cost: this.price.value,
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
