<template>
    <div  class="resualt">
        <div v-if="getReport.length == 0">
            <div class="obj" v-for="obj in getHistory">
                <div class="price">
                    <h3>{{obj["id_ref"]}}</h3>
                    <h3>Цена квартиры: {{obj["price"]}} ₽</h3>
                    <h3>Цена за 1 кв.м: {{obj["priceMeter"]}} ₽</h3>
                </div>
                <div class="analogue" v-for=" history, index in obj['report']">
                    <h1>Аналог {{index+1}}   {{history['id_a']}}</h1>

                    <div>
                        <h3>Разница: {{history["difference"]}}</h3>
                        <h3>Размер:  {{history["size"]}}%</h3>
                        <h3>Вес:     {{history["weight"]}}</h3>
                        <h3>Цена:    {{history["price"]}} ₽</h3>
                    </div>
                    <div class="ls_cof">
                        <h3 style="text-align: center;margin-bottom: 1%;">Корректировки</h3>
                        <div v-for="cof in history['coefficient']">
                            <div class="char">
                                <h3 class="h_d">{{cof['discription']}}</h3>
                                <h3 class="h_c"><input :id="cof['id']" ref="inp_coef" v-on:change="changeCoef(cof['id'], this.$refs.inp_coef, getSession)" style="text-align: center;" type="text" :value="cof['coef']" ></h3>
                                <h3 class="h_e">{{cof['price']}}₽</h3>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <button class="button_pull" v-on:click="CalcPool(getSession)">Рассчитать весь пул</button>
        </div>
        <div v-else>
            <div class="report">
                <h1>Отчет</h1>
                <button v-on:click="CalcPool(getSession)">Скачать</button>
            </div>
            <div class="list">
        <div class="onj_ls">
            <h4 class="h4_title_ls" style="font-size: 11px;">Местоположение</h4>
            <h4 class="h4_title_ls" style="font-size: 11px;">Количество комнат</h4>
            <h4 class="h4_title_ls" style="font-size: 11px;">Сегмент</h4>
            <h4 class="h4_title_ls" style="font-size: 11px;">Этажность дома</h4>
            <h4 class="h4_title_ls" style="font-size: 11px;">Материал стен</h4>
            <h4 class="h4_title_ls" style="font-size: 11px;">Этаж расположения</h4>
            <h4 class="h4_title_ls" style="font-size: 11px;">Площадь квартиры</h4>
            <h4 class="h4_title_ls" style="font-size: 11px;">Площадь кухни</h4>
            <h4 class="h4_title_ls" style="font-size: 11px;">Наличие балкона/лоджии</h4>
            <h4 class="h4_title_ls" style="font-size: 11px;">Удаленность от станции метро</h4>
            <h4 class="h4_title_ls" style="font-size: 11px;">Состояние</h4>
            <h4 class="h4_title_ls" style="font-size: 11px;">Цена</h4>
        </div>
        <div v-for="obj in getReport" class="onj_ls">
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
            <h4>{{obj["price"]}} ₽</h4>
        </div>
    </div>
        </div>
    </div>
</template>


<script>
    import { val } from 'dom7';
import { mapGetters, mapMutations } from 'vuex';
    export default{
        computed: mapGetters(['getHistory', 'getInfoReference', 'getSession', 'getReport']),
        data(){
            return{
                newCoef:0
            }
        },
        methods:{
            ...mapMutations(['NewHistory', 'report']),
            async changeCoef(id, val, id_session){
                let newCoef = 0
                for(let i = 0;i<val.length;i++){
                    if(val[i].id == id){
                        if(val[i].value == null){
                            newCoef = 0
                        }else{
                            newCoef = val[i].value
                        }
                    }
                }
                fetch('http://localhost:8000/api/v1/change/coefficient?id_session='+id_session+'&id='+id+'&new='+newCoef).then(res => res.json()).then(data=>{
                    this.NewHistory(JSON.parse(data))
                })
            }, 
            async CalcPool(id_session){
                fetch('http://localhost:8000/api/v1/calc/pool?id_session='+id_session).then(res=>res.json()).then(data=>{
                    this.report(data)
                })
            }
        }
    }
</script>
<style>
    @import url('../../assets/style/resualt.css')
</style>