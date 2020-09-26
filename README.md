# admission-controller
Proof of Concept

## Build and run

$ podman build . -t flask

$ podman run -p 5000:5000 --rm flask


## Test

N=some-name
NS=some-namespace

curl --silent --header "Content-Type: application/json" --data '{ "apiVersion": "admission.k8s.io/v1", "uid": "'$(openssl rand -hex 10)'", "request": { "name": "'$N'", "namespace": "'$NS'"} }' http://localhost:5000/webhook | jq .

... allowed: false

NS=foo-bar-baz
(repeat curl command)

... allowed: true



