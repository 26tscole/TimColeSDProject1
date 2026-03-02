from agent import buildAIFunctionality, sendAIrequest
from src.AIconnection.userTools import setUsersInstance
from src.setEnviron import loadSecrets
from src.meetIngActions.users import Users
from src.conversion.SpeechToText import audioSource


def main():
    while True:
        loadSecrets()
        user = Users()
        llm = buildAIFunctionality()
        setUsersInstance(user)
        userQuestion = input("ask the AI a question")
        sendAIrequest(llm=llm, userInput=userQuestion)

if __name__ == "__main__":
    main()
