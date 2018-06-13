openssl genrsa -des3 -out rootCA.key 2048 && openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.pem && touch server.csr.cnf && echo "Input IP address for SSL: " 
read IP && echo "[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn

[dn]
C=PH
ST=State
L=CompanyName
O=Org
OU=Section
emailAddress=email@gemail.com
CN=localhost" >> server.csr.cnf && touch v3.ext && echo "authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
IP.1 = $IP" >> v3.ext && openssl req -new -sha256 -nodes -out server.csr -newkey rsa:2048 -keyout server.key -config <( cat server.csr.cnf ) && openssl x509 -req -in server.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out server.crt -days 500 -sha256 -extfile v3.ext && echo "Finished setup."
