<template>
    <div class="work">
        <div v-if="getSession == null" class="import">
            <div class="loadfile">
                <div class="namefile">
                    <h3 v-if="getInfoFIle == null" style="color: #939393;">Загрузите файл</h3>
                    <h3 v-else>{{getInfoFIle.name}}</h3>
                </div>
                <div class="input__wrapper">
                <input name="file" accept=".xls, .xlsx" type="file" id="input__file" class="input input__file" ref="file" v-on:change="LoadFile(this.$refs.file.files[0])">
                <label for="input__file" class="input__file-button">
                    <span class="input__file-button-text">Выберите файл</span>
                </label>
                </div>
            </div>
            <div v-if="getInfoFIle == null" class="no_file">
                <div class="instruction">
                    <h4 class="h4_title">Краткая инструкция</h4>
                </div>
                <div class="ls_instruction">
                    <div class="cell">
                        <span class="step">1</span>
                        <p>
                            Выбирите файл
                        </p>
                    </div>
                    <div class="cell">
                        <span class="step">2</span>
                        <p>
                            Выбирите эталоны
                        </p>
                    </div>
                    <div class="cell">
                        <span class="step">3</span>
                        <p>
                            Подождите немного
                        </p>
                    </div>
                    <div class="cell">
                        <span class="step">4</span>
                        <p>
                            Выбирите аналоги
                        </p>
                    </div>
                    <div class="cell">
                        <span class="step">5</span>
                        <p>
                            Рассчитайте цену для всего пула
                        </p>
                    </div>
                </div>
            </div>
            <div v-else class="send_file">
                <button v-on:click="load(0), loadFile(getInfoFIle)">Начать</button>
            </div>
        </div>
        <div v-else>
            <div v-if="getAnalogues.length == 0">
                <list />
            </div>
            <div v-else>
                <analogue />
            </div>
        </div>
    </div>
</template>

<script>
    import { mapGetters, mapMutations, mapActions } from 'vuex';
    import list from '../main/list.vue'
    import analogue from '../../components/listAnalogues.vue'
    export default{
        computed: mapGetters(['getSession', 'getInfoFIle', 'getAnalogues']),
        methods:{
            ...mapMutations(['LoadFile', 'load']),
            ...mapActions(['loadFile'])
        },
        components:{
            list,
            analogue
        }
    }
</script>

<style>
    @import url('../../assets/style/work.css')
</style>