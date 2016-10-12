#from models import Page, 
import nltk
import re
from nltk.corpus import wordnet
#from django.http import JsonResponse

def simple(request):
	query=request
	#query = request.GET.get('q',"")
	name = query.strip()
	temp=name
	#print "Label 1"
	tagset=nltk.pos_tag(nltk.word_tokenize(temp))
	length=len(nltk.word_tokenize(temp))
	#print "Label 2"
	nouns=[]
	verbs=[]
	#first POS Tag the query and pull out nouns and verbs. Adjectives and Adverbs can be ignored here as they don't add too much information
	#standard Regex Matching to POS tags
	for tag in tagset:
		if re.match('NN*', tag[1]):
			nouns.append(tag[0])
		if re.match('VB*', tag[1]):
			verbs.append(tag[0])
	limit=2
	for n in nouns:
		print "\n",n
		#print "Label 3"
		syn=wordnet.synsets(n)#returns a list of synsets each of which contains a different meaning of the noun
		#print "Label 4"
		#This first wordnet operation creates a pause. Maybe it'll be fine in our server as the first link would have been made already no?
		print "Hypernyms : "
		k=0
		for a in syn:
			k=k+1
			if k>limit:
				break
			print " ",a.hypernyms()#each item on the list of synsets i.e. each different meaning of the noun contains a set of hypernyms
		print "Hyponyms : "
		k=0
		for a in syn:
			k=k+1
			if k>limit:
				break
			print " ",a.hyponyms()#same but hyponyms 
		print "Synonyms : "
		k=0 
		for a in syn:
			k=k+1
			if k>limit:
				break
			print a.name()
			for lemma in a.lemmas():
				print " ", lemma.name()
	for v in verbs:
		print "\n",v
		syn=wordnet.synsets(v)
		k=0
		print "Hypernyms : "
		for a in syn:
			k=k+1
			if k>limit:
				break
			print " ",a.hypernyms()
		print "Hyponyms : "
		k=0
		for a in syn:
			k=k+1
			if k>limit:
				break
			print " ",a.hyponyms()
		print "Synonyms : "
		k=0
		for a in syn:
			k=k+1
			if k>limit:
				break
			print a.name()
			for lemma in a.lemmas():
				print " ",lemma.name()
	if len(nouns)>=2:
		a=(wordnet.synsets(nouns[0]))[0]
		b=(wordnet.synsets(nouns[1]))[0]
		print "Lowest Common"
		print a.lowest_common_hypernyms(b)#moves up the hypernym tree of a and b and returns common ones, to see if two nouns are related, like if you now query "dog and cat" it finds carnivores which could legitly be what you're searching for 
		print "Common"
		print a.common_hypernyms(b)
	name=name.replace(" ","_").capitalize()
	print name
	#to find same category items from our db, not sure of the sql query but, should test on MySQL database itself before putting it here 
	"""
	for p in Category.objects.raw('select pageId from Category where id=(select c.id from category_pages c, Page p where p.pageId=c.pages and p.name=name)'):
		print p
	"""
	#pages = Page.objects.filter(name__startswith=name)[0:5]
	#results = map(lambda x : x.name.replace("_"," "), pages)
	#return JsonResponse({"results":results})
