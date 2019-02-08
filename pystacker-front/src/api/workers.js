import  api from './graphql'

export default {
    all(){
        let q = "workers {name, interval}"
        return api.query(q)
            .then((d) => d['workers'])
    },
    force(name){
        return api.mutation('forceWorker(name:"'+name+'"){name, interval}')
            .then((r) => r['forceWorker'])
    }
}

