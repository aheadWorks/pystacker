    class Query {
    constructor(endpoint) {
        this.ep = endpoint
        this.named_sockets = {}
    }


    getSocket(pf) {

        /*if (this.getSocket.server && this.getSocket.server.readyState < 2) {
            console.log("reusing the socket connection [state = " + this.getSocket.server.readyState + "]: " + this.getSocket.server.url);
            return Promise.resolve(this.getSocket.server);
        }*/

        return new Promise( (resolve, reject) => {

            this.getSocket.server = new WebSocket('ws://'+this.ep+pf);

            this.getSocket.server.onopen = () => {
                resolve(this.getSocket.server);
            };

            this.getSocket.server.onerror = function (err) {
                reject(err);
            };
        });
    }


    _fetch(...params) {
        return fetch(...params)
                .then(r => r.json())
                .then(b => {if (b['error']){
                        return Promise.reject(b['error'])
                    }
                    return b;
                })
    }

    query(q) {
        let _q = 'query {'+q+'}'
        let u = '//' + this.ep + '/query?query=' + encodeURIComponent(_q);
        return this._fetch(u)
    }

    mutation(q) {
        let u = '//' + this.ep + '/query';
        let b = "mutation {" + q + "}"
        return this._fetch(u, {method: "POST", body: b});
    }

    subscription(q, listener) {
        let b = "subscription {" + q + "}";

        return new Promise((resolve, reject) => {
            this.getSocket('/subscribe').then(server => {
                server.onmessage = d => {
                    let response = JSON.parse(d.data)
                    listener(response)

                };
                server.onclose = d => {
                    if(d.wasClean){
                        resolve(d)
                    }
                    else{
                        reject(d)
                    }
                };
                server.send(JSON.stringify({query:b}))
            })
        })

    }
}


const q = new Query(window.location.host + '/api/v1')

export default q
