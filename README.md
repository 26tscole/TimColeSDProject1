# TimColeSDProject1

***

## Requirements 
- Pyaudio  
- vosk 0.3.44  
- pytest 8.3.4
- langchain
- langchain-google-genai
- langchain-core
- nicegui

You also need the vosk Model "vosk-model-small-en-us-0.15"

## Secret.txt  
You need to create a secret.txt file in the project root  
This file needs to be formatted in this specific way

API_ADDRESS=<api_address>  
LOGIN_EMAIL=<login_email>  
LOGIN_PASSWORD=<login_password>  
GEMINI_API_KEY=<gemini_api_key>  

---
___

## Running the code for Sprint4
To run the sprint4 code you have to go to  
>src/editDB/GUI/main.py  

run the if __name__ = "__main__"

### Instructions

- After running the code you will be directed to a localHost webpage
- Here you will have the options to
  - Delete a Room
    - For deleting a room you need to insert the roomId you want to delete
    - After deleting a room if that room has any reservations a csv file will be created with all deleted rooms
  - Add a room
    - For Adding a room you need to give a room name and capacity for that room
  - Change a rooms Capacity
    - To change the rooms Capacity you have to enter the roomId and new Capacity
- For all of these functions the submit button will allow you to save the changes

### Things to Note

- The secrets.txt file needs to be setup in the exact way explained above
- My server droplet is -> Tcole-ubuntu-s-1vcpu-512mb-10gb-nyc3-01
- On this droplet I changed the way the delete works using Claude Code
- I used the same email and password in my server that was given to me on blackboard
- Last thing to note, there is no easy way to stop this code from running other than forcing it stop using the IDE

---
___

## Running the code for Sprint3
To run the sprint3 code you have to go to  
>src/AIconnections/AIMain  

run the if __name__ = "__main__"

### Instructions

- Wait until vosk fully loads, this happens when all the debug prompts stop appearing  
- After this ask talk to through you microphone and ask the agent a question
- When you finish your message wait for it to show up in the terminal and then say "Send Message"
- This will prompt the AI to search for the data you requested using the tools
- After the requested data shows up in the terminal you are free to ask another question
- You can use the all the commands below during the session

### Things to Note

- Iterations will appear in the console as a way to check if the code is actually running
- Sometimes the AI responses will take a significant amount of time to run iterations after the first
- The longest its taken me to get a response from the AI is 35 seconds although this is not the even close to the average time
- This project uses the latest version of Gemini so make sure the api key being used is compatible 
- The console gets a little clogged so you will have to scroll up in the console to get to the message and data the AI responds with 

>Commands
> - "Stop Chat" → ends current session
> - "Reset" → deletes current request and starts a new one
> - "Send Message" → gives the AI the current message you have for it

---
___

## Running the code for Sprint2
To run the code for sprint2 you have to go to  
>src/meetingActions/mainMeeting.py

run the if __name__ = "__main__"

### Instructions

- You will be given 5 actions  
- Typing 1 show you all available meetings  
- Typing 2 lets you book a meeting following in terminal instructions  
- Typing 3 shows you your current bookings  
- Typing 4 lets you delete a booking by id number  
- Typing q will end the program

---
___

## Running the code for Sprint1
To run the code for sprint1 you have to go to  
>src/conversions/conversionMain.py

run the if __name__ = "__main__"  

### Instructions

- You will be prompted to name the file and in doing so you can then speak to activate Speech To Text
- To end the program say "Stop Recording"
