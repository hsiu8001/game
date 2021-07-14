#遊戲規則：控制妹子以躲避考卷，吃到仙女時可藉由觸碰消滅考卷

import pygame, random, sys, time                    #引用函式庫
from pygame.locals import *                         #引用函式庫

#------------------------------設定常數------------------------------

WINDOWWIDTH = 500                                   #設定視窗寬度
WINDOWHEIGHT = 360                                  #設定視窗高度
TEXTCOLOR = (255, 0, 0)                             #文字顏色為紅色
BACKGROUNDCOLOR = (255, 255, 255)                   #背景顏色為白色
FPS = 100                                           #程式畫面更新速度

ARTICLESIZE = 50                                    #物件尺寸
ARTICLEMINSPEED = 1                                 #物件移動最小速度
ARTICLEMAXSPEED = 2                                 #物件移動最大速度
ADDNEWARTICLERATE = 225                             #新增物件的頻率
PLAYERMOVERATE = 5                                  #玩家移動速度(鍵盤控制用)

DOWNLEFT = 'downleft'                               #物件移動方向-左下
DOWNRIGHT = 'downright'                             #物件移動方向-右下
UPLEFT = 'upleft'                                   #物件移動方向-左上
UPRIGHT = 'upright'                                 #物件移動方向-右上
direction = [DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT]  #將方向存成串列

flag = 0                                            #偵測遊玩模式
supertime = 100                                     #設定super time時長

#------------------------------定義函式------------------------------

def terminate():                                    #結束程式
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():                      #暫停遊戲等待玩家按鍵
    while True:
        for event in pygame.event.get():            #偵測事件發生
            if event.type == QUIT:                  #關閉視窗則程式結束
                terminate()
            if event.type == KEYDOWN:               #如果有按下按鍵
                if event.key == K_ESCAPE:           #按下ESC鍵則程式結束
                    terminate()
                elif event.key == K_SPACE:          #按下空白鍵則繼續遊戲
                    return

def drawText(text, font, surface, x, y):            #繪製文字
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

#-------------------------初始化pygame和設定視窗-------------------------

pygame.init()                                       #pygame初始化
mainClock = pygame.time.Clock()                     #設定調整程式執行速度之物件
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('No Test')               #設定視窗橫軸標題

#------------------------------設定字型物件------------------------------

font = pygame.font.SysFont("comicsansms", 32)           #設定字型/大小

#------------------------------設定音效物件------------------------------

pygame.mixer.music.load('D:/Coding/1206 NoTest/NoTest/BGM.mp3')                      #設定背景音樂
gameSuccessSound = pygame.mixer.Sound('D:/Coding/1206 NoTest/NoTest/success.wav')    #設定遊戲成功音效
gameOverSound = pygame.mixer.Sound('D:/Coding/1206 NoTest/NoTest/failure.wav')       #設定遊戲失敗音效
supertimeSound = pygame.mixer.Sound('D:/Coding/1206 NoTest/NoTest/exciting.mp3')     #設定super time音效
 
#------------------------------設定影像物件------------------------------

playerImage1 = pygame.image.load('D:/Coding/1206 NoTest/NoTest/bear.png')             #設定玩家圖像為妹子
playerImage2 = pygame.image.load('D:/Coding/1206 NoTest/NoTest/flower.png')           #設定妹子失敗圖像
fairyImage = pygame.image.load('D:/Coding/1206 NoTest/NoTest/fairy .png')             #設定仙女圖像
playerRect = playerImage1.get_rect()                     #玩家為妹子圖像的Rect物件
testImage = pygame.image.load('D:/Coding/1206 NoTest/NoTest/test.png')                #設定考卷圖像
backgroundImage = pygame.image.load('D:/Coding/1206 NoTest/NoTest/background.jpg')    #設定背景圖像
startImage = pygame.image.load('D:/Coding/1206 NoTest/NoTest/start.jpg')              #設定初始畫面
successImage = pygame.image.load('D:/Coding/1206 NoTest/NoTest/WIN.jpg')              #設定成功畫面
failImage = pygame.image.load('D:/Coding/1206 NoTest/NoTest/fail.jpg')                #設定失敗畫面

#------------------------------顯示起始畫面------------------------------

pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT + 140)).blit(startImage, (0,0))
pygame.display.update()                     #更新畫面
waitForPlayerToPressKey()                   #暫停遊戲等待玩家按鍵

#------------------------------主程式開始------------------------------

while True:                                 #主程式是個無窮迴圈
    GameTime = 2000                         #設定遊戲時間(在FPS為2000的情形下約20秒)
    GameStart = True                        #預設遊戲狀態為執行(True)
    
    tests = []                              #宣告新考卷字典物件的串列
    fairies = []                            #宣告仙女字典物件的串列
    
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)    #妹子初始位置在畫面中間
    moveLeft = moveRight = moveUp = moveDown = False            #鍵盤控制用的移動變數初始為False
    testAddCounter = 0                      #正常計數器初始為0
    fairyAddCounter = 0                     #super time計數器初始為0    
    pygame.mixer.music.play(-1, 0.0)        #重頭播放背景音樂且為循環播放
    
#------------------------------遊戲計時開始------------------------------
    
    while GameTime > 0 and GameStart == True:   #當遊戲時間未歸零的情形下遊戲進行
        GameTime -= 1                           #遊戲時間遞減
        if flag == 1:                           #偵測super time是否開始 
            supertime -= 1                      #super time時間遞減
        
        for event in pygame.event.get():        #偵測事件發生
            if event.type == QUIT:              #關閉視窗則程式結束
                terminate()
            
#------------------------------處理鍵盤事件------------------------------
            
            if event.type == KEYDOWN:                    #當有按下按鍵
                if event.key == K_LEFT:                  #當按下方向左鍵,調整移動變數
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT:                 #當按下方向右鍵,調整移動變數
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP:                    #當按下方向上鍵,調整移動變數
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN:                  #當按下方向下鍵,調整移動變數
                    moveUP = False
                    moveDown = True
            
            if event.type == KEYUP:                      #當有放開按鍵
                if event.key == K_ESCAPE:                #當放開鍵盤ESC時,程式結束
                    terminate()
                if event.key == K_LEFT:                  #當放開方向左鍵,調整移動變數
                    moveLeft = False
                if event.key == K_RIGHT:                 #當放開方向右鍵,調整移動變數
                    moveRight = False
                if event.key == K_UP:                    #當放開方向上鍵,調整移動變數
                    moveUp = False
                if event.key == K_DOWN:                  #當放開方向下鍵,調整移動變數
                    moveDown = False
            
#------------------------------處理滑鼠事件------------------------------
            
            if event.type == MOUSEMOTION:                #當滑鼠移動時,移動玩家至游標處
                if event.pos[0] - ARTICLESIZE/2 >= 0 and event.pos[0] + ARTICLESIZE/2 <= WINDOWWIDTH and event.pos[1] - ARTICLESIZE/2 >= 0 and event.pos[1] + ARTICLESIZE/2 <= WINDOWHEIGHT:
                    playerRect.centerx = event.pos[0]
                    playerRect.centery = event.pos[1]
            
#-----------------------偵測事件結束,移動妹子位置(鍵盤)-----------------------
        
        if moveLeft and playerRect.left > 0:             #當玩家在畫面中且有移動時,改變位置
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)
        
#------------------------------新增考卷------------------------------
        
        testAddCounter += 1                              #考卷計數累加
        if testAddCounter == ADDNEWARTICLERATE:          #當達到預設之新增物件的頻率時
            testAddCounter = 0                           #累加計數歸0
            newtest = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - ARTICLESIZE), 0 - ARTICLESIZE, ARTICLESIZE, ARTICLESIZE),
                      'speed': random.randint(ARTICLEMINSPEED, ARTICLEMAXSPEED),
                      'dir': direction[random.randint(0, 1)]}
            tests.append(newtest)                         #新增新考卷字典物件並放到串列中
            
#------------------------------移動考卷------------------------------
        
        for c in tests:                                  #考卷從天而降,依方向進行移動
            if c['dir'] == DOWNLEFT:
                c['rect'].left -= c['speed']
                c['rect'].top += c['speed']
            if c['dir'] == DOWNRIGHT:
                c['rect'].left += c['speed']
                c['rect'].top += c['speed']
            if c['dir'] == UPLEFT:
                c['rect'].left -= c['speed']
                c['rect'].top -= c['speed']
            if c['dir'] == UPRIGHT:
                c['rect'].left += c['speed']
                c['rect'].top -= c['speed']

            if c['rect'].top < 0:                       #考卷碰到邊界反彈
                if c['dir'] == UPLEFT:
                    c['dir'] = DOWNLEFT
                if c['dir'] == UPRIGHT:
                    c['dir'] = DOWNRIGHT
            if c['rect'].bottom > WINDOWHEIGHT:
                if c['dir'] == DOWNLEFT:
                    c['dir'] = UPLEFT
                if c['dir'] == DOWNRIGHT:
                    c['dir'] = UPRIGHT
            if c['rect'].left < 0:
                if c['dir'] == DOWNLEFT:
                    c['dir'] = DOWNRIGHT
                if c['dir'] == UPLEFT:
                    c['dir'] = UPRIGHT
            if c['rect'].right > WINDOWWIDTH:
                if c['dir'] == DOWNRIGHT:
                    c['dir'] = DOWNLEFT
                if c['dir'] == UPRIGHT:
                    c['dir'] = UPLEFT
            
#------------------------------考卷碰撞偵測------------------------------
        
        for c in tests:

            if flag == 0:
                
                if playerRect.colliderect(c['rect']):       #當玩家碰到考卷
                    GameStart = False;                      #遊戲狀態為不執行(False)
                    break;                                  #迴圈中斷表示遊戲結束(失敗)
        
#------------------------------新增仙女------------------------------
        
        fairyAddCounter += 1                                #仙女計數累加
        if fairyAddCounter == ADDNEWARTICLERATE*3:          #當達到預設之新增物件的頻率時
            fairyAddCounter = 0                             #累加計數歸0
            newfairy = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - ARTICLESIZE), 0 - ARTICLESIZE, ARTICLESIZE, ARTICLESIZE),
                      'speed': random.randint(ARTICLEMINSPEED, ARTICLEMAXSPEED),
                      'dir': direction[random.randint(0, 1)]}
            fairies.append(newfairy)                        #新增新仙女字典物件並放到串列中
            
#------------------------------移動仙女------------------------------
        
        for c in fairies:                                   #仙女從天而降,依方向進行移動
            if c['dir'] == DOWNLEFT:
                c['rect'].left -= c['speed']
                c['rect'].top += c['speed']
            if c['dir'] == DOWNRIGHT:
                c['rect'].left += c['speed']
                c['rect'].top += c['speed']
            if c['dir'] == UPLEFT:
                c['rect'].left -= c['speed']
                c['rect'].top -= c['speed']
            if c['dir'] == UPRIGHT:
                c['rect'].left += c['speed']
                c['rect'].top -= c['speed']

            if c['rect'].top < 0:                           #仙女碰到邊界反彈
                if c['dir'] == UPLEFT: 
                    c['dir'] = DOWNLEFT
                if c['dir'] == UPRIGHT:
                    c['dir'] = DOWNRIGHT
            if c['rect'].bottom > WINDOWHEIGHT:
                if c['dir'] == DOWNLEFT:
                    c['dir'] = UPLEFT
                if c['dir'] == DOWNRIGHT:
                    c['dir'] = UPRIGHT
            if c['rect'].left < 0:
                if c['dir'] == DOWNLEFT:
                    c['dir'] = DOWNRIGHT
                if c['dir'] == UPLEFT:
                    c['dir'] = UPRIGHT
            if c['rect'].right > WINDOWWIDTH:
                if c['dir'] == DOWNRIGHT:
                    c['dir'] = DOWNLEFT
                if c['dir'] == UPRIGHT:
                    c['dir'] = UPLEFT
            
#------------------------------仙女碰撞偵測------------------------------
        for f in fairies:
                           
            if playerRect.colliderect(f['rect']):            #當玩家撞到仙女
                
                fairies.remove(f)                            #移去仙女圖檔
                flag = 1                                     #開啟super time模式
                
                backgroundImage = pygame.image.load('D:/Coding/1206 NoTest/NoTest/special background.jpg')  #換super time背景
                supertimeSound.play()                                          #換super time音樂

        
            
        if flag == 1 and supertime > 0:

            for t in tests:    

                if playerRect.colliderect(t['rect']):                       #當碰撞到考卷
                    tests.remove(t)                                         #移除考卷
                            
        elif supertime < 0:                                                 #當super time結束
            flag = 0                                                        #回到普通模式
            supertime = 100                                                 #下一個super time的間隔////////
            backgroundImage = pygame.image.load('D:/Coding/1206 NoTest/NoTest/background.jpg')           #回到普通背景
            supertimeSound.stop()                                           #回到普通音效
                                        
#------------------------------繪製視窗------------------------------
        
        pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)).blit(backgroundImage, (0, 0))                         #畫出背景圖
        
        drawText('Time: %s' % (GameTime/100), font, windowSurface, 8, 0)   #繪製文字
        if supertime < 100:
            drawText('superTime: %s' % (supertime/100), font, windowSurface, 8, 30)
        
        for c in tests:                                                     #畫出考卷
            windowSurface.blit(testImage, c['rect'])

        for c in fairies:                                                   #畫出仙女
            windowSurface.blit(fairyImage, c['rect'])    
        
        windowSurface.blit(playerImage1, playerRect)                        #畫出妹子
        if GameStart == False:
             windowSurface.blit(playerImage2,playerRect)                    #失敗則畫出妹子失敗圖
        
        pygame.display.update()                                             #更新畫面
        mainClock.tick(FPS)                                                 #設定程式執行速度
        
#-------------------------遊戲計時結束,顯示遊戲結果-------------------------
    
    pygame.mixer.music.stop()                     #停止背景音樂
    
    if GameStart == True:                         #時間到後仍活著為過關
        gameSuccessSound.play()                   #播放成功音效與顯示成功圖片
        pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT + 300)).blit(successImage, (0, 0))
    else:                                         #反之為失敗
        gameOverSound.play()                      #播放失敗音效與顯示失敗圖片
        pygame.display.set_mode((WINDOWWIDTH + 70, WINDOWHEIGHT + 60)).blit(failImage, (0, 0))
            
    pygame.display.update()                       #更新畫面
    waitForPlayerToPressKey()                     #等待玩家按鍵繼續
    gameSuccessSound.stop()                       #關閉音效
    gameOverSound.stop()                          #關閉音效

#------------------------------主程式結束------------------------------
