import json

# json object -> Iterator[Tag, Prob]
def getKeywords(data):
    status = data["results"][0]["status_code"]
    if (status == 'OK'):
        tags = data["results"][0]["result"]["tag"]
        return zip(tags["classes"], tags["probs"])
    else:
        print("Warning: Status was not OK")
        return iter(())
