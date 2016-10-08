import json
import numpy as np

# json object -> Iterator[Tag, Prob]
def getKeywords(data):
    status = data["results"][0]["status_code"]
    if (status == 'OK'):
        tags = data["results"][0]["result"]["tag"]
        return (set(tags["classes"]), dict(zip(tags["classes"], tags["probs"]))
    else:
        print("Warning: Status was not OK")
        return iter(())

# List[Json] -> Map[Key, (Mean, Std)]
def calculate(queue):
    eps = 5;
    intersectKeys = {} # This is incorrect
    if(queue.size() > eps):
        mapped = map(getKeywords,queue.toList()
        intersectKeys = reduce(lambda x, y: (x[0] & y[0]), mapped)
        probsDict = map(lambda k: (k,np.array([l[1][k] for l in mapped])), intersectKeys)
        queue.pop()
        return dict(map(lambda k: (k[0], (np.mean(k[1]), np.std(k[1]))),probsDict))
    else
        return None

def top():
    global queue
    global statResult
    while(True):
        res = calculate(queue)
        if(res != None):
            statResult.push(res)            
        time.sleep(0.05)
