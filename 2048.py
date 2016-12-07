#-*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import random
import math
import json

class qipan(object):
	"""将棋盘上的数字看作一个数组，定义初始化以及在命令下的变换规则"""
	def __init__(self, num,score):
		self.num=num
		if self.num==[] or self.num==[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]] or self.num==None:
			self.restart()
		self.score=score
	def restart(self):

		for i in range(4):
			for j in range(4):
				self.num[i][j]=0
		self.num=randomnum(self.num)
		self.score=0

	def operate(self):
		''' 先将底部数据赋值给辅助数组，然后上层数据同底部数据进行比较，如果相同则相加成为底部数据，如果不同则插入到辅助数组成为下一次比较的对象。
		需要考虑第一个底部数据为0的情况(为0时将棋盘数组中到此项删除，后面到自动替补成为此下标下新的数据，判断不为0后，使用此数据进行操作)，以及已
		经进入辅助数组的数据为合并后得到的数据（如果之前数据为合并后得到的则直接将下一个数据插入，不进行比较和合并） '''
		telist=[[],[],[],[]]             
		for i in range(4):
			telist[i].append(self.num[i][0])
			added=False														#用来判断之前的数据是家和得来还是直接移过来的
			for j in range(1,4):
				try:
					while self.num[i][j]==0:
						del self.num[i][j]									#如果某项为0,则将其删掉，后面的项自动填充到此项
					if self.num[i][j]==telist[i][-1] and added==False:		#如果此项同变化后数组最后一项相同，且变化后数组最后一项不十合并得到
						telist[i][-1]+=self.num[i][j]						#进行合并
						added=True  										#将判断是否为合并得来到值更新为真
						self.score+=telist[i][-1]
						print(self.score)
					else:
						telist[i].append(self.num[i][j])					#如果不相同，或者为合并得来，则直接将数据添加到变化后到数组中。
						added=False
				except IndexError:											#如果有删除，则会造成数组索引超出长度
					pass
			if telist[i][0]==0:												#判断之前底部到值是否是0,如果为0,则删除。
				del telist[i][0]

			for x in range(4-len(telist[i])):								#通过数组的长度来判断有多少位需要补0
				telist[i].append(0)
		self.num=telist.copy()

	def down(self):
		self.num=self.__clockwise(self.num)			#先将数组顺时针旋转90
		self.operate()						#将数组向左进行变换，包括合并，移位
		self.num=self.__unclockwise(self.num)			#再将数组逆时针旋转90
		return self.num
	def up(self):
		self.num=self.__unclockwise(self.num)
		self.operate()
		self.num=self.__clockwise(self.num)
		return self.num
	def left(self):
		self.operate()
		return self.num
	def right(self):
		self.num=self.__reverse(self.num)
		self.operate()
		self.num=self.__reverse(self.num)
		return self.num
	def __reverse(self,orginlist):
		'''左右镜像数组'''
		resultlist=[]
		for i in range(len(orginlist)):
			resultlist.append(orginlist[i][::-1])
		return resultlist
	def __clockwise(self,orginlist):
		'''顺时针旋转数组'''
		resultlist=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		for i in range(0,4):
			for j in range(0,4):
				resultlist[j][3-i]=orginlist[i][j]
		return resultlist
	def __unclockwise(self,orginlist):
		'''逆时针旋转数组'''
		resultlist=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		for i in range(0,4):
			for j in range(0,4):
				resultlist[3-j][i]=orginlist[i][j]
		return resultlist


def randomnum(orginlist):
	'''随机生成2或者4,随机赋值给数组中值为0的项，若没有为0的项则报错'''
	rownum=[]
	for i in range(0,4):
		for j in range(0,4):
			if orginlist[i][j]==0:
				rownum.append([i,j])										#将为0的项的坐标添加到数组
				print("%s,%s |" %(i,j),end="")
	print("\n")
	if rownum!=[]:
		seed=random.choice(range(0,len(rownum)))							#随机挑选一行
		orginlist[rownum[seed][0]][rownum[seed][1]]=random.choice([2,2,4])	#从2,2，4中随机挑选。改变这个数组2和4的比例可以改变初夏2和4的机会
		return orginlist
	else:
		print("gameover")
		return "FULL"

def printnum(orginlist):
	'''shell 中格式化打印'''
	print("=="*10)
	for i in range(0,4):
		print("|",end="")
		for j in range(0,4):
			print("%s |" %(orginlist[i][j]),end="")
		print("\n")
	print("\n"+"=="*10+"\n")

class treatnum(object):
	"""生成屏幕窗口部件，包括数字更新，结束提示"""
	def __init__(self):
		self.fontobj=pygame.font.SysFont('Arial',80)
		self.scorefontobj=pygame.font.SysFont('Arial',40)
		self.status=1									#状态编号，用于判定此时界面处于那个界面。1为初始界面，2为棋盘界面，3为结束界面
	def recation(self,screen,num):
		'''显示棋盘界面，包括棋盘布局，棋盘数字显示，棋盘各个方格颜色变化'''
		screen.fill((0,0,0))
		self.status=2		
		text=[[],[],[],[]]
		for i in range(0,800,200):
			for j in range(0,800,200):
				if num[i//200][j//200]!=0:
					textsurfaceobj=self.fontobj.render(u'%s' %num[i//200][j//200],True,(0,0,123),)
					r=math.log(num[i//200][j//200],2)*17
					g=255-r
					b=255*(1-r//255)
				else:
					textsurfaceobj=self.fontobj.render(u'',True,(0,0,123),)
					r=200
					g=200
					b=200
				squre=pygame.draw.rect(screen,[r,g,b],((j+2,i+2),(196,196)))
				textrectobj=textsurfaceobj.get_rect()
				textrectobj.center=(j+100,i+100)
				screen.blit(textsurfaceobj,textrectobj)

	def gameover(self,screen):
		'''显示游戏结束界面'''
		self.status=3
		gamealert=pygame.font.SysFont("Arial",100)
		alertsurfaceobj=gamealert.render(u'GAME OVER!',True,(255,0,0),(0,255,0))
		alertrectobj=alertsurfaceobj.get_rect()
		alertrectobj.center=(400,400)
		screen.blit(alertsurfaceobj,alertrectobj)

	def start(self,screen,record):
		'''设定初始界面，包括各个按键到位置，显示文字等'''
		self.status=1
		screen.fill((69,132,85))
		titlesurfaceobj=self.fontobj.render(u'2048',True,(0,0,0),)
		titlerectobj=titlesurfaceobj.get_rect()
		screen.blit(titlesurfaceobj,(300,70))

		startsurfaceobj=self.fontobj.render(u'Start',True,(0,0,0),(255,255,255))
		startrectobj=startsurfaceobj.get_rect()
		screen.blit(startsurfaceobj,(100,200))

		restartsurfaceobj=self.fontobj.render(u'Restart',True,(0,0,0),(255,255,255))
		restartrectobj=restartsurfaceobj.get_rect()
		screen.blit(restartsurfaceobj,(80,450))

		historysurfaceobj=self.fontobj.render(u'Record',True,(0,0,0),(255,255,255))
		historyrectobj=historysurfaceobj.get_rect()
		screen.blit(historysurfaceobj,(400,200))
		for i in range(1,6):
			ranksurfaceobj=self.scorefontobj.render(u'NO.%s' %i,True,(0,0,0),(255,255,255))
			rankrectobj=ranksurfaceobj.get_rect()
			screen.blit(ranksurfaceobj,(400,300+i*50))
			scoresurfaceobj=self.scorefontobj.render(u'%s' %record["NO.%s" %i],True,(0,0,0),(255,255,255))
			scorerectobj=scoresurfaceobj.get_rect()
			screen.blit(scoresurfaceobj,(550,300+i*50))

class file(object):
	"""程序开始时读取上次记录以及历史得分排名，结束时记录保存此时数组数据以及得分"""
	def __init__(self):
		self.num=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		self.record={}
		self.latestscore=0
	def histroynumget(self):
		'''获得历史记录，若失败进行初始化'''
		try:
			with open("historyrecord.txt",'rt') as fileobj:
				text=(fileobj.read()).replace("\n","")
				jsontext=json.loads(text)
				print(jsontext)
			try:
				self.num=jsontext["latest_num"]
			except:
				self.num=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
			try:
				self.record=jsontext["Rank"]
				print(type(self.record))
			except:
				self.record={}
			try:
				self.latestscore=jsontext["latest_score"]
			except:
				self.latestscore=0
		except:
			pass


	def writerecord(self,num,score):
		'''写入数据到记录中'''
		recorlist=[]
		historydict={}
		recordict={}
		print(self.record,type(self.record))
		if self.record!={}:
			for k,scor in self.record.items():
				recorlist.append(scor)
		else:
			pass
		recorlist.append(score)
		recorlist.sort(reverse=True)
		print(recorlist)
		for i in range(0,5):
			if i<=len(recorlist)-1:
				recordict["NO."+str(i+1)]=recorlist[i]
			else:
				recordict["NO."+str(i+1)]=0
		historydict['latest_num']=num
		historydict['Rank']=recordict
		historydict['latest_score']=score
		jsonstr=json.dumps(historydict)
		print(jsonstr)
		with open("historyrecord.txt",'wt') as fileobj:
			fileobj.write(jsonstr)


def main():
	pygame.init()												#初始化
	screen=pygame.display.set_mode((800,800),RESIZABLE,32)		#生成屏幕，大小可调
	pygame.display.set_caption("2048")							#设置标题
	screen.fill((0,0,0))										#填充初始颜色
	fil=file()													#初始化一个从历史记录中读取数据，以及保存数据的实例
	fil.histroynumget()											#读取历史数据
	print(fil.num)								
	tr=treatnum()												#初始化一个数据显示处理，包括开始界面，棋盘界面和游戏结束界面的实例
	tr.start(screen,fil.record)									#生成开始界面
	pygame.display.flip()										#刷新显示
	qi=qipan(fil.num,fil.latestscore)							#初始化一个棋盘类，包括初始数组重置，数组根据指令进行变换得到新的数组.
	temp=qi.num 												#设置一个临时变量保存处理之前数组的值，与处理之后到值进行比较，帮助判断变换之前棋盘是否有变化。
	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				fil.writerecord(qi.num,qi.score)
				exit()
			if tr.status==2:								#判断是否在棋盘界面下面
				if event.type==KEYDOWN:
					if event.key==K_DOWN:
						qi.down()
					if event.key==K_UP:
						qi.up()
					if event.key==K_LEFT:
						qi.left()
					if event.key==K_RIGHT:
						qi.right()

					if temp==qi.num:						#判断运算之前和之后有没有变化
						check=randomnum(qi.num)
						if check=="FULL":					#判断16各格子是否都填满了数字
							print("gamealert")
							score=qi.score
							print("%s\n%s\n%s\n%s\n%s\n%s" %(temp,qi.num,qi.down(),qi.up(),qi.left(),qi.right()))
							
							if temp==qi.down() and temp==qi.up() and temp==qi.left() and temp==qi.right():
								tr.gameover(screen)				#若前后没有变化，且数字都填满了格子，则认为游戏结束
							else:
								qi.num=temp
								qi.score=score
						else:
							qi.num=temp						#若格子不满，则将数组置为之前到数组，即数组不变，不产生随机数
							tr.recation(screen,qi.num)		#刷屏
					else:
						check=randomnum(qi.num)				
						if check=="FULL":					#前后发生变化，然后格子充满，这种状况应该不存在
							tr.recation(screen,qi.num)

						else:								#前后发生变化，格子不充满，则棋盘数组更新随机数，将老保存老数组前移
							qi.num=check
							temp=qi.num
							tr.recation(screen,qi.num)
			elif tr.status==1:								#判断是否在开始界面下
				if event.type==MOUSEBUTTONDOWN:
					Pressedarry=pygame.mouse.get_pressed()
					print(Pressedarry)
					pos=pygame.mouse.get_pos()
					print(pos)
					for index in range(len(Pressedarry)):
						if Pressedarry[index]:
							if index==0:
								if 100<pos[0] and pos[0]<280 and 200<pos[1] and pos[1]<300:		#判断是否在start按钮区域
									tr.recation(screen,fil.num)									#点击start按钮，载入上次数组，进行显示
								if 80<pos[0] and pos[0]<330 and 450<pos[1] and pos[1]<550:		#判断是否在restat按钮区域
									fil.writerecord(qi.num,qi.score)
									fil.histroynumget()
									qi.restart()												#点击restart按钮，棋盘的数组全部置0,然后生成一个随机数（2,4）
									num=qi.num 													#得到num
									tr.recation(screen,num)										#使用新到num进行显示
							else:
								pass															#没有点到有效区域不动作
			elif tr.status==3:																	#在界面3时（即提示game over时）
				if event.type==MOUSEBUTTONDOWN:
					Pressedarry=pygame.mouse.get_pressed()
					pos=pygame.mouse.get_pos()
					for index in range(len(Pressedarry)):
						if Pressedarry[index]:
							if index==0:
								if 150<pos[0] and pos[0]<650 and 300<pos[1] and pos[1]<500:
									fil.writerecord(qi.num,qi.score)
									main()									#点击game over区域后回到初始界面。

		pygame.display.update()
if __name__ == '__main__':
	main()