import os, openai
from time import sleep

openai.api_key = '' # Add OpenAI API Key

RHOST = "10.0.0.210"
LHOST = "10.0.0.56"

pretext = f'You are operating as penetration tester attempting to obtain access to a system at the IP address of 
{RHOST}, and are testing from a Kali linux system at {LHOST} on the same local network as the target system. Provide 
commands that will be executed in the Kali linux terminal after "Command: ", and then I will provide responses from 
those commands back to you after "Response: ". Try to avoid using interactive commands like nc, netcat, telnet, 
msfconsole, etc.'

initial_msg = f"Command: ```nmap -sV {RHOST}```"

convo = [{"role": "system", "content": pretext},
         {"role": "assistant", "content": initial_msg}]

# Convo Start
command = initial_msg
stdin = initial_msg.split('```')[1]
print(f'\n\n{initial_msg}')
result = os.popen(stdin).read()
reply = f'Response: {result}'
print(f'\n\Response: ```{result}```')
convo.append({"role": "user", "content": reply})

while True:
    sleep(5)
    r = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=convo)
    command = r['choices'][0]['message']['content']
    stdin = command.split('```')[1]
    convo.append({"role": "assistant", "content": command})
    print(f'\n\n{command}')
    result = os.popen(stdin).read()
    reply = f'Response: {result}'
    print(reply)
    convo.append({"role": "user", "content": reply})

