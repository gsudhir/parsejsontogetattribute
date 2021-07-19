#import json library
import json

# This function returns attribute value for a json object and path identified.
def extract_element_from_json(obj, path):
    '''
    Extracts an element from a nested dictionary or
    a list of nested dictionaries along a specified path.
    If the input is a dictionary, a list is returned.
    If the input is a list of dictionary, a list of lists is returned.
    obj - list or dict - input dictionary or list of dictionaries
    path - list - list of strings that form the path to the desired element
    '''
    def extract(obj, path, ind, arr):
        '''
            Extracts an element from a nested dictionary
            along a specified path and returns a list.
            obj - dict - input dictionary
            path - list - list of strings that form the JSON path
            ind - int - starting index
            arr - list - output list
        '''
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                if key in obj.keys():
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr
    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr

# This function parses the data array list returns the attributeValue for a matching word value
def parseInternalJsonList(dataDict,wordValue,attributeVal):
    #replace ]][[ with a ,
    dataDict = dataDict.replace("]][[",",")
    #remove [[
    dataDict = dataDict.replace("[[","[")  
    #remove ]]
    dataDict = dataDict.replace("]]","]")
    #print(dataDict)
    #now make it more json compliant replace single qoutes with double qoutes for the attributes
    dataDict = dataDict.replace("'",'"')
    #print(dataDict)
    dataDict = '{"data":' + dataDict + '}'
    wordDict = json.loads(dataDict)
    #
    for i in range(0,len(wordDict['data'])):
        item = str(wordDict['data'][i])
        item = item.replace("'",'"')
        jsonObj = json.loads(item)
        if jsonObj['word'] == wordValue:
            return jsonObj[attributeVal]

# the below code is primarily used for tesing the logic of the JSON that a words list.
#appDict1 = '''[[{"word": "wow'9", "offset": "PT3.91S", "duration": "PT0.41S", "offsetInTicks": 99100000.0, "durationInTicks": 4100000.0, "confidence": 0.86124074}]][[{"word": "yeah", "offset": "PT1.35S", "duration": "PT0.13S", "offsetInTicks": 13500000.0, "durationInTicks": 1300000.0, "confidence": 0.9814734}, {"word": "wow", "offset": "PT3.91S", "duration": "PT0.41S", "offsetInTicks": 39100000.0, "durationInTicks": 4100000.0, "confidence": 0.7506247}]][[{"word": "oh", "offset": "PT1.43S", "duration": "PT0.02S", "offsetInTicks": 14300000.0, "durationInTicks": 200000.0, "confidence": 0.83614624}, {"word": "wow", "offset": "PT3.91S", "duration": "PT0.41S", "offsetInTicks": 39100000.0, "durationInTicks": 4100000.0, "confidence": 0.955999}]]'''
#print(appDict1)
#appDict1 = appDict1.replace("'","")
#print(appDict1)
#returnVal =  parseInternalJsonList(appDict1,"wow9","offsetInTicks")
#print(returnVal)

# Main program 
# read the file into a string object
file = open("contenturl_0.json",)

RawJson = file.read()
# Closing file
file.close()
# the file will contain specific words with single qoutes, replace them with ""
RawJson = RawJson.replace("'","")
#print(RawJson) 
#Load the object into a dictionary
sampleDict = json.loads(RawJson)
#print(sampleDict)
if 'recognizedPhrases' in sampleDict:
    for nBest in extract_element_from_json(sampleDict, ["recognizedPhrases",'nBest']):
        if "words" in str(nBest):
            for words in  extract_element_from_json(nBest, ['words']):
                #print(words)
                if words:
                    #print(words)
                    attributeValue = parseInternalJsonList(str(words),"peggy","offsetInTicks")
                    if attributeValue:
                        print(attributeValue)
                        break

