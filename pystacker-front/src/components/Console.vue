<template>
  <ul v-chat-scroll="{always: false, smooth: true}">
    <li
      v-for="(line, n) in lines" :key="n">{{line}}
    </li>
  </ul>
</template>

<script>
  import VueChatScroll from 'vue-chat-scroll'
  import Vue from 'vue'

  Vue.use(VueChatScroll)

  export default {
    name: "Console",
      props: {
        lines: Array
      }
  }
</script>

<style scoped>
  ul {
    background-color: black;
    padding: 0 0.5rem;
    max-height:80vh;
      overflow-y: scroll
  }

  li {
    font-family: Consolas, monospace;
    white-space: nowrap;
    color: lawngreen;
    font-size: 0.8rem;
  }

</style>
