import { createStore } from 'vuex'

export default createStore({
  state: {
    open: false,
    step: 0,
    metro:[],
  },
  getters: {
    getOpenForm(state){
      return state.open
    },
    getStep(state){
      return state.step
    },
    getMaetro(state){
      return state.metro
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
      console.log(state.metro);
    }
  },
  actions: {
    async loadMetroData(ctx){
      const res = await fetch(
       `http://127.0.0.1:8000/api/v1/metro/` 
     );
     const list = await res.json();
     ctx.commit('loadMetro', list)
   }
  },
  modules: {
  }
})
