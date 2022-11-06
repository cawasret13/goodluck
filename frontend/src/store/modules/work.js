export default{
    state:{
        load:false,
        file: null,
        id_session: null,
        dataFile:null,
        selectReference:[],
        list_analogs:[],
        selectAnalog:[],
        history:[],
        url: 'http://localhost:8000',
    },
    getters:{
        getLoad(state){
            return state.load
        },
        getSession(state){
            return state.id_session
        },
        getInfoFIle(state){
            return state.file
        },
        getFileData(state){
            return state.dataFile
        },
        getSelectReference(state){
            return state.selectReference
        },
        getAnalogues(state){
            return state.list_analogs
        },
        getAnalog(state){
            return state.selectAnalog
        },
        getHistory(state){
            return state.history
        },
        getInfoReference: (state) => (id) => {
            return state.dataFile.find(thing => thing.id === id)
        },
    },
    mutations:{
        LoadFile(state, file){
            state.file = file
        }, 
        load(state, flag){
            state.load = true
        },
        closeLoad(state, flag){
            state.load = false
        },
        loadData(state, data){
            state.dataFile = data
        },
        loadSession(state, id){
            state.id_session = id
            console.log(id, state.id_session)
        },
        addReference(state, id){
            if(state.selectReference.includes(id)){
                let index = state.selectReference.indexOf(id)
                state.selectReference.splice(index, 1)
            }else{
                state.selectReference.push(id)
            }
        },
        addAnalog(state,id){
            if(state.selectAnalog.includes(id)){
                let index = state.selectAnalog.indexOf(id)
                state.selectAnalog.splice(index, 1)
            }else{
                state.selectAnalog.push(id)
            }
            console.log(state.selectAnalog)
        },
    },
    actions:{
        async loadFile(ctx, file){
            if( file != ''){
                let _url = ctx.state.url+'/api/v1/calc'
                let formData = new FormData();
                formData.append('file', file);
                formData.append('id_user', '11k,w1k1o');
                fetch(_url,{
                    method: "POST",
                    body: formData
                }).then(data=>data.json()).then(save=>{
                    ctx.commit("closeLoad", 0)
                    ctx.commit("loadData", save["data"])
                    ctx.commit("loadSession", save["id_session"])
                });
            }else{
                console.log("Not File")
            }
        },
        async loadReferece(ctx, ids){
                let data={
                    "id_session":ctx.state.id_session,
                    "id_ref":ids,
                }
                fetch(ctx.state.url+`/api/v1/ref`,{
                        method: "POST",
                        headers:{
                            "Content-Type":"application/json"
                        },
                        body: JSON.stringify(data)
                }).then(data=>{
                    ctx.commit("closeLoad", 0)
                })
        },
        async searchAnalogues(ctx){
            if(ctx.state.selectReference.length > 0){
                ctx.state.load = true
                fetch(ctx.state.url + `/api/v1/ref?id_session=`+ctx.state.id_session).then(req=>req.json()).then(info=>{
                    ctx.state.list_analogs = JSON.parse(info)
                    ctx.state.load = false
                })
            }
        },
        async report(ctx){
            console.log(ctx.state.selectAnalog, ctx.state.id_session)
            let formData = new FormData();
                formData.append('ids_analogs', ctx.state.selectAnalog);
                formData.append('id_session', ctx.state.id_session);
                fetch('http://localhost:8000/api/v1/calc/report',{
                    method: "POST",
                    body: formData,
            }).then(res => res.json()).then(data => {
                console.log(JSON.parse(data))
                ctx.state.history = JSON.parse(data)
            })
        }
    }
}