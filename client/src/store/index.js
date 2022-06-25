import {createStore} from "vuex";
import {publiсationsModule} from "./publiсationsModule";


export default createStore({
  modules: {
    publiсationsModule: publiсationsModule,
  }
})