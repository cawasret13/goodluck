<template>
    <div class="resualt">
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
    </div>
</template>


<script>
    import { val } from 'dom7';
import { mapGetters } from 'vuex';
    export default{
        computed: mapGetters(['getHistory', 'getInfoReference', 'getSession']),
        data(){
            return{
                newCoef:0
            }
        },
        methods:{
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
                fetch('http://localhost:8000/api/v1/change/coefficient?id_session='+id_session+'&id='+id+'&new='+newCoef)
                console.log(newCoef, id, id_session)
            }
        }
    }
</script>
<style>
    @import url('../../assets/style/resualt.css')
</style>