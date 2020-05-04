import json
import random

file_path = 'dev1.0.json'
output = open('results.txt', 'w+')

with open(file_path) as f:
    data = json.load(f)

### TEST DATASET STRUCTURE ###
'''
print("Q1, option 1:  ", data['data'][5]['document']['qas'][0]['answers'][0])
print("Q1, ID:  ", data['data'][5]['document']['qas'][0]['id'])
print("Q1, question:  ", data['data'][5]['document']['qas'][0]['query'])
print("Document Title:  ", data['data'][5]['document']['title'])
print("Passage:  ", data['data'][5]['document']['context'])
print("Source:", data['data'][5]['source'])
'''

### FILE ###
N = len(data['data'])
print("Total = ", N)

#Picking 5 random passages
pass_n = 5
passages = []
for i in range(0, pass_n):
    temp1 = random.randint(0, N-1)
    passages.append(temp1)
print("Chosen Passages:", passages)
for passage in passages:
    print("Passage ", passage)
    output.write("Source:  "+str(data['data'][passage]['source'])+"\n")
    print("Document Title:  ", data['data'][passage]['document']['title'])
    output.write("Document Title:  "+str(data['data'][passage]['document']['title'])+"\n\n")
    print(data['data'][passage]['document']['context']+"\n")
    ques_n = len(data['data'][passage]['document']['qas'])
    print("Questions = ", ques_n)
    questions = []
    for i in range(0, 2):
        temp2 = random.randint(0, ques_n-1)
        questions.append(temp2)
    print("Chosen Questions:", questions)
    for question in questions:
        print("Q:", data['data'][passage]['document']['qas'][question]['query'])
        output.write("Q "+str(question)+": "+str(data['data'][passage]['document']['qas'][question]['query'])+"\n")
        op_n = len(data['data'][passage]['document']['qas'][question]['answers'])
        print("Options = ", op_n)
        for i in range(0, op_n):
            output.write(str(i)+". "+data['data'][passage]['document']['qas'][question]['answers'][i]['text']+"(Origin - "+data['data'][passage]['document']['qas'][question]['answers'][i]['origin']+")\n")
        output.write("\n")
    print("\n\n")
    output.write("\n\n")
output.close()