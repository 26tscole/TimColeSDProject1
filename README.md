# TimColeSDProject1
## Requirements 
- Pyaudio  
- vosk 0.3.44  
- pytest 8.3.4
- langchain
- langchain-google-genai
- langchain-core

You also need the vosk Model "vosk-model-small-en-us-0.15"

## Secret.txt  
You need to create a secret.txt file in the project root  
This file needs to be formatted in this specific way

API_ADDRESS=<>  
LOGIN_EMAIL=<>  
LOGIN_PASSWORD=<>  
GEMINI_API_KEY=<>  

## Running the code for Sprint2
To run the code for sprint2 you have to go to  
>src/meetingActions/mainMeeting.py

run the if __name__ = "__main__"

- You will be given 5 actions  
- Typing 1 show you all available meetings  
- Typing 2 lets you book a meeting following in terminal instructions  
- Typing 3 shows you your current bookings  
- Typing 4 lets you delete a booking by id number  
- Typing q will end the program

## Running the code for Sprint1
To run the code for sprint1 you have to go to  
>src/conversions/conversionMain.py

run the if __name__ = "__main__"  

- You will be prompted to name the file and in doing so you can then speak to activate Speech To Text
- To end the program say "Stop Recording"
