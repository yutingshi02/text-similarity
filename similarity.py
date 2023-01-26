#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 16:52:44 2022

@author: yutingshi, pair working with Lucia Godinez
"""

import math 

def clean_text(txt):
    """
    that takes a string of text txt returns a list containing the words in txt 
    after it has it's punctuation and special symbols removed 
    and all letters are lowercase  split the text into a list of words 
    """
    txt=txt.lower()
    newstring=''
    for c in txt:
        if c in """.,?"'!;:""":
            newstring += ' '
        else:
            newstring += str(c)        
    splitstring=newstring.split()
    return splitstring   
           

def stem(s):
    """
    accepts a string as a parameter. The function should then return the stem of s
    """
    if len(s) == 3:
        return s
    if s[-1] == 's':
        s = s[:-1] 
        if len(s) <= 1:
            return s
    if s[-1] == 'e':
        s = s[:-1]   
    if s[-1] == 'y':
        s = s[:-1] + 'i'
    if s[-3:] == 'ing': 
        if len(s) >= 5:
            if s[-4] == s[-5]: 
                if s[-4] in 'l':
                    s = s[:-3]
                else:
                    s = s[:-4]
        else:
            s = s
    if s[-2:] == 'er' or s[-2:] == 'ly' or s[-2:] == 'ed':
        if len(s) >= 4:
            if s[-3] == s[-4]: 
                if s[-3] in 'l':
                    s = s[:-2] 
                else:
                    s = s[:-3]
            else:
                s = s[:-2]    
    return s


def compare_dictionaries(d1, d2):
    """
    takes two feature dictionaries d1 and d2 as inputs
    return their log similarity score
    """
    if d1 == {}:
        return -50
    score = 0 
    total = 0 
    for word in d1:
        total += d1[word]
    for words in d2:
        if words in d1:
            score += (d2[words]) * math.log(d1[words]/total)
        else: 
            score += (d2[words]) * math.log(0.5/total)
    return score

                     
class TextModel: 
    """
    class of objects that creates the dictionaries of words from a text file
    """
    def __init__(self, model_name):
        """
        constructs an object of TextModel
        name – a string that is a label for this text model such as author name
        words – a dictionary that records the number of times each word appears in the text
        word_lengths – a dictionary that records the number of times each word length appears
        """ 
        self.name = model_name
        self.words = {}  # num of times word appears
        self.word_lengths = {}  # num of lengths of words appears 
        self.stems = {} # num of times each stem appears
        self.sentence_lengths = {} # records the num of times each sentence length
        self.conjunctions = {} # records num of appearances of 7 main conjunctions
        
    def __repr__(self):
        """
        returns a string that includes the name of the model 
        as well as the sizes of the dictionaries for each feature of the text
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of conjunction words: ' + str(len(self.conjunctions)) + '\n'
        return s 
    
    def add_string(self, s):
        """
        adds a string of text s to the model by augmenting the feature 
        dictionaries defined in the constructor
        does not return anything
        """
        new = s.replace('!', '.').replace('?', '.')
        newlist = new.split('.')
        for sentence in newlist:
            scount = 0
            newsentence = sentence.split()
            scount = len(newsentence) 
            if scount == 0:
                scount = scount
            elif scount not in self.sentence_lengths:
                self.sentence_lengths[scount] = 1 
            else: 
                self.sentence_lengths[scount] += 1 

        word_list = clean_text(s)
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else: 
                self.words[w] += 1
                
            lengthword = len(w)
            if lengthword not in self.word_lengths:
                self.word_lengths[lengthword] = 1 
            else: 
                self.word_lengths[lengthword] += 1 
            
            stemword = stem(w)
            if stemword not in self.stems:
                 self.stems[stemword] = 1
            else: 
                 self.stems[stemword] += 1     
            
            if w == 'and' or w == 'or' or w == 'but' or w == 'for' or w == 'nor' or w == 'so' or w == 'yet':
                if w not in self.conjunctions:
                  self.conjunctions[w] = 1
                else: 
                  self.conjunctions[w] += 1   
                
    def add_file(self, filename):
        """
        adds all of the text in the file identified by filename to the model
        does not return anything
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        file = f.read()
        self.add_string(file) 
        f.close()
        
    def save_model(self):
        """
        saves the TextModel object self by writing its various 
        feature dictionaries to files,
        one file for self.words (1) and another for self.word_lengths (2)
        """ 
        dictionary1 = self.words  
        filename1 = str(self.name) + '_words'
        f1 = open(filename1, 'w')     
        f1.write(str(dictionary1))             
        f1.close()  
        
        dictionary2 = self.word_lengths 
        filename2 = str(self.name) + '_word_lengths'
        f2 = open(filename2, 'w')     
        f2.write(str(dictionary2))             
        f2.close() 
        
        dictionary3 = self.stems
        filename3 = str(self.name) + '_stems'
        f3 = open(filename3, 'w')     
        f3.write(str(dictionary3))             
        f3.close() 
        
        dictionary4 = self.sentence_lengths
        filename4 = str(self.name) + '_sentence_lengths'
        f4 = open(filename4, 'w')     
        f4.write(str(dictionary4))             
        f4.close() 
        
        dictionary5 = self.conjunctions
        filename5 = str(self.name) + '_conjunctions'
        f5 = open(filename5, 'w')     
        f5.write(str(dictionary5))             
        f5.close() 
        
    def read_model(self):
        """
        reads the stored dictionaries for the called TextModel object 
        from their files and assigns them to the attributes 
        of the called TextModel
        """
        filename1 = str(self.name) + '_words'
        f1 = open(filename1, 'r')  
        d1_str = f1.read()         
        f1.close()
        d1 = dict(eval(d1_str))
        self.words = d1
        
        filename2 = str(self.name) + '_word_lengths'
        f2 = open(filename2, 'r')  
        d2_str = f2.read()         
        f2.close()
        d2 = dict(eval(d2_str)) 
        self.word_lengths = d2
        
        filename3 = str(self.name) + '_stems'
        f3 = open(filename3, 'r')  
        d3_str = f3.read()         
        f3.close()
        d3 = dict(eval(d3_str)) 
        self.stems = d3
        
        filename4 = str(self.name) + '_sentence_lengths'
        f4 = open(filename4, 'r')  
        d4_str = f4.read()         
        f4.close()
        d4 = dict(eval(d4_str)) 
        self.sentence_lengths = d4
        
        filename5 = str(self.name) + '_conjunctions'
        f5 = open(filename5, 'r')  
        d5_str = f5.read()         
        f5.close()
        d5 = dict(eval(d5_str)) 
        self.conjunctions = d5
        
    def similarity_scores(self, other):
        """
        computes and returns a list of log similarity scores measuring 
        the similarity of self and other
        one score for each type of feature: 
            words, word lengths, stems, sentence lengths
        """
        scores_list = []
        word_score = compare_dictionaries(other.words, self.words)
        scores_list += [word_score]
        word_length_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        scores_list += [word_length_score]
        stem_score = compare_dictionaries(other.stems, self.stems)
        scores_list += [stem_score]
        sentence_length_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        scores_list += [sentence_length_score]
        conjunction_score = compare_dictionaries(other.conjunctions, self.conjunctions)
        scores_list += [conjunction_score]
        return scores_list
        
    def classify(self, source1, source2):
        """
        compares the called TextModel object (self) 
        to two other “source” TextModel objects (source1 and source2)
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print("scores for", source1.name + ":", scores1)
        print("scores for", source2.name + ":", scores2)
        count1 = 0 
        count2 = 0 
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                count1 += 1
            if scores2[i] > scores1[i]:
                count2 += 1
        if count1 > count2: 
            print(self.name, 'is more likely to have come from', source1.name)
        elif count2 > count1:
            print(self.name, 'is more likely to have come from', source2.name)
        else: 
            print(self.name, ' could have come from either source.')
            

def run_tests():
    """ test code, with names of our articles/files"""
    source1 = TextModel('CNN')
    source1.add_file('CNNarticle.txt')

    source2 = TextModel('Washington Post')
    source2.add_file('washingtonposttrumptwitter.txt')
    
    print('Onion Elon Christmas Article')
    new1 = TextModel('Onion 1')
    new1.add_file('elonchristmasarticle.txt')
    new1.classify(source1, source2)
    
    print()
    print('Onion Economic Article: ')
    
    new2 = TextModel('Onion 2')
    new2.add_file('economicarticle.txt')
    new2.classify(source1, source2) 
    
    print()
    print('NBC Twitter Article:')
    
    new3 = TextModel('NBC')
    new3.add_file('nbcnews.txt')
    new3.classify(source1, source2) 
    
    print()
    print('TMZ Twitter Article')
    
    new4 = TextModel('TMZ')
    new4.add_file('tmz.txt')
    new4.classify(source1, source2) 
    
    
    
    

        
        
        
        
        
        

        


                
        
                

            
        
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    