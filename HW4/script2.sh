function load_creds {
	export OS_USERNAME=admin
	export OS_PASSWORD=secret
	export OS_PROJECT_NAME=admin
	export OS_PROJECT_DOMAIN_ID=default
	export OS_USER_DOMAIN_ID=default
	export OS_IDENTITY_API_VERSION=3
	export OS_AUTH_URL=http://$ENDPOINT_URL/identity
	export OS_NETWORK_API=$ENDPOINT_URL:9696 
}

function remove_quotes {
	string=$1
	temp="${string%\"}"
	temp="${temp#\"}"
	echo $temp
}

function auth {
	data='{ "auth": {
		"identity": {
		"methods": ["password"],
		"password": {
		"user": {
		"name": "admin",
		"domain": { "id": "default" },
		"password": "secret"
	}}},
	"scope": {
	"project": {
	"name": "admin",
	"domain": { "id": "default" }}}}}'
	header='Content-Type: application/json'
	result=`curl -i -s -H "$header" -d "$data" "http://$ENDPOINT_URL/identity/v3/auth/tokens"`
	token_header=`echo "$result" | grep -Fi X-Subject-Token`
	arr=($token_header)
	OS_TOKEN=${arr[1]}
	export OS_TOKEN=${OS_TOKEN//$'\015'}
}

function list_servers {
	header="X-AUTH-Token:$OS_TOKEN"
	curl -s -H "$header" "http://$ENDPOINT_URL/compute/v2.1/servers" | jq '[.servers[] | {id: .id, name: .name}]'
}

function list_networks {
	header="X-AUTH-Token:$OS_TOKEN"
	curl -s -H "$header" "http://$OS_NETWORK_API/v2.0/networks" | jq '[.networks[] | {id: .id, status: .status, name: .name}]'
}

function list_router {
	header="X-AUTH-Token:$OS_TOKEN"
	router_id=`curl -s -H "$header" "http://$OS_NETWORK_API/v2.0/routers" | jq '.routers[0].id'`
	router_id=`remove_quotes $router_id`
	curl -s -H "$header" "http://$OS_NETWORK_API/v2.0/ports?device_id=$router_id" | jq '[.ports[] | {id: .id, status: .status, network: .network_id}]'

}

export ENDPOINT_URL=$1
load_creds
auth
servers=`list_servers`
networks=`list_networks`
routers=`list_router`
echo "{servers: $servers, networks: $networks, router: $routers}"
