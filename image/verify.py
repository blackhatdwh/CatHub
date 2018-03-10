#!/usr/bin/env python3
import subprocess
import json
import sys

def verify_image(url):
    command = 'curl -s -H "Content-Type: application/json" https://vision.googleapis.com/v1/images:annotate?key=AIzaSyC2F-NrDgXR530blIxYzTcdQm-P8vDNErs --data-binary \'{ "requests": [ { "image": { "source": { "imageUri": "%s" } }, "features": [ { "type": "LABEL_DETECTION", }, { "type": "SAFE_SEARCH_DETECTION", } ] } ] }\'' % url
    result = subprocess.getoutput(command)
    result = json.loads(result)
    if result['responses'][0]['safeSearchAnnotation']['adult'] in ['LIKELY', 'VERY_LIKELY']:
        return -1
    label = []
    keyword = ['cat', 'kitten', 'mammal', 'cat like mammal', 'vertebrate']
    for i in result['responses'][0]['labelAnnotations']:
        label.append(i['description'])
    if any(i in keyword for i in label):
        return 0
    else:
        return -2

if __name__ == '__main__':
    print(verify_image(sys.argv[1]))
