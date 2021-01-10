import requests
def NiuBi(atname):
    rest = requests.get("https://el-bot-api.vercel.app/api/words/niubi")
    rest_text = rest.text
    result =  rest_text.replace("${name}",atname)
    return result[2:-2]

