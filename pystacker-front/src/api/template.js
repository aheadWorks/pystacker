import api from './graphql'


export default {
    all(){
        let q = "templates {name, meta}"
        return api.query(q)
            .then(d => d['templates'])
    },
    one(name) {
        let q = "template(name:\""+name+"\") {name, meta, vars}"
        return api.query(q)
            .then(d => d['template'])
    },
    names(cb) {
        let q = "templates {name}}"
        api.query(q)
            .then(d => cb(d['templates']))
    }

}

