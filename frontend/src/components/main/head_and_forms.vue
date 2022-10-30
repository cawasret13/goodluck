<template>
    <div class="flex">
        <div class="menu">
            <div class="d_menu">
                dlsdjlakjsfl
            </div>
        </div>
        <div class="content">
            <div class="controll">
                <div class="inf_user">
                    <img src="../../assets/icon-256x256.png" alt="">
                    <p>Бабич Александр</p>
                </div>
                <div class="button_place">
                    <button>Импорт</button>
                </div>                
            </div>
            <div class="at_house" v-if="this.selectHouse != null">
                <h2>Эталон</h2>
                <h4>{{this.selectHouse}}</h4>
                <button v-on:click="r">Показать аналоги</button>
                <h3 v-if="this.list_analogs != null" style="text-align: center;">Мы нашли {{this.list_analogs.length-1}} аналог(ов)</h3>
                <div class="list_analods">
                    <div v-for=" (info, index_arr) in this.list_analogs" class="analog">
                        <div class="photo">
                            <div class="div_photo" v-bind:class="getPhoto(info['info']['id']) != index?'none':' '" v-for="(photos, index) in JSON.parse(info['photo'])" style="background:url(); backdrop-filter:blur(5px)">
                                <img  :data-index="index" class="img" :src="photos" alt="">
                                <img  :data-index="index" class="back_img" :src="photos" alt="">
                            </div>
                            <div class="bar_photo"><div class="br_text"><h5>{{this.photo[info['info']['id']]+1}}/{{JSON.parse(info['photo']).length}}</h5></div></div>
                            <div class="contr_img">
                                <button v-on:click="backPhoto(info['info']['id'])">
                                    <img class="icon_ctrl_photo" src="../../assets/img/icon/left_str.svg" alt="">
                                </button>
                                <button v-on:click="nextPhoto(info['info']['id'], index_arr)">
                                    <img class="icon_ctrl_photo" src="../../assets/img/icon/right_str.svg" alt="">
                                </button>
                            </div>
                        </div>
                        <div class="information">
                            <div class="character"><h4>Цена</h4><h4>{{info["info"]["price"]}}₽</h4></div>
                            <div class="character"><h4>Комнаты</h4><h4>{{info["info"]["rooms"]}}</h4></div>
                            <div class="character"><h4>Этаж</h4><h4>{{info["info"]["floor"]}}/{{info["info"]["totalFloor"]}}</h4></div>
                            <div class="character"><h4>Площадь общая</h4><h4>{{info["info"]["area"]}} м²</h4></div>
                            <div class="character"><h4>Площадь кухни</h4><h4>{{info["info"]["areaKitchen"]}} м²</h4></div>
                            <div class="character"><h4>Балкон</h4><h4>{{info["info"]["balcony"]}}</h4></div>
                            <div class="character"><h4>Ремонт</h4><h4>{{info["info"]["repair"]}}</h4></div>
                            <div class="character"><h4>Дом</h4><h4>{{info["info"]["typeHouse"]}}</h4></div>
                        </div>
                        <button v-if="getAnalog(info['info']['id']) == false" v-on:click="addAnalog(info['info']['id'])">Выбрать</button>
                        <button v-else v-on:click="addAnalog(info['info']['id'])">Убрать</button>
                    </div>
                </div>
                <button v-if="this.selectAnalog.length >=3">Рассчитать</button>
            </div>

            <div v-if="this.flag == 0">
                <h4 style="text-align: center; margin-top: 20%;color: #959595;">Загрузите файл</h4>
                    <input type="file" id="file" ref="file" accept=".xls, .xlsx" v-on:change="handleFileUpload()">
                    <button v-on:click="submitFile">Отправить</button>
                <h1> file {{this.file.name}}</h1>
            </div>
            
            <div v-else-if="this.flag == 1" class="load_data">
                <img src="../../assets/48x48.gif" alt="">
            </div>
            <div class="res" v-else-if="this.flag == 2">
                <div class="list">
                    <h4>Местоположение</h4>
                    <h4>Количество комнат</h4>
                    <h4>Сегмент </h4>
                    <h4>Этажность дома</h4>
                    <h4>Материал стен</h4>
                    <h4>Этаж расположения</h4>
                    <h4>Площадь квартиры, кв.м</h4>
                    <h4>Площадь кухни, кв.м</h4>
                    <h4>Наличие балкона/лоджии</h4>
                    <h4>Удаленность от станции метро, мин. пешком</h4>
                    <h4>Состояние</h4>
                </div>
                <div v-for="obj in this.list" class="list">
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
                    <!-- <input type="radio" :value="location" name="contact" v-model="selectHouse"> -->
                    <input type="radio" name="sel_house" v-on:change="selectHouseValue(obj.id_Apart)">
                </div>
            </div>
           
        </div>
    </div>
    <!-- <div >
        <h1>{{obj['location']}}  {{obj['numRooms']}}</h1>
    </div> -->
</template>
<script>
import {mapGetters} from 'vuex'
    export default{
        computed: mapGetters(['getOpenForm', 'getIdUser']),
        data(){
            return{
                file: '',
                list:'',
                selectHouse:null,
                flag:0,
                id_session:'',
                list_analogs:null,
                selectAnalog:[],
                photo:[],

            }
        },
        methods: {
        backPhoto(id){
            if (this.photo[id]>0){
                this.photo[id]--
            }
        },
        nextPhoto(id, index){
            if(this.photo[id] < JSON.parse(this.list_analogs[index]["photo"]).length-1){
                this.photo[id]++
            }
        },
        getPhoto(index){
            return this.photo[index]
        },
        getAnalog(id){
            return this.selectAnalog.includes(id)
        },
        addAnalog(id){
            if(this.selectAnalog.includes(id)){
                let index = this.selectAnalog.indexOf(id)
                this.selectAnalog.splice(index, 1)
            }else{
                this.selectAnalog.push(id)
            }
            console.log(this.selectAnalog)
        },
        async r(){
            fetch(`http://localhost:8000/api/v1/ref?id_session=`+this.id_session).then(req=>req.json()).then(info=>{
                this.list_analogs = JSON.parse(info)
                for (var index = 0; index < this.list_analogs.length; index++){
                    this.photo[this.list_analogs[index]['info']["id"]] = 0
                } 
            })
        },
        
         selectHouseValue(id){
            this.selectHouse = id
            this.SendReferents()
        },
        submitFile(){
            if(this.file != ''){
                this.flag = true
                let formData = new FormData();
                formData.append('file', this.file);
                formData.append('id_user', '11k,w1k1o');
                this.list = fetch("http://localhost:8000/api/v1/calc",{
                    method: "POST",
                    body: formData
                }).then(data=>data.json()).then(save=>{
                    this.id_session = save["id_session"]
                    this.list = save["data"]
                    this.flag = 2
                });
            }else{
                console.log("Not File")
            }
        },
        handleFileUpload(){
            this.file = this.$refs.file.files[0];
        },
        async SendReferents(){
            let data={
                "id_session":this.id_session,
                "id_ref":this.selectHouse,
                "id_user":"11k,w1k1o",
            }
            fetch("http://localhost:8000/api/v1/ref",{
                    method: "POST",
                    headers:{
                        "Content-Type":"application/json"
                    },
                    body: JSON.stringify(data)
            }).then(data=>{
                console.log(data.json())
            })
        },  
        }
    }
</script>
<style>
   
</style>