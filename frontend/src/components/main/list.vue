<template>
    <div class="controll">
        <h3 v-if="getSelectReference.length == 0" class="h4_title mn">Выбирите эталон(ы)</h3>
        <h3 v-else-if="getSelectReference.length == 1" class="h4_title mn">Вы выбрали 1 эталон</h3>
        <h3 v-else class="h4_title mn">Вы выбрали {{getSelectReference.length}} эталонов</h3>
        <button v-on:click="searchAnalogues()">Найти</button>
    </div>
    <div class="list">
        <div class="onj_ls">
            <h4 class="h4_title_ls">Местоположение</h4>
            <h4 class="h4_title_ls">Количество комнат</h4>
            <h4 class="h4_title_ls">Сегмент</h4>
            <h4 class="h4_title_ls">Этажность дома</h4>
            <h4 class="h4_title_ls">Материал стен</h4>
            <h4 class="h4_title_ls">Этаж расположения</h4>
            <h4 class="h4_title_ls">Площадь квартиры</h4>
            <h4 class="h4_title_ls">Площадь кухни</h4>
            <h4 class="h4_title_ls">Наличие балкона/лоджии</h4>
            <h4 class="h4_title_ls">Удаленность от станции метро</h4>
            <h4 class="h4_title_ls">Состояние</h4>
            <h4 style="width: 1%;"> </h4>
        </div>
        <div v-for="obj in getFileData" class="onj_ls">
            <h4>{{obj["location"]}}</h4>
            <h4>{{obj["numRooms"]}}</h4>
            <h4>{{obj["segment"]}}</h4>
            <h4>{{obj["floorsHouse"]}}</h4>
            <h4>{{obj["materialWall"]}}</h4>
            <h4>{{obj["floor"]}}</h4>
            <h4>{{obj["areaApart"]}}</h4>
            <h4>{{obj["areaKitchen"]}}</h4>
            <h4>{{obj["balcony"]}}</h4>
            <h4>{{obj["proxMetro"]}}</h4>
            <h4>{{obj["structure"]}}</h4>
            <input type="checkbox" name="sel_house" v-on:change="addReference(obj.id_Apart), loadReferece(getSelectReference)">
        </div>
    </div>
</template>
<script>
    import { mapGetters, mapMutations, mapActions} from 'vuex';
    export default{
        computed: mapGetters(['getFileData', 'getSelectReference', 'getSession']),
        methods: {
            ...mapMutations(['addReference']),
            ...mapActions(['loadReferece', 'searchAnalogues'])
        }
    }
</script>
<style scoped>
    @import url('../../assets/style/list.css')
</style>