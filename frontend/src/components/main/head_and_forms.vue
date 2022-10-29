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
                <button v-on:click="SendReferents">Рассчитаь</button>
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
                <button>Далее</button>
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
                id_session:''
            }
        },
        methods: {
         selectHouseValue(id){
            this.selectHouse = id
        },
        submitFile(){
            if(this.file != ''){
                this.flag = true
                let formData = new FormData();
                formData.append('file', this.file);
                formData.append('id_user', '11k,w1k1o');
                this.list = fetch("http://45.9.24.240:7000/api/v1/calc",{
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
            fetch("http://45.9.24.240:7000/api/v1/ref",{
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