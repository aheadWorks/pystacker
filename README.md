# pystacker

## Running as docker container

```bash
docker run -p10080:80 -v /data:/data -v /var/run/docker.sock:/var/run/docker.sock -e APP_ID=stacker -e APP_HOST=localhost -e DOCKERHUB_LOGIN=mylogin -e DOCKERHUB_PASSWORD=mypassword -d aheadworks/pystacker:latest
```

will run pystacker at http://localhost:10080 and data directory(where stacks configs are stored) mounted at `/data` at host machine

## Development mode

* clone this repository
* copy `pystacker-backend/config/app.dist.yml` to `pystacker-backend/config/app.yml`
* install pystacker-backend package to your python environment(virualenv recommended): `pip install -e pystacker-backend`
* install JS requirements: `cd pystacker-front && npm install`

Running backend:
`cd pystacker-backend && python run.py`

Running frontend dev server:
`cd pystacker-front && npm run serve`

