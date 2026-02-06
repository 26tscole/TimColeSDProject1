from conversion.SpeechToText import audioSource

if __name__ == "__main__":
    #for choosing file names i dont think its a good idea to have spaces so i took away the option
    chosenName = input("Enter File Name To Continue (Do not include file Extension): ")
    print("To stop recording say 'stop recording'")
    # this may be an issue
    if chosenName == "":
        audioSource()
    else:
        fileName = (chosenName.replace(" ", "_")+".txt")
        audioSource(txtFileName=fileName)

