"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)
import numpy as np
def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()
    Frames = []
    Balls_x = []
    Balls_y = []
    Bricks_x=[]
    Bricks_y=[]
    ball_willbe_x=100
    ball_willbe_y=400
    PlatformPos = []
    vectors_x=0
    vectors_y=0
  
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information
        ball_x=scene_info.ball[0]
        ball_y=scene_info.ball[1]
        bricks=scene_info.bricks
        platform_x=scene_info.platform[0]
        platform_y=scene_info.platform[1]      
      
                
            
        Balls_x.append(ball_x)
        Balls_y.append(ball_y)
        
       
        if len(Balls_x)>2:
            vectors_x=Balls_x[-1]-Balls_x[-2]
            vectors_y=Balls_y[-1]-Balls_y[-2]
        #Balls_next_x = np.array(Balls[1:])
        #vectors = Balls_next - Balls[:-1]
        #last_x=int(vectors[-1:,:-1]) 抓最後一個 但是會持續變動
        #last_y=int(vectors[-1:,1:])
            if vectors_y != 0:
                if vectors_y<0:
                    vectors_y*=-1
                time=(platform_y-ball_y)/vectors_y
                ball_willbe_x=ball_x+(vectors_x*time)
        #200,0 最右邊跟最左邊
            #最上面395
        tempbrick_x=ball_x
        tempbrick_y=ball_y
        tempvectors_x=vectors_x
        
        j=0
        for j in range(len(scene_info.bricks)):
            if scene_info.bricks[j][1]-ball_y>0 :
               if ball_x+((scene_info.bricks[j][1]-ball_y)/vectors_y)*vectors_x<scene_info.bricks[j][0]+2 or ball_x+((scene_info.bricks[j][1]-ball_y)/vectors_y)*vectors_x>scene_info.bricks[j][0]-2: 
                 if ball_willbe_x<scene_info.bricks[j][0] and vectors_x<0:
                    ball_willbe_x=scene_info.bricks[j][0]+(scene_info.bricks[j][0]-ball_willbe_x)
                    tempbrick_y=scene_info.bricks[j][1]
                    tempbrick_x=scene_info.bricks[j][0]
                    tempvectors_x=vectors_x*-1
                    break
                 elif ball_willbe_x>scene_info.bricks[j][0] and vectors_x>0:
                    ball_willbe_x=scene_info.bricks[j][0]-(ball_willbe_x-scene_info.bricks[j][0])
                    tempbrick_y=scene_info.bricks[j][1]
                    tempbrick_x=scene_info.bricks[j][0]
                    tempvectors_x=vectors_x*-1
                    break
        j=0
        if len(scene_info.hard_bricks)!=0:
            for j in range(len(scene_info.hard_bricks)):
                if scene_info.hard_bricks[j][1]-ball_y>0 :
                    if ball_x+((scene_info.hard_bricks[j][1]-ball_y)/vectors_y)*vectors_x<scene_info.hard_bricks[j][0]+2 or ball_x+((scene_info.hard_bricks[j][1]-ball_y)/vectors_y)*vectors_x>scene_info.hard_bricks[j][0]-2: 
                      if ball_willbe_x<scene_info.hard_bricks[j][0] and vectors_x<0:
                        ball_willbe_x=scene_info.hard_bricks[j][0]+(scene_info.hard_bricks[j][0]-ball_willbe_x)
                        tempbrick_y=scene_info.hard_bricks[j][1]
                        tempbrick_x=scene_info.hard_bricks[j][0]
                        tempvectors_x=vectors_x*-1
                        break
                      elif ball_willbe_x>scene_info.hard_bricks[j][0] and vectors_x>0:
                        ball_willbe_x=scene_info.hard_bricks[j][0]-(ball_willbe_x-scene_info.hard_bricks[j][0])
                        tempbrick_y=scene_info.hard_bricks[j][1]
                        tempbrick_x=scene_info.hard_bricks[j][0]
                        tempvectors_x=vectors_x*-1
                        break
        j=0
        for j in range(len(scene_info.bricks)):
            if scene_info.bricks[j][1]-ball_y>0:
                if tempbrick_x+((scene_info.bricks[j][1]-tempbrick_y)/vectors_y)*tempvectors_x<scene_info.bricks[j][0]+2 or tempbrick_x+((scene_info.bricks[j][1]-tempbrick_y)/vectors_y)*tempvectors_x>scene_info.bricks[j][0]-2 :
                 if ball_willbe_x<scene_info.bricks[j][0] and vectors_x<0:
                    ball_willbe_x=scene_info.bricks[j][0]+(scene_info.bricks[j][0]-ball_willbe_x)
                    tempbrick_y=scene_info.bricks[j][1]
                    tempbrick_x=scene_info.bricks[j][0]
                    tempvectors_x=vectors_x*-1
                    break
                 elif ball_willbe_x>scene_info.bricks[j][0] and vectors_x>0:
                    ball_willbe_x=scene_info.bricks[j][0]-(ball_willbe_x-scene_info.bricks[j][0])
                    tempbrick_y=scene_info.bricks[j][1]
                    tempbrick_x=scene_info.bricks[j][0]
                    tempvectors_x=vectors_x*-1
                    break
            
      
            
        j=0
        if len(scene_info.hard_bricks)!=0:
            for j in range(len(scene_info.hard_bricks)):
                if scene_info.hard_bricks[j][1]-ball_y>0 and tempbrick_x+((scene_info.hard_bricks[j][1]-tempbrick_y)/vectors_y)*tempvectors_x==scene_info.hard_bricks[j][0]:
                    if ball_willbe_x<scene_info.hard_bricks[j][0] and vectors_x<0:
                        ball_willbe_x=scene_info.hard_bricks[j][0]+(scene_info.hard_bricks[j][0]-ball_willbe_x)
                        tempbrick_y=scene_info.hard_bricks[j][1]
                        tempbrick_x=scene_info.hard_bricks[j][0]
                        tempvectors_x=vectors_x*-1
                        break
                    elif ball_willbe_x>scene_info.hard_bricks[j][0] and vectors_x>0:
                        ball_willbe_x=scene_info.hard_bricks[j][0]-(ball_willbe_x-scene_info.hard_bricks[j][0])
                        tempbrick_y=scene_info.hard_bricks[j][1]
                        tempbrick_x=scene_info.hard_bricks[j][0]
                        tempvectors_x=vectors_x*-1
                        break
                          
        j=0
        for j in range(len(scene_info.bricks)):
            if scene_info.bricks[j][1]-ball_y>0 and tempbrick_x+((scene_info.bricks[j][1]-tempbrick_y)/vectors_y)*tempvectors_x==scene_info.bricks[j][0]:
                if ball_willbe_x<scene_info.bricks[j][0] and vectors_x<0:
                    ball_willbe_x=scene_info.bricks[j][0]+(scene_info.bricks[j][0]-ball_willbe_x)
                    tempbrick_y=scene_info.bricks[j][1]
                    tempbrick_x=scene_info.bricks[j][0]
                    tempvectors_x=vectors_x*-1
                    break
                elif ball_willbe_x>scene_info.bricks[j][0] and vectors_x>0:
                    ball_willbe_x=scene_info.bricks[j][0]-(ball_willbe_x-scene_info.bricks[j][0])
                    tempbrick_y=scene_info.bricks[j][1]
                    tempbrick_x=scene_info.bricks[j][0]
                    tempvectors_x=vectors_x*-1
                    break
            
      
            
        j=0
        if len(scene_info.hard_bricks)!=0:
            for j in range(len(scene_info.hard_bricks)):
                if scene_info.hard_bricks[j][1]-ball_y>0 and tempbrick_x+((scene_info.hard_bricks[j][1]-tempbrick_y)/vectors_y)*tempvectors_x==scene_info.hard_bricks[j][0]:
                    if ball_willbe_x<scene_info.hard_bricks[j][0] and vectors_x<0:
                        ball_willbe_x=scene_info.hard_bricks[j][0]+(scene_info.hard_bricks[j][0]-ball_willbe_x)
                        tempbrick_y=scene_info.hard_bricks[j][1]
                        tempbrick_x=scene_info.hard_bricks[j][0]
                        tempvectors_x=vectors_x*-1
                        break
                    elif ball_willbe_x>scene_info.hard_bricks[j][0] and vectors_x>0:
                        ball_willbe_x=scene_info.hard_bricks[j][0]-(ball_willbe_x-scene_info.hard_bricks[j][0])
                        tempbrick_y=scene_info.hard_bricks[j][1]
                        tempbrick_x=scene_info.hard_bricks[j][0]
                        tempvectors_x=vectors_x*-1
                        break
        if ball_willbe_x<0:
            temp=0-ball_willbe_x
            ball_willbe_x=temp
         
        elif ball_willbe_x>195:
            temp=ball_willbe_x-195
            ball_willbe_x=195-temp
     
        
        # 3.4. Send the instruction for this frame to the game process
     
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        else:                     
            if ball_willbe_x>platform_x+25:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                
               
            elif ball_willbe_x<platform_x+25:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
    
            else:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
