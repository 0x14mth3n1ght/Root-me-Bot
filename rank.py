#!/usr/bin/python

import time
import requests
import re

# User Agent lambda pour pas avoir de 429
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_user_rank(username=None):
	response = requests.get(f"https://api.www.root-me.org/{username}", headers=headers)
	if response.status_code == 200:
		pattern_points = r"<h3><img src='squelettes/img/valid.svg\?\d+' width='\d+' height='\d+' />&nbsp;(\d+)</h3>"
		points = re.search(pattern_points, response.text).group(1)
		time.sleep(0.2)  # Délai entre chaque requête
		
		pattern_rank = r"<h3><img src='squelettes/img/classement.svg\?\d+' width='\d+' height='\d+' />&nbsp;(\d+)</h3>"
		rank = re.search(pattern_rank, response.text).group(1)

		pattern_chall = r"<h3><img src='IMG/logo/rubon5\.svg\?\d+' width='\d+' height='\d+' />&nbsp;(\d+)</h3>"
		challs = re.search(pattern_chall, response.text).group(1)

		pattern_compromissions = r"<h3><img src='IMG/logo/rubon196.svg\?\d+' width='\d+' height='\d+' />&nbsp;(\d+)</h3>"
		compromissions = re.search(pattern_compromissions, response.text).group(1)

		return points, rank, challs, compromissions
	else:
		time.sleep(0.2)  # Délai entre chaque requête
		return "Error retrieving user ranking"

def get_user_profile(username=None):
	scores = []
	categories = ["Web-Client","Programmation","Cryptanalyse","Steganographie","Web-Serveur","Cracking","Realiste","Reseau","App-Script","App-Systeme","Forensic"]
	response = requests.get(f"https://api.www.root-me.org/{username}", headers=headers)
	if response.status_code == 200:
		for category in categories:
			pattern_category = r'href="fr/Challenges/'+category+'/">(\d+)%</a></span>'
			score_category = re.search(pattern_category, response.text).group(1)
			scores.append(category+': '+str(score_category)+"%")
			time.sleep(0.1)  # Délai entre chaque requête

		returnscores = "\n"
		for score in scores:
			returnscores += score + "\n"

		pattern_image = r'<img class="vmiddle logo_auteur logo_6forum" width="[0-9]+" height="[0-9]+" src="(.*)" alt="'+username+'" '
		image = re.search(pattern_image, response.text)
		imagetext = "https://www.root-me.org/"+str(image)

		return (returnscores, imagetext)
	else:
		time.sleep(0.2)  # Délai entre chaque requête
		return "Error retrieving user profile"

def get_user_last(username=None):
	response = requests.get(f"https://api.www.root-me.org/{username}", headers=headers)
	if response.status_code == 200:
		pattern = r';&nbsp;<a href="fr/Challenges/(?P<category>.+)/(?P<text>.+)">(?P<challenge>.+)</a><span class="right txs gris italic vmiddle">(?P<date>.+)</span></li>'
		challenges = []
		
		for match in re.finditer(pattern, response.text):
			text = match.group('text')
			challenge = match.group('challenge')
			date = match.group('date')
			category = match.group('category')
			challenges.append(f"({category}) {challenge} : {date}")
			time.sleep(0.1)  # Délai entre chaque requête

		returnchallenge = "\n"
		for challenge in challenges:
			returnchallenge += challenge + "\n"

		return returnchallenge
	
	else:
		time.sleep(0.2)  # Délai entre chaque requête
		return "Error retrieving user last challenges"

# Exemple d'utilisation
#username = "Nu1t"
#points , rank, challs, comprom = get_user_rank(username)
#print(f"{username} a {points} points, est classé {rank}, a résolu {challs} défis, et a pwn {comprom} machines ctfatd sur Root-Me")
#scores = get_user_profile(username)
#print(scores)
#challenges = get_user_last(username)
#print(challenges)
