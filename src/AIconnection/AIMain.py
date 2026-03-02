from agent import buildAIFunctionality, sendAIrequest
from src.AIconnection.userTools import setUsersInstance
from src.setEnviron import loadSecrets
from src.meetIngActions.users import Users




if __name__ == "__main__":
    loadSecrets()
    user = Users()
    llm = buildAIFunctionality()
    setUsersInstance(user)
    sendAIrequest(llm=llm, userInput="Show me all the bookings I have made in total")
