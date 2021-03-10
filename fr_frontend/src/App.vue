<template>
  <router-view/>
</template>

<script>
export default {
  name: "APP",
  data() {
  },
  mounted() {
    // js代码中使用环境变量
    console.log("BASE_URL: ", process.env.BASE_URL);
    console.log("VUE_APP_API: ", process.env.VUE_APP_API);
  }
};
</script>
