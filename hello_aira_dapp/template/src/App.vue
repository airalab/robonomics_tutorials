<template>
  <div id="app">
    <web3-check :networks="[network]">
      <router-view />
    </web3-check>
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
  .application.theme--light {
    background: #f2f2f2;
    color: rgba(0,0,0,.87);
  }
  .application .theme--light.table tbody tr:not(:last-child), .theme--light .table tbody tr:not(:last-child) {
    border-bottom: 1px solid #ccc;
  }
  table {
    border: 1px solid #ccc;
  }
  table td, table th {
    vertical-align: top !important;
    padding: 13.5px !important;
    padding: .84375rem !important;
  }
  .application .theme--light.card, .theme--light .card {
    border: 1px solid #ccc;
    box-shadow: none;
  }
  .btn {
    width: auto;
    padding: initial;
  }
</style>
