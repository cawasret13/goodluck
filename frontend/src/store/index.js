import { createStore } from 'vuex'

export default createStore({
  state: {
    open: false,
    step: 0,
    metro:[],
    region:[],
    id_user: '1oo2j33211j'
  },
  getters: {
    getIdUser(state){
      return state.id_user
    },
    getOpenForm(state){
      return state.open
    },
    getStep(state){
      return state.step
    },
    getMaetro(state){
      return state.metro
    },
    getRegion(state){
      return state.region
    }
  },
  mutations: {
    Load(state, flag){
      state.open = true;
      state.step = 0
    },
    back(state, flag){
      if(state.step > 0){
        state.step--;
      }
    },
    next(state, flag){
      state.step++;
    },
    loadMetro(state, data){
      state.metro.push(data)
    },
    loadRegion(state, data){
      state.region.push(data)
    }
  },
  actions: {
    async loadMetroData(ctx){
      const res = await fetch(
       `http://127.0.0.1:8000/api/v1/metro/` 
     );
     const list = await res.json();
     ctx.commit('loadMetro', list)
   },
   async loadRegionData(ctx){
    const res = await fetch(
     `http://127.0.0.1:8000/api/v1/region/` 
   );
   const list = await res.json();
   ctx.commit('loadRegion', list)
 }
  },
  modules: {
  }
})
