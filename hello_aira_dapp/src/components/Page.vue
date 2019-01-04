<template>
  <div>
    <Hello />
    <v-divider style="margin:20px 0;"/>
    <Trade />
  </div>
</template>

<script>
import Hello from './Hello'
import Trade from './Trade'

export default {
  name: 'Page',
  components: {
    Hello,
    Trade
  }
}
</script>
