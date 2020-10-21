import json

if __name__ == '__main__':
    # generate json dict
    dictData = {
        "totalLen": 640,
        "groupLen": 80,
        "coreThre": 0.4,
        "seStep": 3
    }
    out = open("config.json", 'w')
    out.write(json.dumps(dictData, indent=4))
