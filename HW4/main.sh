function load_creds {
	export OS_USERNAME=admin
	export OS_PASSWORD=secret
	export OS_PROJECT_NAME=admin
	export OS_PROJECT_DOMAIN_ID=default
	export OS_USER_DOMAIN_ID=default
	export OS_IDENTITY_API_VERSION=3
	export OS_AUTH_URL=http://localhost/identity
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
	result=`curl -i -s -H "$header" -d "$data" http://$1/identity/v3/auth/tokens`
	token_header=`echo "$result" | grep -Fi X-Subject-Token`
	arr=($token_header)
	export OS_TOKEN=${arr[1]}
}

load_creds
auth $1

