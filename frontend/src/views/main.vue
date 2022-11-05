<template>
    <div v-if="getLoad"  class="load">
        <div class="loader"></div>
    </div>
    <div v-if="getLoad == false">
        <menuUser />
        <work />
    </div>
</template>
<script>
    import menuUser from '../components/main/menu.vue'
    import work from '../components/main/work.vue'
    import { mapGetters } from 'vuex';
    export default{
        components:{    
            menuUser,
            work
        },
        computed: mapGetters(['getLoad'])
    }
</script>
<style scoped>
    @import url('../assets/style/main.css')
</style>