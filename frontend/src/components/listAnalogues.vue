<template>
    <div v-if="getAnalog.length >= 3 * getAnalogues.length" class="controll" style="justify-content: space-between;z-index: 2;">
        <h3>Мы готовы начать рассчитывать цену для эталонов</h3>
        <button v-on:click="report">Рассчитать</button>
    </div>
    <h2 class="h4_title">Аналоги ({{getAnalog.length}} шт.)</h2>
    <div class="anal">
        <swiper
            class="swiper obj_ref"
            :modules="modules"
            :space-between="30"
            :slides-per-view="3"
            :slides-per-group="3"
            :loop="true"
            :loop-fill-group-with-blank="true"
            :navigation="true"
            :pagination="{ clickable: true }"
            v-for="obj in getAnalogues"
        >
            <swiper-slide class="cell_ana" v-for="info in obj['resualt']['data']">
                <div class="photo">
                    <swiper
                        class="swiper"
                        :modules="modules"
                        :pagination="{ clickable: true, renderBullet: bulletRenderer }"
                    >
                        <swiper-slide v-for="slide in JSON.parse(info['photo'])" :key="slide" class="slide">
                            <img class="img_cell" :src="slide" />
                            <img class="img_cell_b" :src="slide" />
                        </swiper-slide>
                    </swiper>
                </div>
                <div class="info">
                    <div class="character"><h4>id</h4><h4>{{info["info"]["id"]}}</h4></div>
                    <div class="character"><h4>Адрес</h4><h4>{{info["info"]["address"]}}</h4></div>
                    <div class="character"><h4>Цена</h4><h4>{{info["info"]["price"]}}₽</h4></div>
                    <div class="character"><h4>Комнаты</h4><h4>{{info["info"]["rooms"]}}</h4></div>
                    <div class="character"><h4>Этаж</h4><h4>{{info["info"]["floor"]}}/{{info["info"]["totalFloor"]}}</h4></div>
                    <div class="character"><h4>Площадь общая</h4><h4>{{info["info"]["area"]}} м²</h4></div>
                    <div class="character"><h4>Площадь кухни</h4><h4>{{info["info"]["areaKitchen"]}} м²</h4></div>
                    <div class="character"><h4>Балкон</h4><h4>{{info["info"]["balcony"]}}</h4></div>
                    <div class="character"><h4>Ремонт</h4><h4>{{info["info"]["repair"]}}</h4></div>
                    <div class="character"><h4>Дом</h4><h4>{{info["info"]["typeHouse"]}}</h4></div>
                    <button v-on:click="addAnalog(info['info']['id'])" v-if="getAnalog.includes(info['info']['id']) == false">Выбрать</button>
                    <button v-else v-on:click="addAnalog(info['info']['id'])">Убрать</button>
                </div>
            </swiper-slide>
            <br>
        </swiper>
    </div>
</template>
<script>
    import { mapGetters, mapMutations , mapActions} from 'vuex';
    import SwiperClass, { Pagination , Navigation } from 'swiper'
    import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
    import 'swiper/css'
    import 'swiper/css/pagination'
    import 'swiper/css/navigation'
    export default{
        computed: mapGetters(['getAnalogues', 'getAnalog']),
        methods:{
            ...mapMutations(['addAnalog', ]),
            ...mapActions(['report'])
        },
        components:{
            Swiper,
            SwiperSlide
        },
        setup() {
      return {
        modules: [Pagination, Navigation ]
      }
    }
    }
</script>
<style>
    @import url('../assets/style/analogue.css')
</style>