<template>
<div class="sl">
    <div v-bind:class="getStep ==0?'on':'off'">
    <p style="margin-top: 0;text-align: center;">Расположение дома</p>
    <div class="s1a">
        <div class="s1d">
            <p>Метро</p>
            <select name="" id="">
                <option value="">Не выбрано</option>
                <option v-for="st in getMaetro[0]" value="">{{st.name}}</option>
            </select>
            <div style="width:100%;display:inline-flex;justify-content: space-evenly;align-items:center;flex-direction: column;align-content: space-between;">
                <p style="margin-bottom: 5px;">До метро</p>
                <div class="metro_c">
                    <button class="b_p">Пешком</button>
                    <button class="b_t">Транспорт</button>
                </div>
                <input style="text-align: center;" class="s1i" type="text" placeholder="10 мин">
            </div>
        </div>
        <div class="s1d">
            <p>или</p>
        </div>
        <div class="s1d">
            <p>Район</p>
            <select name="" id="" >
                <option value="">Не выбрано</option>
                <option value="">Митино</option>
            </select>
        </div>
    </div>
  </div>
  <div v-bind:class="getStep ==1?'on':'off'">
    <p style="margin-top: 0;text-align: center;">Информация о доме</p>
    <div class="s2">
        <div class="s2d">
            <p>Этажей в доме</p>
            <input type="text">
        </div>
        <div class="s2d">
            <p>Квартир на этаже</p>
            <input type="text">
        </div>
        <div class="s2d">
            <p>Тип дома</p>
            <select name="" id="">
                <option value="">Панельны</option>
                <option value="">Блочный</option>
                <option value="">Кирпичный</option>
                <option value="">Сталинский</option>
                <option value="">Монолитный</option>
                <option value="">Элитное жилье</option>
            </select>
        </div>
    </div>
  </div>
  <div v-bind:class="getStep ==2?'on':'off'">
    <p style="margin-top: 0;text-align: center;">Информация о квартире</p>
    <div class="s3">
        <div class="s3_bl">
            <div class="s3d">
                <p>Количество комнат</p>
                <div class="crtl_rooms">
                    <button style="border-bottom-left-radius: 13px;border-top-left-radius: 13px;">1</button>
                    <button>2</button>
                    <button>3</button>
                    <button style="border-bottom-right-radius: 13px;border-top-right-radius: 13px;">4+</button>
                </div>
            </div>
            <div class="s3d">
                <p>Площадь квартиры</p>
                <input type="text" name="" id="">
            </div>
            <div class="s3d">
                <p>Площадь кухни</p>
                <input type="text" name="" id="">
            </div>
        </div>
        <div class="s3_bl">
            <div class="s3d">
                <p>Состояние квартиры</p>
                <select name="" id="">
                    <option value="">Не требует ремонта</option>
                </select>
            </div>
        </div>
    </div>
  </div>
  <div v-bind:class="getStep ==3?'on':'off'">
    <div style="width: 100%;display: flex;justify-content: center;margin-top: 16%;">
        <button class="btn_res" v-on:click="Load(1)">Рассчитать</button>
    </div>
  </div>
  <div class="controll_form">
    <button v-if="getStep != 0" v-on:click="back(1)"><img style="height: 50%;" src="../../assets/left.svg" alt=""></button>
    <button v-if="getStep != 3" v-on:click="next(1)"><img style="height: 50%;" src="../../assets/right.svg" alt=""></button>
  </div>
</div>
</template>
<script>
    import {mapMutations, mapGetters, mapActions} from 'vuex'
    export default{
        methods:{
            ...mapMutations(['Load', 'back', 'next']),
            ...mapActions(['loadMetroData']),
        },
        async mounted() {
            this.loadMetroData(1)
        },
        computed: mapGetters(['getStep', 'getMaetro']),
        
    }
</script>
