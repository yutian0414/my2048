#-*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import random
import math
import json

class qipan(object):
	"""docstring for qipan"""
	def __init__(self, num):
		self.num = num

	def restart(self):

		for i in range(4):
			for j in range(4):
				self.num[i][j]=0
		self.num=randomnum(self.num)

	def operate(self):
		''' 先将底部数据赋值给辅助数组，然后上层数据同底部数据进行比较，如果相同则相加成为底部数据，如果不同则插入到辅助数组成为下一次比较的对象。
		需要考虑第一个底部数据为0的情况(为0时将棋盘数组中到此项删除，后面到自动替补成为此下标下新的数据，判断不为0后，使用此数据进行操作)，以及已
		经进入辅助数组的数据为合并后得到的数据（如果之前数据为合并后得到的则直接将下一个数据插入，不进行比较和合并） '''
		
		telist=[[],[],[],[]]             
		for i in range(4):
			telist[i].append(self.num[i][0])
			added=False
			for j in range(1,4):
				try:
					while self.num[i][j]==0:
						del self.num[i][j]

					# print(j)
					if self.num[i][j]==telist[i][-1] and added!=True:
						telist[i][-1]+=self.num[i][j]
						added=True
					else:
						telist[i].append(self.num[i][j])
						added=False
				except IndexError:
					pass
			if telist[i][0]==0:
				del telist[i][0]

			for x in range(4-len(telist[i])):
				telist[i].append(0)
			# print(telist[i])
		self.num=telist.copy()


def randomnum(orginlist):
	'''随机生成2或者4,随机赋值给数组中值为0的项，若没有为0的项则报错'''
	rownum=[]
	for i in range(0,4):
		for j in range(0,4):
			if orginlist[i][j]==0:
				rownum.append([i,j])
				print("%s,%s |" %(i,j),end="")
	print("\n")
	if rownum!=[]:
		seed=random.choice(range(0,len(rownum)))
		orginlist[rownum[seed][0]][rownum[seed][1]]=random.choice([2,2,4])
		return orginlist
	else:
		print("gameover")
		return "FULL"
	
def reverse(orginlist):
	'''左右镜像数组'''
	resultlist=[]
	for i in range(len(orginlist)):
		resultlist.append(orginlist[i][::-1])
	return resultlist
def clockwise(orginlist):
	'''顺时针旋转数组'''
	resultlist=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	for i in range(0,4):
		for j in range(0,4):
			# print(orginlist[i][j])
			# print(resultlist[j][3-i])
			resultlist[j][3-i]=orginlist[i][j]
	return resultlist
def unclockwise(orginlist):
	'''逆时针旋转数组'''
	resultlist=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	for i in range(0,4):
		for j in range(0,4):
			# print(orginlist[i][j])
			# print(resultlist[3-j][i])
			resultlist[3-j][i]=orginlist[i][j]
	return resultlist

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
		self.status=1
	def recation(self,screen,num):
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
		self.status=3
		gamealert=pygame.font.SysFont("Arial",100)
		alertsurfaceobj=gamealert.render(u'GAME OVER!',True,(255,0,0),(0,255,0))
		alertrectobj=alertsurfaceobj.get_rect()
		alertrectobj.center=(400,400)
		screen.blit(alertsurfaceobj,alertrectobj)

	def start(self,screen):
		self.status=1
		screen.fill((69,132,85))
		titlesurfaceobj=self.fontobj.render(u'2048',True,(0,0,0),)
		titlerectobj=titlesurfaceobj.get_rect()
		screen.blit(titlesurfaceobj,(300,100))

		startsurfaceobj=self.fontobj.render(u'Start',True,(0,0,0),(255,255,255))
		startrectobj=startsurfaceobj.get_rect()
		screen.blit(startsurfaceobj,(100,300))

		restartsurfaceobj=self.fontobj.render(u'Restart',True,(0,0,0),(255,255,255))
		restartrectobj=restartsurfaceobj.get_rect()
		screen.blit(restartsurfaceobj,(100,600))

		historysurfaceobj=self.fontobj.render(u'Record',True,(0,0,0),(255,255,255))
		historyrectobj=historysurfaceobj.get_rect()
		screen.blit(historysurfaceobj,(400,300))

class file(object):
	"""程序开始时读取上次记录以及历史得分排名，结束时记录保存此时数组数据以及得分"""
	def __init__(self):
		self.num=[]
		self.record={}
	def histroynumget(self):
		try:
			with open("historyrecord.txt",'rt') as fileobj:
				text=(fileobj.read()).replace("\n","")
				jsontext=json.loads(text)
				print(jsontext)
				try:
					self.num=jsontext[latest_num]
				except:
					self.num=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
				try:
					self.record=jsontext[Rank]
				except:
					self.record={}
		except:
				self.num=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
				self.record={}

	def writerecord(self,num,score):
		try:
			with open("historyrecord.txt",'rt') as fileobj:
				jsontext=json.load(fileobj)
		except:
			pass

if __name__ == '__main__':
	'''

	'''
	pygame.init()
	screen=pygame.display.set_mode((800,800),RESIZABLE,32)
	pygame.display.set_caption("2048")
	screen.fill((0,0,0))
	tr=treatnum()
	tr.start(screen)
	fil=file()
	fil.histroynumget()
	print(fil.num)
	pygame.display.flip()
	qi=qipan(fil.num)
	temp=qi.num
	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				exit()
			if tr.status==2:
				# print("1 left clicked!")
				if event.type==KEYDOWN:
					if event.key==K_DOWN:
						#逆时针旋转90度
						qi.num=clockwise(qi.num)
						qi.operate()
						qi.num=unclockwise(qi.num)
					if event.key==K_UP:
						#顺时针旋转90度
						qi.num=unclockwise(qi.num)
						qi.operate()
						qi.num=clockwise(qi.num)
					if event.key==K_LEFT:
						qi.operate()
					if event.key==K_RIGHT:
						#左右颠倒
						qi.num=reverse(qi.num)
						qi.operate()
						qi.num=reverse(qi.num)

					if temp==qi.num:						#判断运算之前和之后有没有变化
						check=randomnum(qi.num)
						if check=="FULL":					#判断16各格子是否都填满了数字
							print("gamealert")
							tr.gameover(screen)				#若前后没有变化，且数字都填满了格子，则认为游戏结束
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
			elif tr.status==1:
				# print("0 left clicked!")
				if event.type==MOUSEBUTTONDOWN:
					Pressedarry=pygame.mouse.get_pressed()
					pos=pygame.mouse.get_pos()
					print(pos)
					for index in range(len(Pressedarry)):
						if Pressedarry[index]:
							if index==0:
								if 100<pos[0] and pos[0]<250 and 300<pos[1] and pos[1]<400:
									tr.recation(screen,num)
								if 100<pos[0] and pos[0]<300 and 600<pos[1] and pos[1]<700:

									qi.restart()
									num=qi.num
									tr.recation(screen,num)
							else:
								pass
			elif tr.status==3:
				# print("3 left clicked!")
				if event.type==MOUSEBUTTONDOWN:
					Pressedarry=pygame.mouse.get_pressed()
					pos=pygame.mouse.get_pos()
					for index in range(len(Pressedarry)):
						if Pressedarry[index]:
							if index==0:
								if 150<pos[0] and pos[0]<650 and 300<pos[1] and pos[1]<500:
									tr.start(screen)

			# printnum(qi.num)
				
		pygame.display.update()