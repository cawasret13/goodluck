<template>
    <div v-if="getLoad"  class="load">
        <div class="loader"></div>
    </div>
    <div v-if="getLoad == false">
        <menuUser />
        <div v-if="getHistory.length == 0">
            <work />
        </div>
        <div v-else>
            <history />
        </div>
    </div>
</template>
<script>
    import menuUser from '../components/main/menu.vue'
    import work from '../components/main/work.vue'
    import history from '../components/main/history.vue'
    import { mapGetters } from 'vuex';
    export default{
        components:{    
            menuUser,
            work,
            history
        },
        computed: mapGetters(['getLoad', 'getHistory'])
    }
</script>
<style scoped>
    @import url('../assets/style/main.css')
</style>