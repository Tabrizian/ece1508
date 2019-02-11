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

function convert_to_array {
	($1)
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


function create_network {
	name=$1
	public=$2
	ip_range=$3
	header="X-AUTH-Token:$OS_TOKEN"
	data="{ \
		\"network\": { \
		\"name\": \"$name\", \
		\"router:external\": $public, \
		\"admin_state_up\": true}}"
	network_id=`curl -s -H "$header" -d "$data" "http://$OS_NETWORK_API/v2.0/networks" | jq '.network.id'`
	network_id=`remove_quotes $network_id`
	data="{ \
		\"subnet\": { \
		\"name\": \"$1-subnet\", \
		\"enable_dhcp\": true, \
		\"network_id\": \"$network_id\", \
		\"ip_version\": 4, \
		\"cidr\": \"$ip_range\" }}"
	subnet_id=`curl -s -H "$header" -d "$data" "http://$OS_NETWORK_API/v2.0/subnets" | jq '.subnet.id'`
	subnet_id=`remove_quotes $subnet_id`
	echo "$subnet_id $network_id"
}

function create_server {
	name=$1
	flavor=$2
	image=$3
	network=$4
	header="X-AUTH-Token:$OS_TOKEN"
	content_type='Content-Type: application/json'
	data="{ \"server\": { \
		\"name\": \"$name\", \
		\"flavorRef\": \"$flavor\", \
		\"imageRef\": \"$image\",\
		\"networks\": [{\
		\"uuid\": \"$network\"}]}}"
	curl -s -H $content_type -H "$header" -d "$data" "http://$ENDPOINT_URL/compute/v2.1/servers"
}

function get_image_id {
	image=$1
	header="X-AUTH-Token:$OS_TOKEN"
	image_id=`curl -s -H "$header" "http://$ENDPOINT_URL/image/v2/images?name=in:$1" | jq '.images[0].id'`
	remove_quotes $image_id
}

function get_flavor_id {
	flavor=$1
	header="X-AUTH-Token:$OS_TOKEN"
	flavor_id=`curl -s -H "$header" "http://$ENDPOINT_URL/compute/v2.1/flavors" | jq ".flavors[] | select(.name==\"$flavor\") | .id"`
	remove_quotes $flavor_id
}

function create_router {
	name=$1
	header="X-AUTH-Token:$OS_TOKEN"
	data="{ \"router\": { \
		\"name\": \"$name\", \
		\"admin_state_up\": true }}"
	router=`curl -s -H "$header" -d "$data" "http://$OS_NETWORK_API/v2.0/routers" | jq '.router.id'`
	remove_quotes $router
}

function add_interface_to_router {
	router=$1
	interface=$2
	header="X-AUTH-Token:$OS_TOKEN"
	data="{ \
		\"subnet_id\": \"$interface\"}"
	curl -X PUT -s -H "$header" -d "$data" "http://$OS_NETWORK_API/v2.0/routers/$1/add_router_interface"
}

export ENDPOINT_URL=$1

load_creds
auth 
red=`create_network blue false "10.0.0.0/24"`
red=($red)
echo "Blue network created"
blue=`create_network red false "192.168.1.0/24"`
blue=($blue)
echo "Red network created"
public=`create_network public true "172.24.4.0/24"`
public=($public)
echo "Public network created"
router=`create_router router`
echo "Router was created"
interface1=`add_interface_to_router $router ${red[0]}`
echo "Interface ${red[0]} was added to router"
interface2=`add_interface_to_router $router ${blue[0]}`
echo "Interface ${blue[0]} was added to router"
interface3=`add_interface_to_router $router ${public[0]}`
echo "Interface ${public[0]} was added to router"
image_id=`get_image_id "cirros-0.3.5-x86_64-disk"`
flavor_id=`get_flavor_id "m1.nano"`
vm1=`create_server "vm1" $flavor_id $image_id ${blue[1]}`
echo "VM1 created"
vm2=`create_server "vm2" $flavor_id $image_id ${red[1]}`
echo "VM2 created"
vm3=`create_server "vm3" $flavor_id $image_id ${public[1]}`
echo "VM3 created"


