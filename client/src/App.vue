<template>
  <navbar></navbar>
  <section class="content col-lg-12" style="height: calc(100vh - 75px)">
    <router-view></router-view>
  </section>
</template>

<script>
import Navbar from "./components/Navbar";
import 'bootstrap/dist/css/bootstrap.css';
import {mapMutations} from 'vuex';

export default {
  components: {
    Navbar
  },
  methods: {
    ...mapMutations({
      setAuth: 'auth/setAuth',
    })
  },
  beforeMount() {
    if(localStorage.getItem('token')) {
      this.setAuth(true)
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
