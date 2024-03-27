import os

SourceDirectory = "\\\\.\\F:"
DestinationDirectory = "./Files_Recovered"
Counter = 0

#Create recovery folder in case it doesn't exist
if not os.path.exists(DestinationDirectory):
    os.makedirs(DestinationDirectory)

#Open the directory with read permissions in binary
with open(SourceDirectory, "rb") as Unit:
    while True:
        Data = Unit.read(1024)

        if not Data:
            break

        #set start market to find JPEG images
        StartMarker = Data.find(b"\xff\xd8\xff\xe0\x00\x10")

        while StartMarker != -1:
            EndMarker = Data.find(b"\xff\xd9", StartMarker)

            if EndMarker != -1:
                FileLenght = EndMarker + 2 - StartMarker

                #Save the file found writting in binary
                with open(os.path.join(DestinationDirectory, f"{Counter}.jpg"), "wb") as File:
                    File.write(Data[StartMarker:StartMarker + FileLenght])

                Counter += 1
                StartMarker = Data.find(b"\xff\xd8\xff\xe0\x00\x10", EndMarker + 2)
            else:
                AditionalData = Unit.read(1024)

                if not AditionalData:
                    break

                Data += AditionalData
                continue
