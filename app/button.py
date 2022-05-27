import pygame_widgets
from pygame_widgets.button import Button
from settings.settings import *
import pygame

class AppButton():
    def __init__(self):
        pass
    
    def add_button_play(self, h, w, screen, game):
        button_play = Button(screen,
                             h,
                             w,
                             200,
                             45,
                             text='play',
                             textColour=PLAYER_COLOR,
                             font=pygame.font.Font('fonts/emulogic.ttf', 23),
                             fontSize=23,
                             margin=20,
                             inactiveColour=BLACK,
                             hoverColour=BLUE,
                             pressedColour=BLUE,
                             onClick=game.button_play)
    
    def add_button_hs_table(self, h, w, screen, game):
        button_hs_table = Button(screen,
                                 h,
                                 w,
                                 200,
                                 45,
                                 text='hs table',
                                 textColour=PLAYER_COLOR,
                                 font=pygame.font.Font('fonts/emulogic.ttf', 23),
                                 fontSize=23,
                                 margin=20,
                                 inactiveColour=BLACK,
                                 hoverColour=BLUE,
                                 pressedColour=BLUE,
                                 onClick=game.button_hs_table)
    
    def add_button_rules(self, h, w, screen, game):
        button_rules = Button(screen,
                              h,
                              w,
                              200,
                              45,
                              text='rules',
                              textColour=PLAYER_COLOR,
                              font=pygame.font.Font('fonts/emulogic.ttf', 23),
                              fontSize=23,
                              margin=20,
                              inactiveColour=BLACK,
                              hoverColour=BLUE,
                              pressedColour=BLUE,
                              onClick=game.button_rules)
    
    def add_button_exit(self, h, w, screen, game):
        button_exit = Button(screen,
                             h,
                             w,
                             200,
                             45,
                             text='exit',
                             textColour=PLAYER_COLOR,
                             font=pygame.font.Font('fonts/emulogic.ttf', 23),
                             fontSize=23,
                             margin=20,
                             inactiveColour=BLACK,
                             hoverColour=BLUE,
                             pressedColour=BLUE,
                             onClick=game.button_exit)
    
    def add_button_back(self, h, w, screen, game):
        button_back = Button(screen,
                             h,
                             w,
                             200,
                             45,
                             text='back',
                             textColour=PLAYER_COLOR,
                             font=pygame.font.Font('fonts/emulogic.ttf', 23),
                             fontSize=23,
                             margin=20,
                             inactiveColour=BLACK,
                             hoverColour=BLUE,
                             pressedColour=BLUE,
                             onClick=game.button_back)
        
    def add_button_play_again(self, h, w, screen, game):
        button_play_again = Button(screen,
                                   h,
                                   w,
                                   220,
                                   45,
                                   text='play again',
                                   textColour=PLAYER_COLOR,
                                   font=pygame.font.Font('fonts/emulogic.ttf', 23),
                                   fontSize=23,
                                   margin=20,
                                   inactiveColour=BLACK,
                                   hoverColour=BLUE,
                                   pressedColour=BLUE,
                                   onClick=game.button_play_again)