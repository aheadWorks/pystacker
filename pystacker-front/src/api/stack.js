import  api from './graphql'

export default {
    all(cb){
        let q = "stacks {name, links, id, meta, from_template, services {name, status, image}}"
        return api.query(q)
            .then((d) => {cb(d['stacks'])})
    },
    one (cb, id){
        let q = "stack(id:"+id+") {name, links, id, meta, from_template, services {name, status, image}}"
        return api.query(q)
            .then((d) => {cb(d['stack'])})
    },
    cmd(listener, cmd, id){
        return api.subscription("runCmd( id:"+parseInt(id)+", cmd:"+cmd+")", r => listener(r['runCmd']))

    },
    exec(listener, stack_id, service_name, cmd){
        return api.subscription("execServiceCmd (stack_id: "+stack_id+", service_name:\""+service_name+"\", cmd: "+JSON.stringify(cmd)+")", r => listener(r['execServiceCmd']))
    },
    logs(listener, stack_id, service_name){
        return api.subscription("getLogs (stack_id: "+stack_id+", service_name:\""+service_name+"\")", r => listener(r['getLogs']))
    },
    pullImages(listener, id){
        return api.subscription("pullImages( id:"+parseInt(id)+") {id, status, service, stack_id, progressDetail {current, total} }", r => listener(r['pullImages']))
    },
    create(id, name, vars){
        let v = [];
        for(let k in vars){
            if(vars.hasOwnProperty(k)) {
                v.push([k, vars[k]])
            }
        }

        let m = "createStack(name:\""+name+"\", from_template:\""+id+"\", vars:"+JSON.stringify(v)+") {id}"
        return api.mutation(m).then((r) => r['createStack'])
    },
    delete(id){
        return api.mutation('deleteStack(id:'+parseInt(id)+')')
            .then((r) => r['deleteStack'])
    }
}
