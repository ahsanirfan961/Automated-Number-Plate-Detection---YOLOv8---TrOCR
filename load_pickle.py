#LOAD A PICKLE FILE INTO A LIST
import pickle
processed_frame=[]
with open('list.pkl', 'rb') as file:
    processed_frame = pickle.load(file)
print(len(processed_frame))    
    