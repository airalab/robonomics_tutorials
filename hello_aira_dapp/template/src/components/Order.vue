<template>
  <div>
    <v-container v-if="!robonomicsStatus" fluid fill-height>
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

    <v-container v-if="robonomicsStatus" grid-list-md>
      <v-layout row wrap>
        <v-flex md12>
          <v-card>
            <v-card-text>
              <v-container grid-list-md>
                <v-layout row wrap>
                  <v-flex md12>
                    Маяк: <a :href="`https://etherscan.io/address/${lighthouse.address}`" target="blank">\{{ lighthouse.name }}</a>
                  </v-flex>
                </v-layout>
              </v-container>
              <v-divider />

              <v-container grid-list-md>
                <v-layout row wrap>
                  <v-flex md12>
                    <div>
                      Стоимость: \{{ price.valueStr }} |
                      Баланс: <a :href="`https://etherscan.io/token/${balance.address}?a=${account}`" target="blank">\{{ balance.valueStr }}</a> |
                      Одобренно: \{{ approveTrade.valueStr }}
                    </div>
                  </v-flex>
                </v-layout>
              </v-container>

              <v-btn
                v-if="approveTrade.value >= price.value"
                :loading="loadingOrder"
                :disabled="loadingOrder || balance.value < price.value"
                color="primary"
                @click.native="order"
              >
                Заказать
              </v-btn>

            </v-card-text>
          </v-card>
        </v-flex>

        <v-flex md12>
          <v-card v-if="liability">
            <v-card-title primary-title>
              <div>
                <h3 class="headline mb-0">Результат</h3>
              </div>
            </v-card-title>
            <v-card-text>
              <Liability :liability="liability" />
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>

      <v-layout row wrap>
        <v-flex>
          <v-card>
            <v-card-title primary-title>
              <div>
                <h3 class="headline mb-0">Спрос</h3>
              </div>
            </v-card-title>
            <v-card-text>
              <p class="t-break" v-for="(item, i) in asks" :key="i">
                <b>account: </b>\{{ item.account }}<br/>
                <b>model: </b>\{{ item.model }}<br/>
                <b>objective: </b>\{{ item.objective }}<br/>
                <b>token: </b>\{{ item.token }}<br/>
                <b>cost: </b>\{{ item.cost }}<br/>
                <b>validatorFee: </b>\{{ item.validatorFee }}<br/>
                <b>deadline: </b>\{{ item.deadline }}
              </p>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import getRobonomics from '../utils/robonomics'
import { formatDecimals, watchTx } from '../utils/utils'
import Liability from './Liability'
import * as config from '../config'

let robonomics

export default {
  name: 'order',
  components: {
    Liability
  },
  data () {
    return {
      robonomicsStatus: false,
      loadingApprove: false,
      loadingOrder: false,
      price: {
        value: 0,
        valueStr: `${formatDecimals(0, 9)} XRT`
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
      model: config.MODEL,
      account: '',
      lighthouse: {
        name: '',
        address: ''
      },
      liability: null,
      asks: [],
      bids: []
    }
  },
  created () {
    robonomics = getRobonomics(config.LIGHTHOUSE)
    robonomics.ready().then(() => {
      this.fetchData()
        .then(() => {
          this.robonomicsStatus = true
          this.balance.address = robonomics.xrt.address
          this.lighthouse.name = robonomics.lighthouse.name
          this.lighthouse.address = robonomics.lighthouse.address
          this.account = robonomics.account

          robonomics.getAsk(this.model, (msg) => {
            this.asks = [{ ...msg }, ...this.asks.slice(0, 10)]
          })
          robonomics.getBid(this.model, (msg) => {
            this.bids = [{ ...msg }, ...this.bids.slice(0, 10)]
          })
          robonomics.getResult((msg) => {
            console.log('result unverified', msg)
            if (this.liability !== null && msg.liability === this.liability.address) {
              this.setResult(msg.result, false)
            }
          })
        })
    })
  },
  methods: {
    fetchData () {
      return robonomics.xrt.call('balanceOf', [robonomics.account])
        .then((balanceOf) => {
          this.balance.value = balanceOf
          this.balance.valueStr = `${formatDecimals(balanceOf, 9)} XRT`
          if (balanceOf > 0) {
            return robonomics.xrt.call('allowance', [robonomics.account, robonomics.factory.address])
          }
          return false
        })
        .then((allowance) => {
          if (allowance) {
            this.approveTrade.value = allowance
            this.approveTrade.valueStr = `${formatDecimals(allowance, 9)} XRT`
          }
        })
    },
    sendApproveTrade () {
      this.loadingApprove = true
      return robonomics.xrt.send('approve', [robonomics.factory.address, (this.price.value * 100)], { from: robonomics.account })
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
      this.liability.result = result
      this.liability.check = check
    },
    newLiability (liability) {
      console.log('liability ask', liability.address)
      return liability.getInfo()
        .then((info) => {
          this.liability = {
            address: liability.address,
            lighthouse: liability.lighthouse,
            worker: liability.worker,
            ...info
          }
          liability.watchResult((result) => {
            console.log('result check', result)
            this.setResult(result, true)
          })
          return true
        })
    },
    order () {
      this.liability = null
      this.loadingOrder = true
      web3.eth.getBlock('latest', (e, r) => {
        const ask = {
          objective: config.OBJECTIVE,
          token: robonomics.xrt.address,
          cost: this.price.value,
          validator: '0x0000000000000000000000000000000000000000',
          validatorFee: 0,
          deadline: r.number + 1000
        }
        robonomics.postAsk(this.model, ask)
          .then((liability) => {
            this.newLiability(liability)
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
