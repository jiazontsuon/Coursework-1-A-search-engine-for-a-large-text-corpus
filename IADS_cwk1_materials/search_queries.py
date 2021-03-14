
# Inf2-IADS Coursework 1, October 2019
# Python source file: search_queries.py


# PART B: PROCESSING SEARCH QUERIES

import index_build

# We find hits for queries using the index entries for the search terms.
# Since index entries for common words may be large, we don't want to
# process the entire index entry before commencing a search.
# Instead, we process the index entry as a stream of items, each of which
# references an occurrence of the search term.

# For example, the (short) index entry

#    'ABC01,23,DEF004,056,789\n'

# yields a stream which successively yields the items

#    ('ABC',1), ('ABC',23), ('DEF',4), ('DEF',56), ('DEF',789), None, None, ...

# Item streams also support peeking at the next item without advancing.

class ItemStream:
    def __init__(self,entryString):
        self.entryString = entryString
        self.pos = 0
        self.doc = 0
        self.comma = 0
    def updateDoc(self):
        if self.entryString[self.pos].isalpha():
            self.doc = self.entryString[self.pos:self.pos+3]
            self.pos += 3
    def peek(self):
        if self.pos < len(self.entryString):
            self.updateDoc()
            self.comma = self.entryString.find(',',self.pos)
                    # yields -1 if no more commas after pos
            line = int(self.entryString[self.pos:self.comma])
                    # magically works even when comma == -1, thanks to \n
            return (self.doc,line)
        # else return None
    def next(self):
        e = self.peek()
        if self.comma == -1:
            self.pos = len(self.entryString)
        else:
            self.pos = self.comma + 1
        return e


# STUDENT CODE goes here.
class HitStream:
    def __init__(self,itemStreams,lineWindow,minRequired):
        self.itemStreams = itemStreams
        self.current_itemStream =itemStreams[0]
        self.lineW = lineWindow
        self.minReq = minRequired
        self.line =0
        self.doc= 0
        self.idx = 0
        self.history_return = set()
        
    def isQualified(self,hit):
        if (hit[0] !=self.doc):
            return False
        if (hit[1]>=self.line+self.lineW or hit[1]<=self.line-self.lineW):
            return False
        return True
    def meet_minReq(self,hit):
        counter =1
        for i in range(len(self.itemStreams)):
            if (i == self.idx):
                continue
            copy = ItemStream(self.itemStreams[i].entryString)
            while(copy.peek()!=None):
                if (self.isQualified(copy.next())):
                    counter+=1
                    if (counter>=self.minReq):
                        return True
                    break
        return False
    def next(self):
        if (self.idx>=len(self.itemStreams)):
            return None
        self.current_itemStream = self.itemStreams[self.idx]
        while(1):
            
            if (self.current_itemStream.peek() is None):
                self.idx+=1
                if (self.idx>=len(self.itemStreams)):
                    return None
                else:
                    self.current_itemStream = self.itemStreams[self.idx]
            self.doc,self.line = self.current_itemStream.next()
            hit = (self.doc,self.line)
            if (hit in self.history_return):
                continue
            if (self.minReq ==1 or self.meet_minReq(hit)):
                self.history_return.add(hit)
                return hit
            


# Displaying hits as corpus quotations:

import linecache

def displayLines(startref,lineWindow):
    # global CorpusFiles
    if startref is not None:
        doc = startref[0]
        docfile = index_build.CorpusFiles[doc]
        line = startref[1]
        print ((doc + ' ' + str(line)).ljust(16) +
               linecache.getline(docfile,line).strip())
        for i in range(1,lineWindow):
            print (' '*16 + linecache.getline(docfile,line+i).strip())
        print ('')

def displayHits(hitStream,numberOfHits,lineWindow):
    for i in range(0,numberOfHits):
        startref = hitStream.next()
        if startref is None:
            print('-'*16)
            break
        displayLines(startref,lineWindow)
    linecache.clearcache()
    return hitStream


# Putting it all together:

currHitStream = None

currLineWindow = 0

def advancedSearch(keys,lineWindow,minRequired,numberOfHits=5):
    indexEntries = [index_build.indexEntryFor(k) for k in keys]
    if not all(indexEntries):
        message = "Words absent from index:  "
        for i in range(0,len(keys)):
            if indexEntries[i] is None:
                message += (keys[i] + " ")
        print(message + '\n')
    itemStreams = [ItemStream(e) for e in indexEntries if e is not None]
    if len(itemStreams) >= minRequired:
        global currHitStream, currLineWindow
        currHitStream = HitStream (itemStreams,lineWindow,minRequired)
        currLineWindow = lineWindow
        displayHits(currHitStream,numberOfHits,lineWindow)

def easySearch(keys,numberOfHits=5):
    global currHitStream, currLineWindow
    advancedSearch(keys,1,len(keys),numberOfHits)
#change the 3rd argument of advancedSearch from len(keys) to 1

def more(numberOfHits=5):
    global currHitStream, currLineWindow
    displayHits(currHitStream,numberOfHits,currLineWindow)

# End of file

'''if __name__ == "__main__":
    index_build.buildIndex()
    a=index_build.indexEntryFor('abide')
    A= ItemStream(a)
    b = index_build.indexEntryFor('able')
    B = ItemStream(b)
    c= [A,B]
    hs = HitStream(c,1200,2)'''
    
