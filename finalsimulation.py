import random
import csv

#match information
totalovers=20
ballsinover=6

randomteams=['MI','DD','KKR','RCB','KXIP','RPS','GL','SRH']
#team information
team1,team2=raw_input("enter the two short forms of the teams you want to simulate seperated by a space").split()
#team1,team2=random.sample(randomteams,2)
#team1,team2 = '','GL'
#team1='MI'
#team2='RPS'

team={team1:{"players":[],"bowlers":[]},team2:{"players":[],"bowlers":[]}}
batorder={team1:[],team2:[]}
bowlstyle={team1:{},team2:{}}#NEW
with open("teaminfo.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        if(row[1]==team1):
            team[team1]["players"].append(row[0])
            batorder[team1].append(row[0])
            if(len(row)!=3):
                team[team1]["bowlers"].append((row[0],row[3]))
                bowlstyle[team1][row[0]]=row[3]
        elif(row[1]==team2):
            team[team2]["players"].append(row[0])
            batorder[team2].append(row[0])
            if(len(row)!=3):
                team[team2]["bowlers"].append((row[0],row[3]))
                bowlstyle[team2][row[0]]=row[3]


#batsman average for calculating threshold
bataverage={}
with open("pinfobatcluster5.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        bataverage[row[1]]=row[9]

#loading the probabilities loading all the data(most error prone as some rows might not be there!)
pvspprobabilities={}
with open("FinalTotalProbabilities5.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        pvspprobabilities[(row[0],row[1])]=row[2:]

        
#bowling styles
bowlingstyles={"RF":"Right Arm Fast","LF":"Left Arm Fast","RMF":"Right Arm Medium Fast","LMF":"Left Arm Medium Fast","ROS":"Right Arm Off Spin","LOS":"Left Arm Off Spin","RLS":"Right Arm Leg Spin","LLS":"Left Arm Leg Spin"}

#ground information
grounds=["PES Ground in bengaluru","Chinnaswamy stadium in bengaluru","Lords Crciket ground in london","Wankhede Stadium in mumbai","Nagpur Stadium in nagpur","Ranchi international stadium from the home of the MSD","Feroz Shah Kotla Stadium in Delhi"]#fill out other stadiums there
bowlingends=["K.V.S end","Dinkar end"]

#threshold for each batsman for predicting wickets
threshold={}
maxavg=max([float(v) for k,v in bataverage.iteritems()])
for k,v in bataverage.iteritems():
    threshold[k]=(1-(float(v)/float(maxavg)))



#simulation stuff
def predict(batsman,bowler,currprob):#will return 0->6 for runs and 10 if out
	#print simulate_wickets(batsman,bowler,currprob)
	flag,currprob=simulate_wickets(batsman,bowler,currprob)
	if(flag==1):
		return 10,currprob
	else:
		return simulate_runs(batsman,bowler),currprob
    
def simulate_wickets(batsman,bowler,currprob):
	pdissmissal=float(pvspprobabilities[(batsman,bowler)][-2])
	#print "in wicketsimulation"
	#print pdissmissal
	if(pdissmissal!=0):
		currprob[batsman]=currprob[batsman]*(1-pdissmissal)
	#print currprob[batsman]
	#print threshold[batsman]
	if(currprob[batsman]<threshold[batsman]):
		result=[]
		result.append(1)
		result.append(currprob)
		return result
	else:
		result=[]
		result.append(0)
		result.append(currprob)
		return result
    
def simulate_runs(batsman,bowler):
    bucketchoice=random.random()
    problist=map(float,pvspprobabilities[(batsman,bowler)][:7])
    cummproblist=[]
    cummproblist.append(problist[0])
    runs=0
    for i in range(1,len(problist)):
        cummproblist.append(cummproblist[i-1]+problist[i])
    #print problist
    #print cummproblist
    #print bucketchoice
    for i in range(0,len(cummproblist)):
        if(bucketchoice<=cummproblist[i]):
            runs=i
            break
    #print "runs===",runs
    return runs

comment=[]

#simulate toss and returns the name of the team going to bat
def prematchceremonies():
    weather=["warm and sunny here with a electric crowd waiting for the action to unfold!","hot and humid here with both teams and the crowd raring to go!","cold and damp here due to yesterdays rain but the crowd have turned up in large numbers waiting for a piece of the action","windy and stormy here with the slight chance of rain but that didnt stop the crowd from turning up in large numbers eagerly waiting for the action to commence!"]
    commentator=["Harsha Bogle","Danny Morrison","Ravi Shastri","Scott Styris","Brett Lee","Shoaib Akhtar","Shane Warne","Sunil Gavaskar","Laxman Sivaramakrsihanan","Sanjay Manjnekar"]
    pitchanalysis=["a soft and spongy wicket with a lot of grass so later on in the game we can expect the ball the swing and seam for the fast bowlers ","good surface to bat on as the pitch is a flat deck ","hard wicket to bat on with lots of cracks and the ball will turn later today ","good surface for the seamers to bowl as the pitch is very green and damp today with a lot of asssistance to swing bowlers "]#fill it out
    prematchcommentary="This is "+random.choice(commentator)+" talking to you live from the beautiful "+random.choice(grounds)+" .It is "+random.choice(weather)+" .Todays game promises to be an exciting one as these two rival teams line up .Talking about the pitch here it looks like a "+ random.choice(pitchanalysis)+"lets head to the toss now and see the action as it unfolds!"#fill it out 
    comment.append(prematchcommentary)
    t2tosschoice=random.randint(0,1)#ie heads or tails
    toss=random.randint(0,1)
    batbowlchoice=random.randint(0,1)
    tosswinner=team1
    if(toss!=t2tosschoice):
        if(batbowlchoice==0):
            print team1,"has won the toss and choose to bat"
            comment.append(team1+" has won the toss and choose to bat")
            tosswinlose=(team1,team2)
        else:
            print team1,"has won the toss and choose to bat"
            comment.append(team+" has won the toss and choose to bowl")
            tosswinlose=(team1,team2)
    else:
        if(batbowlchoice==0):
            print team1,"has won the toss and choose to bat"
            comment.append(team2+" has won the toss and choose to bowl")
            tosswinlose=(team1,team2)
        else:
            print team1,"has won the toss and choose to bat"
            comment.append(team2+" has won the toss and choose to bowl")
            tosswinlose=(team1,team2)
    return tosswinlose
#each state
def printstate():#ie scorecard after each ball+commentary for each ball
    pass

#modes of dissmissals
modeofdissmissal=["mankaded","hit wicket","slow bouncer top edged","bowled!!","LBW","caught","runout","stumped","caught at the slips","caught and bowled!","caught at short leg","toe crushing yorker!!"]#fill it out	
fourcommentry=["thats an elegent stright drive pushed to boundary by showing a straight bat what a shot!","he has smashed it dead stright with great ferocity what a shot!","he has played an eyewatering coverdrive what a delightful shot!","he has pulled that ball from right under his nose ! what tremoundous control","he has flicked that ball through the gap !such pure timing from a batsman of the highest class!","he has found the gap by playing an on drive ,there can be no better shot to watch in all of cricket than this one!","he is cut that ball with great power over the gully fielder and the ball has raced away to the boundary!!","thats so close ! edged and gone to the boundary,fortune surely does favour the brave","thats a delicate late cut played ,the fielder chases it but the ball beats him to the boundary","what a shot!!!! he has ABSOLUTELY DISMMISED IT FROM HIS SIGHTS !looks like he is on FIRE!!","thats an upper cut just beats the third man fielder and goes to the bondary a risky shot but well controlled by the batsman","he has swept him for a four! great shot","he has REVERSE swept for a four !he is just toying with the field what skill!","he has played a lofted inside out shot over the covers great hit! thats just bounced inside its a four!","OH NO!what a silly mistake by the fielder thats gone to the boundary !!you dont expect misfields at this level","IT'S IN THE AIRR! and he drops it near the boundary thats a four ! what a shocking display of fielding the captian is visibly agitated!!","what flair,what class, what balance !what a shot soo elegently played !! youngsters should learn how to play this shot by watching the replay of this shot!AWESOME!!","they dont call himm mr 360 for nothing thats a very innovative shot and it splits the field great shot!!","he has hit the ball so hard the fielder couldnt even take a step!!thats some scary stuff for the fielder and the bowler will be having nightmares of this shot!!"]
sixcommentry=["thats HUGE!!! he has dismissed it from his sights !! we wont be getting that ball back in a long time...","HOLYYYY MOLLLY what a hit thats HUUUUGGGGEEE!! its on the roof ,thats just sheer POWER!!","WHAT AN EFFORTLESS SHOT!IT JUST CAME OF THE MIDDLE OF HIS BAT","THATS JUST OVER THE FIELDER AT LONG ON!! WELL as they say a six is a six be it a huge one or one that just crosses the fence","thats slogged over midwicket for a six !!crazy hitting!!"," HOW DO YOU DESCRIBE THAT SHOT!! WHAT AN INNOVATIVE SHOT FROM A INNOVATIVE BATSMAN!!THEY DONT CALL HIM MR 360 FOR NOTHING!!","he has hit that straight like an arrow and that just whistles into the crowd!!","WATCH OUT ! that almost hit that security guard on the way !! great shot!!", "he has is just dancing donwn the pitch and he smoked it straigt outta here!!","he has hooked that for a huge six!! he is on fire","thats unfortunate for the bowler he has edgedd it stright behind the keeper and that has gone all the way for a six!!!","THE HELICOPTER HAS STARTED FLYING!!thats a crazy shot only someone as skilled as him could hace pulled this off","that is a special shot he has played an inside out shot all theway for a six!!","he has reverse swept him for a six, a very risky,predeterminedd shot but a great reward for the team","you dont get balls easier than that that is a full toss and he has hit it for a six !! bad bowling from the bowler","terrible bowling from the bowler!! he just gives a juicy ball and he has flicked it all the way for a six , you know what harsha! my granny could have hit that too it was that easy!!"]
dotcommentry=["thats a dropped catch! that was a hard chance for the fielder but thats a good attempt!!","thats just missed the stumps great piece of bowling!!","thats beaten the batsman fair and square brillaint bowling","thats just gone past the outside edge !!unlucky for the bowler","thats soun away from the batsman  great piece of bowling ","thats swung into the batsman and leaves him completely bamboozeled!! great stufff","thats a quick bouncer and had the batsmn ducking for cover he is bringing the heat to him!!","OH NO! THATS HIT HIM ON THE HEAD HOPE HE IS OKAY!","thats spun into the batsman and just clips his pads great bowling","thats hit stright to the fielder no run!","the batsman tries to take a run but thats brilliant fielding from the fielder to deny him taking a run!","that fielder is just flying like superman!! brillaint stop ! great fielding","that ball just hit him in his crotch it must hurt a lot!i still find it funny though!!","thats wizardly bowling from him ! the batsman has no clue about the ball !","that ball has left the batsman completely flummoxed! brillaint stuff from gazza!","that ball spun sharply there is nothing much the batsman could have dome to play that!","thats lightninig fast from the bowler ! the batsman couldnt even see the ball !!ohh this contest is getting intersting now!!","this is what you expect when a great bowler bowls to any batsman that ball is the stuff of dreams brillant"]

#each innings
def firstinnings():
    #innings initialization
	score=0
	wickets=0
	overscompleted=0#max=totalovers
	ballsbowled=0#max=ballsinover
	scorecard={}
	batteam,bowlteam=team1,team2
	battingorder=team[batteam]["players"]
	bowlers=[x[0] for x in team[bowlteam]["bowlers"]]
	bowlerovercount={}
	bowlerwickets={}
	bowlerscore={}#new
	batsman50or100={}
	for bowler in bowlers:
		bowlerovercount[bowler]=0#max can be 4
	for bowler in bowlers:
		bowlerwickets[bowler]=0
	for bowler in bowlers:#new
		bowlerscore[bowler]=0
	for batsman in battingorder:
		scorecard[batsman]={"runs":0,"balls":0,"4s":0,"6s":0,"dissmissal":"not out","bowler":"--"}
	for batsman in battingorder:
		batsman50or100[batsman]=[False,False]
	#current batting probabilites for wicket simulation
	batcurrprob={k:float(1.0) for k,v in threshold.iteritems()}
	
	#initial status of striker,nonstriker,bowler
	striker=battingorder[0]
	nonstriker=battingorder[1]
	currbowler=random.choice(bowlers)
	currend=0
	print "INITIALLY"
	print "the ball is with "+currbowler+" and he is going to bowl "+bowlingstyles[bowlstyle[bowlteam][currbowler]]+ "from "+bowlingends[currend%2]#NEW
	print[("Striker",striker),("NonStriker",nonstriker),("currbowler",currbowler)]
	print 
	print
	currend+=1
	count=0
	ccount=0
	#simulating now
	for over in range(1,totalovers+1):
		for ball in range(1,ballsinover+1):
			state,batcurrprob=predict(striker,currbowler,batcurrprob)
			#he is out
			if(state==10):
				print "####################"
				print striker,"is OUT!","HE IS ",random.choice(modeofdissmissal),"by",currbowler
				print "####################"
				print 
				print 
				print
				scorecard[striker]["bowler"]=currbowler
				scorecard[striker]["dissmissal"]=random.choice(modeofdissmissal)#get the next batsman to bat
				#print "batting order",battingorder
				if striker in battingorder:
					battingorder.remove(striker)
				#print "batting order",battingorder
				if nonstriker in battingorder: 
					battingorder.remove(nonstriker)
				#print "batting order final",battingorder
				if(len(battingorder)>0):
					striker=battingorder[0]
				ballsbowled+=1
				wickets+=1
				bowlerwickets[currbowler]+=1
				if(wickets==10):
					#finish innings
					return score,wickets,overscompleted,ballsbowled,bowlerovercount,bowlerwickets,bowlerscore,scorecard,batteam,bowlteam
			elif(state%2==0):#run has happened the striker has hit either a 0,2,4,6 he should stay on strike
				print "runs scored now=",state
				scorecard[striker]["runs"]+=state
				bowlerscore[currbowler]+=state
				scorecard[striker]["balls"]+=1
				print striker,"==>",scorecard[striker]["runs"]
				if(state==0):
					print random.choice(dotcommentry)
				if(state==4):
					scorecard[striker]["4s"]+=1
					print random.choice(fourcommentry)
				elif(state==6):
					scorecard[striker]["6s"]+=1
					print random.choice(sixcommentry)
				if(scorecard[striker]["runs"]>=50 and scorecard[striker]["runs"]<100 and batsman50or100[striker][0]==False):
					print "***********"
					print "thats a well deserved 50 for"+striker+" well played!!"
					print "***********"
					batsman50or100[striker][0]=True
					print striker,"==>",scorecard[striker]["runs"]
				elif(scorecard[striker]["runs"]>=100 and batsman50or100[striker][1]==False):
					print "***********"
					print "WHAT A KNOCK BY THAT PLAYER!! well deserved 100 for "+striker+" very well played!!"
					print "***********"
					batsman50or100[striker][1]=True
					print striker,"==>",scorecard[striker]["runs"]
				score+=state
				ballsbowled+=1
			#the nonstriker is on strike now
			else:
				print "runs scored now=",state
				scorecard[striker]["runs"]+=state
				bowlerscore[currbowler]+=state
				scorecard[striker]["balls"]+=1
				print striker,"==>",scorecard[striker]["runs"]
				if(state==0):
					print random.choice(dotcommentry)
				if(state==4):
					scorecard[striker]["4s"]+=1
					print random.choice(fourcommentry)
				elif(state==6):
					scorecard[striker]["6s"]+=1
					print random.choice(sixcommentry)
				if(scorecard[striker]["runs"]>=50 and scorecard[striker]["runs"]<100 and batsman50or100[striker][0]==False):
					print "***********"
					print "thats a well deserved 50 for"+striker+" well played!!"
					print "***********"
					batsman50or100[striker][0]=True
					print striker,"==>",scorecard[striker]["runs"]
				elif(scorecard[striker]["runs"]>=100 and batsman50or100[striker][1]==False):
					print "***********"
					print "WHAT A KNOCK BY THAT PLAYER!! well deserved 100 for "+striker+" very well played!!"
					print "***********"
					batsman50or100[striker][1]=True
					print striker,"==>",scorecard[striker]["runs"]
				score+=state
				ballsbowled+=1
				striker,nonstriker=nonstriker,striker
			print 
			print[("Striker",striker),("NonStriker",nonstriker),("currbowler",currbowler)]
			#for ball by ball
			'''
			while True:
				try:
					choice= int(raw_input("Press 1 to continue simulating..0 to exit"))
				except ValueError:
					print("please retry..")
					continue
				if(choice==1):
					break
				elif(choice==0):
					exit()
			'''
		#reset after the over completion
		ballsbowled=0
		striker,nonstriker=nonstriker,striker
		print "OVERUP!!"
		overscompleted+=1
		bowlerovercount[currbowler]+=1
		print "BOWLING OVER COUNT IS ",bowlerovercount
		print "BOWLING SCORECARD IS",bowlerwickets
		#predicting the next bowler to bowl
		print
		print
		print "FOR THE NEXT OVER INITIAL STATE IS"
		print[("Striker",striker),("NonStriker",nonstriker),("currbowler","...")]
		print 
		print
		nextbowler=random.choice(bowlers)
		while (nextbowler==currbowler) or (bowlerovercount[nextbowler]==4):
			nextbowler=random.choice(bowlers)
		currbowler=nextbowler
		if(over<20):
			print "the ball is with "+currbowler+" and he is going to bowl "+bowlingstyles[bowlstyle[bowlteam][currbowler]]+ " from "+bowlingends[currend%2]#NEW
			currend+=1
		#for ball by ball
		'''
		while True:
			try:
				choice= int(raw_input("Press 1 to continue simulating..0 to exit"))
			except ValueError:
				print("please retry..")
				continue
			if(choice==1):
				break
			elif(choice==0):
				exit()
		'''
		
	return score,wickets,overscompleted,ballsbowled,bowlerovercount,bowlerwickets,bowlerscore,scorecard,batteam,bowlteam





def secondinnings():
	firstinning=firstinnings()
	print "#######################################"
	print "END OF FIRST INNINGS"
	print "#######################################"
	scoretobeat=firstinning[0]
	batteam=firstinning[-1]
	bowlteam=firstinning[-2]
	#innings initialization
	score=0
	wickets=0
	overscompleted=0#max=totalovers
	ballsbowled=0#max=ballsinover
	scorecard={}
	battingorder=team[batteam]["players"]
	bowlers=[x[0] for x in team[bowlteam]["bowlers"]]
	bowlerovercount={}
	bowlerwickets={}
	bowlerscore={}#new
	batsman50or100={}
	for bowler in bowlers:
		bowlerovercount[bowler]=0#max can be 4
	for bowler in bowlers:
		bowlerwickets[bowler]=0#max can be 4
	for bowler in bowlers:#new
		bowlerscore[bowler]=0
	for batsman in battingorder:
		scorecard[batsman]={"runs":0,"balls":0,"4s":0,"6s":0,"dissmissal":"not out","bowler":"--"}
	for batsman in battingorder:
		batsman50or100[batsman]=[False,False]
	#current batting probabilites for wicket simulation
	batcurrprob={k:float(1.0) for k,v in threshold.iteritems()}
	
	#initial status of striker,nonstriker,bowler
	striker=battingorder[0]
	nonstriker=battingorder[1]
	currbowler=random.choice(bowlers)
	currend=0
	print "INITIALLY"
	print "the ball is with "+currbowler+" and he is going to bowl "+bowlingstyles[bowlstyle[bowlteam][currbowler]]+ "from "+bowlingends[currend%2]#NEW
	print[("Striker",striker),("NonStriker",nonstriker),("currbowler",currbowler)]
	print 
	print
	currend+=1
	#simulating now
	for over in range(1,totalovers+1):
		for ball in range(1,ballsinover+1):
			state,batcurrprob=predict(striker,currbowler,batcurrprob)
			#he is out
			if(state==10):
				print "####################"
				print striker,"is OUT!","HE IS ",random.choice(modeofdissmissal),"by",currbowler
				print "####################"
				print 
				print 
				print
				scorecard[striker]["bowler"]=currbowler
				scorecard[striker]["dissmissal"]=random.choice(modeofdissmissal)#get the next batsman to bat
				#print "batting order",battingorder
				if striker in battingorder:
					battingorder.remove(striker)
				#print "batting order",battingorder
				if nonstriker in battingorder: 
					battingorder.remove(nonstriker)
				#print "batting order final",battingorder
				if(len(battingorder)>0):
					striker=battingorder[0]
				ballsbowled+=1
				wickets+=1
				bowlerwickets[currbowler]+=1
				if(wickets==10 and score<scoretobeat):
					print "#############"
					print "#############"
					print "#############"
					print "#############"
					print "#############"
					print "TEAM",bowlteam,"WINS BY",scoretobeat-score,"RUNS!!!!"
					return [list(firstinning),score,wickets,overscompleted,ballsbowled,bowlerovercount,bowlerwickets,bowlerscore,scorecard,batteam,bowlteam]
			elif(state%2==0):#run has happened the striker has hit either a 0,2,4,6 he should stay on strike
				print "runs scored now=",state
				scorecard[striker]["runs"]+=state
				scorecard[striker]["balls"]+=1
				bowlerscore[currbowler]+=state
				print striker,"==>",scorecard[striker]["runs"]
				if(state==0):
					print random.choice(dotcommentry)
				if(state==4):
					scorecard[striker]["4s"]+=1
					print random.choice(fourcommentry)
				elif(state==6):
					scorecard[striker]["6s"]+=1
					print random.choice(sixcommentry)
				if(scorecard[striker]["runs"]>=50 and scorecard[striker]["runs"]<100 and batsman50or100[striker][0]==False):
					print "***********"
					print "thats a well deserved 50 for"+striker+" well played!!"
					print "***********"
					batsman50or100[striker][0]=True
					print striker,"==>",scorecard[striker]["runs"]
				elif(scorecard[striker]["runs"]>=100 and batsman50or100[striker][1]==False):
					print "***********"
					print "WHAT A KNOCK BY THAT PLAYER!! well deserved 100 for "+striker+" very well played!!"
					print "***********"
					batsman50or100[striker][1]=True
					print striker,"==>",scorecard[striker]["runs"]
				score+=state
				ballsbowled+=1
				if(score>scoretobeat):
					print "#############"
					print "#############"
					print "#############"
					print "#############"
					print "#############"
					print "TEAM",batteam,"WINS WITHIN",overscompleted,".",ballsbowled," OVERS WITH ",10-wickets,"WICKETS TO SPARE!!!"
					return [list(firstinning),score,wickets,overscompleted,ballsbowled,bowlerovercount,bowlerwickets,bowlerscore,scorecard,batteam,bowlteam]
			#the nonstriker is on strike now
			else:
				print "runs scored now=",state
				scorecard[striker]["runs"]+=state
				scorecard[striker]["balls"]+=1
				bowlerscore[currbowler]+=state
				print striker,"==>",scorecard[striker]["runs"]
				if(state==0):
					print random.choice(dotcommentry)
				if(state==4):
					scorecard[striker]["4s"]+=1
					print random.choice(fourcommentry)
				elif(state==6):
					scorecard[striker]["6s"]+=1
					print random.choice(sixcommentry)
				if(scorecard[striker]["runs"]>=50 and scorecard[striker]["runs"]<100 and batsman50or100[striker][0]==False):
					print "***********"
					print "thats a well deserved 50 for"+striker+" well played!!"
					print "***********"
					batsman50or100[striker][0]=True
					print striker,"==>",scorecard[striker]["runs"]
				elif(scorecard[striker]["runs"]>=100 and batsman50or100[striker][1]==False):
					print "***********"
					print "WHAT A KNOCK BY THAT PLAYER!! well deserved 100 for "+striker+" very well played!!"
					print "***********"
					batsman50or100[striker][0]=True
					print striker,"==>",scorecard[striker]["runs"]
				score+=state
				ballsbowled+=1
				if(score>scoretobeat):
					print "#############"
					print "#############"
					print "#############"
					print "#############"
					print "#############"
					print "TEAM",batteam,"WINS WITHIN",overscompleted,".",ballsbowled," OVERS WITH ",10-wickets,"WICKETS TO SPARE!!!"
					return [list(firstinning),score,wickets,overscompleted,ballsbowled,bowlerovercount,bowlerwickets,bowlerscore,scorecard,batteam,bowlteam]
				striker,nonstriker=nonstriker,striker
			print
			print[("Striker",striker),("NonStriker",nonstriker),("currbowler",currbowler)]
			'''
			while True:
				try:
					choice= int(raw_input("Press 1 to continue simulating..0 to exit"))
				except ValueError:
					print("please retry..")
					continue
				if(choice==1):
					break
				elif(choice==0):
					exit()
			'''
		#reset after the over completion
		ballsbowled=0
		striker,nonstriker=nonstriker,striker
		print "OVERUP!!"
		overscompleted+=1
		bowlerovercount[currbowler]+=1
		print "BOWLING OVER COUNT IS ",bowlerovercount
		print "BOWLING SCORECARD IS",bowlerwickets
		#predicting the next bowler to bowl
		print
		print
		print "FOR THE NEXT OVER INITIAL STATE IS"
		print[("Striker",striker),("NonStriker",nonstriker),("currbowler","...")]
		print 
		print
		nextbowler=random.choice(bowlers)
		while (nextbowler==currbowler) or (bowlerovercount[nextbowler]==4):
			nextbowler=random.choice(bowlers)
		currbowler=nextbowler
		if(over<20):
			print "the ball is with "+currbowler+" and he is going to bowl "+bowlingstyles[bowlstyle[bowlteam][currbowler]]+ " from "+bowlingends[currend%2]#NEW
			currend+=1
		#for ball by ball commentry
		'''
		while True:
			try:
				choice= int(raw_input("Press 1 to continue simulating..0 to exit"))
			except ValueError:
				print("please retry..")
				continue
			if(choice==1):
				break
			elif(choice==0):
				exit()
		'''
	if(score<scoretobeat):
		print "#############"
		print "#############"
		print "#############"
		print "#############"
		print "#############"
		print "TEAM",bowlteam,"WINS BY",scoretobeat-score,"RUNS!!!!"
		return [list(firstinning),score,wickets,overscompleted,ballsbowled,bowlerovercount,bowlerwickets,bowlerscore,scorecard,batteam,bowlteam]

# 0      1       2              3           4               5             6              7       8      9
#[score,wickets,overscompleted,ballsbowled,bowlerovercount,bowlerwickets,bowlerscore,scorecard,batteam,bowlteam]
def scorecard(l):
    score=str(l[0])+"/"+str(l[1])
    overs=str(l[2])+"."+str(l[3])
    batteam=str(l[8])
    bowlteam=str(l[9])
    bowlers=[]
    battingorder=batorder[batteam]
    for k in l[4].keys():
        bowlers.append(k)
    bowlingscorecard=[]
    battingscorecard=[]
    for bowler in bowlers:
        bscore=str(bowler)+"  ::  "+str(l[6][bowler])+"/"+str(l[5][bowler])+" in "+str(l[4][bowler])+" overs "
        bowlingscorecard.append(bscore)
    #print battingorder
    for batsman in battingorder:
        runs=l[7][batsman]["runs"]
        dissmissedby=l[7][batsman]["bowler"]
        sixes=l[7][batsman]["6s"]
        fours=l[7][batsman]["4s"]
        balls=l[7][batsman]["balls"]
        modeofdissmissal=l[7][batsman]["dissmissal"]
        #print (batsman,runs,balls,fours,sixes,fours,balls,dissmissedby,modeofdissmissal)
        batscore=str(batsman)+"  ::  "+" runs= "+str(runs)+","+" balls= "+str(balls)+","+" 4s= "+str(fours)+","+" 6s= "+str(sixes)+","+" dissmissedby= "+str(dissmissedby)+","+" modeofdissmisssal= "+str(modeofdissmissal)
        battingscorecard.append(batscore)
    print "SCORE:: "+score
    print "OVERS:: "+overs
    print
    print ".................."
    print
    print "BATTING SCORE CARD"
    for bat in battingscorecard:
        print bat
    print
    print ".................."
    print
    print "BOWLING SCORE CARD"
    #print bowlingscorecard
    for bowl in bowlingscorecard:
        print bowl




#call it in the right order!
def create_match():
    m=secondinnings()
    print "#############"
    print "#############"
    print "#############"
    print "#############"
    print "MATCH SUMMARY"
    print "#############"
    print "#############"
    print "#############"
    print "#############"
    print "#############"
    for x in comment:
        print "--------"
        print x
        print "--------"
    print "#############"
    print "#############"
    print "#############"
    print "#############"
    print "#############"
    print "FIRST INNING SCORE CARD"
    #print m[0]
    #print "&&&&&&&&&&&&&&&"
    scorecard(list(m[0]))
    print "#############"
    print "#############"
    print "#############"
    print "#############"
    print "#############"
    print "SECOND INNING SCORE CARD"
    #print m[1:]
    #print "&&&&&&&&&&&&&&&"
    scorecard(m[1:])
    print "#############"
    print "#############"
    print "#############"
    print "#############"
    print "#############"
    print team1,team2


if __name__ == "__main__":
    create_match()
