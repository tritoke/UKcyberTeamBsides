# Challenge Document


### Version: `1.0.0`
### Long Title: Mutually Assured Security
### Short Title: TBC
### Author: Nicholas Gregory
### Date: 05/08/2025
### Difficulty: Easy
### Learning objective: To demonstrate mTLS and certificate exploitation


## Challenge Brief (as its to be written in RIO):

You are a security engineer at a company that is building an API with mTLS to secure its internal services.
You have been tasked with investigating and finding vulnerabilities in the mTLS implementation.

You have been provided the Nginx configuration of the target service. A web UI with more information is available
at https://cpp.bootupctf.net:8092

Task 1:
 - Get to know the API, and succesfully authenticate against the target service `/user` endpoint using a valid certificate.
 - HINT: None

Task 2:
 - Find a way to authenticate against the target service `/admin` endpoint using a valid certificate.
 - HINT: The comments in the frontend indicate an alternative service, have you tried using that?

Task 3:
 - Find a way to authenticate against the target service `/advanced` endpoint using a valid certificate.
 - HINT: None

## Solve:

`./solve.sh`

tl;dr:

1. Hit `$PROD_PKI_URL/issue?username=user` to get a user certificate. 
2. `curl -k --cert user_cert.pem --key user_cert.pem $NGINX_URL/user` to authenticate against the target service `/user` endpoint using a valid certificate. (part 1)
3. Hit `$DEV_PKI_URL/issue?username=admin` to get an admin certificate.
4. `curl -k --cert admin_cert.pem --key admin_cert.pem $NGINX_URL/admin` to authenticate against the target service `/admin` endpoint using a valid certificate. This is mistrust on the prod Nginx supporting the dev CA. (part 2)
5. Hit `$DEV_PK_URL/issue-ca?username=attacker` to get the intermediate CA. Generate a CSR and sign it with the intermediate CA. Send the combined chained cert to the `/advanced` endpoint to get the advanced flag. (part 3)



## Author Notes: 

This challenge is designed to give a basic understanding of mTLS misconfiguration.


## Debrief: 



## Hints: 

- For part 2: "What was that about the dev PKI service?"
- For part 3: "Certificate chaining might help"
