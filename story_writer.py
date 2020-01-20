import utilities

BAD_CHARS=utilities.BAD_CHARS
VALID_PUNCTUATION=utilities.VALID_PUNCTUATION
END_OF_SENTENCE_PUNCTUATION=utilities.END_OF_SENTENCE_PUNCTUATION
ALWAYS_CAPITALIZE = utilities.ALWAYS_CAPITALIZE

def parse_story(file_name):
    """
    (string) -> list
    returns a parsed list of words and characters given the name of a text file.
    >>>parse_story('test_text_parsing.txt')
    ['the', 'code', 'should', 'handle', 'correctly', 'the', 'following', ':', 'white', 'space', '.', 'sequences', 'of', 'punctuation', 'marks', '?', '!', '!', 'periods', 'with', 'or', 'without', 'spaces', ':', 'a', '.', '.', 'a', '.', 'a', "don't", 'worry', 'about', 'numbers', 'like', '1', '.', '5', 'remove', 'capitalization']
    """
    file=open(file_name, 'r')
    content=file.read()
    
    content=content.replace('\n',' ')
    
    for i in range(len(BAD_CHARS)):
        content=content.replace(BAD_CHARS[i],' ')
    content=content.lower()
    word_list=[]
    word=''
    length = len(content)
    for i in range(length):
        
        if(content[i]!=' ' and not(content[i] in VALID_PUNCTUATION)):
            word=word+content[i]
            
        else:
            if(word!=''):
                word_list.append(word)
                word=''
        
        if content[i] in VALID_PUNCTUATION:
            word_list.append(content[i])        
            
    return word_list

def get_prob_from_count(counts):
    """
    (list) -> list
    returns a list of probabilities given a list of counts of occurances of an ngram after a specific ngram.
    >>> get_prob_from_count([10, 20, 40, 30])
    [0.1, 0.2, 0.4, 0,3]
    >>> get_prob_from_count([5, 5, 5, 5])
    [0.25, 0.25, 0.25, 0.25]
    """
    length=len(counts)
    sum=0
    for i in range(length):
        sum=sum+counts[i]
    probs=[]
    for i in range(length):
        probs.append(counts[i]/sum)
    return probs


def build_ngram_counts(words,n):
    """
    (list, number) -> dictionary
    returns a dictionary with ngrams of length n as keys and all the words which occur after the ngram as a list as the value for the key.
    >>>words=[the’, ‘child’, ‘will’, ‘go’, ‘out’, ‘to’, ‘play’, ‘,’, ‘and’, ‘the’, ‘child’, ‘can’, ‘not’, ‘be’, ‘sad’, ‘anymore’, ‘.’]
    >>>build_ngram_count(words,2)
    {(‘the’, ‘child’): [[‘will’, ‘can’], [1, 1]],(‘child’, ‘will’): [[‘go’], [1]], (‘will’, ‘go’): [[‘out’], [1]], (‘go’, out’): [[‘to’], [1]],(‘out’, ‘to’): [[‘play’], [1]], (‘to’, ‘play’): [[‘,’], [1]], (‘play’, ‘,’): [[‘and’], [1]], (‘,’, ‘and’): [[‘the’], [1]], (‘and’, ‘the’): [[‘child’], [1]], (‘child’, ‘can’): [[‘not’], [1]], (‘can’, ‘not’): [[‘be’], [1]], (‘not’, ‘be’): [[‘sad’], [1]], (‘be’, ‘sad’): [[‘anymore’],[1]],(‘sad’, ‘anymore’): [[‘.’], [1]]}
    """
    dictionary={}
    for i in range(len(words)-n):
        key=[]
        for j in range(n):
            key.append(words[i+j])
        key_tuple=tuple(key)   
        newkey = {key_tuple : [[],[]]}
        dictionary.update(newkey)
        
    for i in range(len(words)-n):
        key=[]
        for j in range(n):
            key.append(words[i+j])
        key_tuple=tuple(key)   
        
        
        next_word=words[i+n]
        
        if next_word not in dictionary[key_tuple][0]:
            dictionary[key_tuple][0].append(next_word)
            dictionary[key_tuple][1].append(1)
        else:
            
            for k in range(len(dictionary[key_tuple][0])):
                
                if dictionary[key_tuple][0][k] == next_word:
                    dictionary[key_tuple][1][k]=dictionary[key_tuple][1][k]+1
                    
    return dictionary
                           
def prune_ngram_counts(counts, prune_len):
    """
    (dictionary, number) -> dictionary
    returns a dictionary of ngrams with lower frequency words removed. 
    >>> ngram_counts= {(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’, ‘no’], [20, 20, 10, 2]],(‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]],('toronto’, ‘is’): [[‘six’, ‘drake’], [2, 3]]}
    >>> prune_ngram_counts(ngram_counts, 3)
    {(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [20, 20, 10]],(‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]],('toronto’, ‘is’): [[‘six’, ‘drake’],[2, 3]]}
    """
    pruned={}
    for ngrams,count_list in counts.items():
        
        length=len(count_list[0])  
        #sorts both lists
        for i in range(length):
            for j in range(0,length-1-i):
                if(count_list[1][j]<count_list[1][j+1]):
                    count_list[1][j], count_list[1][j+1] = count_list[1][j+1], count_list[1][j]
                    count_list[0][j], count_list[0][j+1] = count_list[0][j+1], count_list[0][j]
        #            
        
       
        
        if prune_len < length and count_list[1][prune_len]==count_list[1][prune_len-1]:
            count_list[1]=count_list[1][:prune_len+1]
            count_list[0]=count_list[0][:prune_len+1]
           
        else:
            count_list[1]=count_list[1][:prune_len]
            count_list[0]=count_list[0][:prune_len]
         
        pruned[ngrams]=count_list
        
        
    return pruned
 
def probify_ngram_counts(counts):
    """
    (dictionary) -> dictionary 
    takes a dictionary of ngrams and counts, and converts the counts into probabilities.
    >>>ngram_counts = {(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [20, 20, 10]],(‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]],('toronto’, ‘is’): [[‘six’, ‘drake’], [2, 3]]}
    >>>probify_ngram_counts(ngram_counts)
    {(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [0.4, 0.4, 0.2]],(‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [0.32, 0.28, 0.2, 0.2]],('toronto’, ‘is’): [[‘six’, ‘drake’], [0.4, 0.6]]}
    """

    probified={}
    
        
            
    for ngrams,count_list in counts.items(): 
        
        length=len(count_list[1])
               
        for i in range(length):           
            count_list[1]=get_prob_from_counts(count_list[1]) 
        probified[ngrams]=count_list
        
    return probified
            
def build_ngram_model(words,n):
    """
    (list, number) -> dictionary
    takes a list of words generated using parse_story and converts it to a dictionary of ngrams of length n, keeping the 15 most likely words to follow an ngram in descending order.
    >>>words = [‘the’, ‘child’, ‘will’, ‘the’, ‘child’, ‘can’, ‘the’, ‘child’, ‘will’, ‘the’, ‘child’, ‘may’,‘go’, ‘home’, ‘.’]
    >>> build_ngram_model(words, 2)
    {(‘the’, ‘child’): [[‘will’, ‘can’, ‘may’], [0.5, 0.25, 0.25]],(‘child’, ‘will’): [[‘the’], [1.0]],(‘will’, ‘the’): [[‘child’],[1.0]],(‘child’, ‘can’): [[‘the’], [1.0]],(‘can’, ‘the’): [[‘child’], [1.0]],(‘child’, ‘may’): [[‘go’], [1.0]],(‘may’, ‘go’): [[‘home’], [1.0]],(‘go’, ‘home’): [[‘.’], [1.0]]}
    """
    lol=build_ngram_counts(words,n)
    lol=prune_ngram_counts(lol,15)
    lol=probify_ngram_counts(lol)
    return lol

def gen_bot_list(ngram_model, seed,  num_tokens=0):
    """
    (dictionary, tuple, number) -> list
    converts an ngram model generated by the build_ngram_model function and random generates a list of tokens starting with the tokens found in the seed.
    >>>ngram_model = {('the', 'child'): [['will', 'can','may'], [0.5, 0.25, 0.25]], ('child', 'will'): [['the'], [1.0]], ('will', 'the'): [['child'], [1.0]], ('child', 'can'): [['the'], [1.0]], ('can', 'the'): [['child'], [1.0]], ('child', 'may'): [['go'], [1.0]], ('may', 'go'): [['home'], [1.0]], ('go', 'home'): [['.'], [1.0]] }
    >>> random.seed(10)
    >>> gen_bot_list(ngram_model, ('hello', 'world'))
    []
    >>>gen_bot_list(ngram_model, ('the', 'child'), 5)
    ['the', 'child', 'will', 'the', 'child']
    """
    print(seed)
    seed=list(seed)
    
    tokens=[]
    
    for i in range(len(seed)):
        if len(tokens)<num_tokens:
            tokens.append(seed[i])
            
            
    check=False
    for key in ngram_model:            
        if(seed==list(key)):
            check=True
            
    while len(tokens)<num_tokens and check:
        check=False
        for key in ngram_model:            
            if(seed==list(key)):
                check=True
                
        new = utilities.gen_next_token(tuple(seed), ngram_model)
       
        new_seed=[]
        for j in range(1,len(seed)):
            new_seed.append(seed[i])
            
        
        
        new_seed.append(new)
        seed=new_seed
        
        tokens.append(new)
        check=False
        for key in ngram_model:            
            if(seed==list(key)):
                check=True  
                
    return tokens   

def gen_bot_text(token_list, bad_author):
    """
    (list, boolean) -> string
    Takes a list of tokens and converts it to a string. If bad author is True, then all tokens are seperated by space. If bad author is False, then the string will have proper sentence structure.
    >>> token_list= ['this', 'is', 'a', 'string', 'of', 'text', '.', 'which', 'needs', 'to', 'be', 'created', '.']
    >>> gen_bot_text(token_list, False)
    'This is a string of text. Which needs to be created.'
    >>> gen_bot_text(token_list, True)
    'this is a string of text . which needs to be created .'
    """
    
    caps=[]
    for i in range(len(ALWAYS_CAPITALIZE)):
        ALWAYS_CAPITALIZE[i]=ALWAYS_CAPITALIZE[i].lower()
        caps=ALWAYS_CAPITALIZE
    if token_list==[]:
        return ''
    if bad_author:
        text=''
        for i in range(len(token_list)):
            text=text+token_list[i]+' ' 
        
        return text.rstrip()
    else:
        sentence_start=True
        text=''
        for i in range(0, len(token_list)):
            if sentence_start:
                if(token_list[i] in ['.', '!', '?']):
                    text=text+ token_list[i]
                elif(token_list[i] in [',', ':', ';']):
                    text=text+ token_list[i]
                    sentence_start=False
                else:
                    text=text+' ' +token_list[i].lower().capitalize()
                    sentence_start=False
            elif token_list[i] in ['.', '!', '?']:#ends sentence
                text=text+token_list[i]
                
                sentence_start=True
            elif token_list[i].lower() in caps:#in always caps?
                
                text=text+' ' +token_list[i].lower().capitalize()
            elif token_list[i] in [',' , ':' , ';']:
                text=text+token_list[i] 
            else:
                text=text+' ' + token_list[i]
        
        if text[len(text)-1]== ' ':
          
            text=text.rstrip()
        if text[0]==' ':
            text=text.lstrip()
            
        return text

def write_story(file_name, text, title, student_name, author, year):
    """
    (string, string string, string, string, number) -> string
    Converts a text into story format. Creates a title page with the title, student name, author and year. The text is formated such that there are maximum 90 characters in a line, maximum 30 lines per page,
    and maximum 12 pages per chapter.
    """
    #title page
    text=text
    new_text='\n\n\n\n\n\n\n\n\n\n'
    new_text=new_text+title+': '+ str(year) +', UNLEASHED'
    new_text=new_text+'\n'+student_name+', inspired by ' + author
    new_text=new_text+'\nCopyright year published (' + str(year) +'), publisher: EngSci press'
    new_text=new_text+'\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
    new_text=new_text+ 'CHAPTER 1\n\n'
    line_count=2
    page_count=0
    page_count_12=0
    chapter=1
    while len(text)>90:
        line=''
        for i in range(90):
            line = line +text[i]
                
        text=text[90:len(text)]
        
        if text[0] == ' ':
            text=text.lstrip()
            
        else:
            i=89
            while line[i] != ' ':
                text = line[i] +text
                line = line[0:i]
                i=i-1
                
        if line[len(line)-1]==' ':
            line=line.rstrip()        
        new_text=new_text+line+'\n' 
            
        
        
        line_count+=1
       
        if(line_count == 28):
            line_count=0
            page_count+=1
            page_count_12+=1
            new_text=new_text+ '\n' + str(page_count) + '\n'
             
        if(page_count_12 ==12):
            page_count_12=0
            chapter+=1
            new_text=new_text + 'CHAPTER ' +str(chapter) +'\n\n'
            line_count=2
            
        
            
    new_text=new_text+text
    line_count+=1
    lol=28-line_count+1
    new_text=new_text+'\n'*lol
    new_text=new_text+ '\n' + str(page_count+1)
    myfile=open(file_name, 'w')
    myfile.write(new_text)
    myfile.close()
    

    
            
               
if (__name__ == "__main__"):
    print("hello")