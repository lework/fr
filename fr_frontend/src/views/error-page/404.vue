<template>
    <div>
       
      <el-empty description="404 NOT FOUND"></el-empty>

    </div>
</template>

<script>
export default {
    name: 'Error404',
    data() {
      return {}
    },
    methods: {
        backPage () {
            this.$router.go(-1);
        },
        goHome () {
            this.$router.push({
                name: 'Home'
            });
        }
    },
    created() {
      console.log("404 NOT FOUND")
      let that = this
      setTimeout(function(){ that.goHome(); }, 5000);
    },
};
</script>
