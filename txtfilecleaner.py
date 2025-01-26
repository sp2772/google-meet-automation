

import re
import nltk
from nltk.corpus import words

# Download necessary NLTK resources
nltk.download('words', quiet=True)
import string

def remove_punctuation(input_string):
    new=input_string
    for i in input_string:
        if i in """!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'""":
            new=new.replace(i,' ')
    return new

def extract_user_names(word_list):
   
    # Get set of English words for comparison
    
    english_words = set(words.words())
    english_words= set([word for word in english_words if len(word)>1])
    english_words.add('okay')
    english_words.add('knows')
    english_words.add('translating')
    english_words.add('a')
    english_words.add('i')
    english_words.remove('sai')
    
    with open("singleletter.txt",'w') as f:
        for word in english_words:
            if len(word)<2:
                f.write(word+'\n')

    print("No. of english words",len(english_words))
    # Function to check if a word is likely a name
    def is_likely_name(word):
        print("word:",word)
        # Remove any non-alphabetic characters
        clean_word = re.sub(r'[^a-zA-Z0-9 ]', ' ', word)
        print("clean_word:",clean_word)
        # Check conditions:
        # 1. Word is not empty after cleaning
        # 2. Not in English words dictionary
        
        yes=''
        flag=0
        clean_list=clean_word.strip().split()
        print("Clean list:",clean_list)
        for word in clean_list:
            new_word=remove_punctuation(word)
            print("Word after removing punctuations:",new_word)
            if new_word.lower() in english_words:
                flag=1
                print(new_word,"in english dict!")
                break
            

            
                
        if flag !=1:
            yes=clean_word
            print("word passed punctuation non english")

        return (clean_word and 
                len(yes)!=0 and
                2 <= len(clean_word) <= 40)
    
    print("User names:")
    for word in word_list:
        if is_likely_name(word):
            print(word)

    # Filter and return likely names
    names = list(set(word for word in word_list if is_likely_name(word)))
    
    return sorted(names)








def remove_duplicate_parts(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    y=0
    processed_lines = []
    i=0
    print("Initial length:",len(lines))
    users=set()
    while i<len(lines):
        if i!=len(lines)-1:
            if lines[i]==lines[i+1]:
                print("removed line:",lines[i])
                lines.remove(lines[i+1])
                print("after removal, no. of lines:",len(lines),", detected redundant line at index:",i)
        i+=1
    
    
    
    for line in lines:
        if len(line.split())<7:
            users.add(line)
    
    print("users:",users)
    user_names=extract_user_names(users)
    user_names.append("You\n")
    print("\npotential user names:",type(user_names))
    i=1
    name_dict={}
    for name in user_names:
        print(i," ",name)
        name_dict[i]=name
        i+=1
    
    numbers=input("Enter invalid user numbers separated by space:")
    num_list=[int(num) for num in numbers.split()]
    for i in num_list:
        user_names.remove(name_dict[i])

    print("Corrected user names:",user_names)

    with open("user_participated.txt",'w') as f:
        for user in user_names:
            f.write(user)

    
    
    i=0
    while i<len(lines):
        if i!=len(lines)-1 and i>2:
            if lines[i] in user_names and lines[i+1] in user_names:
                print("removed line:",lines[i])
                lines.remove(lines[i])
                print("after removal, no. of lines:",len(lines),", detected redundant line at index:",i)
        i+=1
    """
    i=0
    while i<len(lines):
        if i<len(lines)-6:
            print(lines[i])
            flag=0
            j=len(lines[i])-1
            while j>=0:
                for k in range(0,j+1):
                    #print("start line:",lines[i][k:j+1],"next line:",lines[i+1],"next next line:",lines[i+2],sep='\n')
                    if  lines[i+1].startswith(lines[i][k:j+1]) :
                        print("i value:",i, "j value:",j,'k value',k, len(lines))
                        print("matched line:",lines[i][k:j+1])
                        print("Line redundancy found: line1:",lines[i],"\n line2:",lines[i+1])
                        lines[i+1]=lines[i+1].replace(lines[i][k:j+1],'')
                        flag=1
                        
                    if lines[i+2].startswith(lines[i][k:j+1]) :
                        print("i value:",i, "j value:",j,'k value',k, len(lines))
                        print("matched line:",lines[i][k:j+1])
                        print("Line redundancy found: line1:",lines[i],"\n line2:",lines[i+2])
                        lines[i+2]=lines[i+2].replace(lines[i][k:j+1],'')
                        flag=1
                    if  lines[i+3].startswith(lines[i][k:j+1]) :
                        print("i value:",i, "j value:",j,'k value',k, len(lines))
                        print("matched line:",lines[i][k:j+1])
                        print("Line redundancy found: line1:",lines[i],"\n line2:",lines[i+3])
                        lines[i+3]=lines[i+3].replace(lines[i][k:j+1],'')
                        flag=1
                        
                    if lines[i+4].startswith(lines[i][k:j+1]) :
                        print("i value:",i, "j value:",j,'k value',k, len(lines))
                        print("matched line:",lines[i][k:j+1])
                        print("Line redundancy found: line1:",lines[i],"\n line2:",lines[i+4])
                        lines[i+4]=lines[i+4].replace(lines[i][k:j+1],'')
                        flag=1
                    
                    if flag==1:
                        break
                if flag==1:
                    break
                j-=1
                    
            
        i+=1
        """
    processed_lines=lines
        
    # Write to output file
    with open(output_file, 'w') as f:
        f.writelines(processed_lines)

# Example usage
input_file = 'salvo_induction.txt'
output_file = 'output_salvo.txt'
remove_duplicate_parts(input_file, output_file)
#remove_duplicate_parts(output_file,"output_salvo2.txt")

print(f"Processed file saved to {output_file}")
