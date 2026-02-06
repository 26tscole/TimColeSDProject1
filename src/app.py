from conversion.SpeechToText import audioConversion

if __name__ == "__main__":
    #for choosing file names i dont think its a good idea to have spaces so i took away the option
    chosenName = input("Enter File Name To Continue (Do not include file Extension): ")
    print("To stop recording say 'stop recording'")
    fileName = (chosenName.replace(" ", "_")+".txt")
    audioConversion(txtFileName=fileName)

