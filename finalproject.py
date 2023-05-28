#100shi
import pygame
import textwrap
from pygame.locals import *
import sys
import time
import random
pygame.init()
screen=pygame.display.set_mode((900, 500))
white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)
def text_format(message, textFont, textSize, textColor):
    global font
    newText=font.render(message, 0, textColor)
    return newText
font = pygame.font.SysFont('tempus sans ITC',55)
clock = pygame.time.Clock()
FPS=30
    
class Test:
   
    def __init__(st):
        st.width=900
        st.height=500
        st.reset=True
        st.active = False
        st.input_text=''        # user input 
        st.word = ''            # for comparison 
        st.time_start = 0
        st.total_time = 0
        st.accuracy = '0%'
        st.results = 'Time:0 Accuracy:0 % Wpm:0 '
        st.wpm = 0
        st.end = False
        st.HEAD_C = (255,255,0)            # borders
        st.TEXT_C = (240,240,240)
        st.RESULT_C = (180,225,100)
        
       
        pygame.init()
        st.screen = pygame.display.set_mode((st.width,st.height))     # surface
        

        
    def showsentence(st, screen, msg, y ,fsize, color):         # msg=100shi speed typing test
        font = pygame.font.SysFont('tempus sans ITC', fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(st.width/2, y))    #coordinates of the text
        screen.blit(text,text_rect)
        pygame.display.update()   
        
    def randomoutput(st):# make changes here...long sentences are going out of the window
        f=open('sentences.txt','r')
        r=f.read()
        k=r.split()
        i=1
        sentence=''
        while i<len(k):
            w=random.choice(k)
            sentence+=(w+' ')
            i+=1
            
          
        wrapped=textwrap.TextWrapper(width=70)      # text wrap to not let the sentences go out of frame 
        wlist=wrapped.wrap(text=sentence)
        #return('\n\n' + wrapped.fill(text = sentence))
        for i in wlist:
            return(i)

        blit_text(st.screen,sentence)    

    def RESULTS(st, screen):
        if(not st.end):
            # time
            st.total_time = time.time() - st.time_start
               
            # accuracy
            count = 0
            for i,c in enumerate(st.word):       #comparision
                try:
                    if st.input_text[i] == c:
                        count += 1
                except:
                    pass
            st.accuracy = count/len(st.word)*100
           
            # words per minute
            st.wpm = len(st.input_text)*60/(5*st.total_time)
            st.end = True
            print(st.total_time)
                                       #print till only 2 dec                      
            st.results = 'Time:'+str(round(st.total_time,2)) +" secs   Accuracy:"+ str(round(st.accuracy)) + "%" + '   Wpm: ' + str(round(st.wpm))
            st.showsentence(screen,"Reset", st.height - 70, 26, (211,211,211))
            print(st.results)
            pygame.display.update()

    def run(st):#changing size of input box
        st.reset_game()
        st.running=True
        while(st.running):
            clock = pygame.time.Clock()
            st.screen.fill((0,0,0), (25,250,850,50))
            pygame.draw.rect(st.screen,st.HEAD_C, (0,0,0,0),1)
            st.showsentence(st.screen, st.input_text, 274, 26,(250,250,250))    # putting my input into it
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    st.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # position of input box
                    if(x>=50 and x<=650 and y>=250 and y<=300):
                        st.active = True
                        st.input_text = ''
                        st.time_start = time.time() 
                     # position of reset box
                    if(x>=310 and x<=510 and y>=390 and st.end):
                        st.reset_game()
                        x,y = pygame.mouse.get_pos()
         
                        
                elif event.type == pygame.KEYDOWN:
                    if st.active and not st.end:
                        if event.key == pygame.K_RETURN:
                            print(st.input_text)
                            st.RESULTS(st.screen)
                            print(st.results)
                            st.showsentence(st.screen, st.results,350, 28, st.RESULT_C)  
                            st.end = True
                            
                        elif event.key == pygame.K_BACKSPACE:
                            st.input_text = st.input_text[:-1]
                        else:
                            try:
                                st.input_text += event.unicode
                            except:
                                pass
            
            pygame.display.update()
             
                
        clock.tick(60)

    def reset_game(st):
        time.sleep(1)
        
        st.reset=False
        st.end = False

        st.input_text=''
        st.word = ''
        st.time_start = 0
        st.total_time = 0
        st.wpm = 0

        # random sentence 
        st.word = st.randomoutput()
        if (not st.word): st.reset_game()
        st.screen.fill((50,50,50))      #head

        msg = "100SHI Typing Speed Test"
        st.showsentence(st.screen, msg,80, 60,st.HEAD_C)  
        # draw the rectangle for input box
        pygame.draw.rect(st.screen,(0,0,0), (25,250,850,50), 1)

        st.showsentence(st.screen, st.word,200, 25,st.TEXT_C) #myinput
        
        pygame.display.update()

def main_menu():
    
    menu=True
    selected="start"
 
    while menu:
       
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                quit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_UP:
                    selected="start"
                elif e.key==pygame.K_DOWN:
                    selected="quit"
                if e.key==pygame.K_RETURN:
                    if selected=="start":
                        print("Start")
                        Test().run()           #calling Game 
                    if selected=="quit":
                        pygame.quit()
                        quit()
                   
 
        # Main Menu UI
        screen.fill(gray)
        title=text_format("100SHI Typing Speed Test", font, 90, yellow)
        if selected=="start":
            text_start=text_format("START", font, 75, white)
        else:
            text_start = text_format("START", font, 75, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, black)
 
        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
 
        # Main Menu Text
        screen.blit(title, (180, 80))
        screen.blit(text_start, (355, 300))
        screen.blit(text_quit, (355, 360))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("100shi Typing Test")
        
main_menu()
pygame.quit()
quit()

