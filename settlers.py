import pygame
import random

pygame.init()

# Create the screen
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.font.init()
bg = pygame.image.load("assets/Dice Game.png")


# Class to draw Roll button
class Button (object):
    def __init__ (self, screen, width, height, x, y):
        self.__screen = screen
        self._width = width
        self._height = height
        self._xLoc = x
        self._yLoc = y
        w, h = pygame.display.get_surface().get_size()
        self.__W = w
        self.__H = h


    def draw(self):
        # Button
        pygame.draw.rect(screen, (0,0,0), (self._xLoc,self._yLoc,self._width,self._height),0)
        # Text
        myfont = pygame.font.SysFont(None, 30)
        textsurface = myfont.render('Roll', False, (255, 255, 255))
        screen.blit(textsurface,(self._xLoc+20,self._yLoc+15))

    def reset(self):
        myfont = pygame.font.SysFont(None, 20)
        textsurface = myfont.render('Reset', False, (0,0,0))
        screen.blit(textsurface,(440, 570))

    def reset_pressed(self, pos):
        if (pos[0] >= 440) & (pos[0] <= 440 + 30):
            if (pos[1] >= 570) & (pos[1] <= 570 + 10):
                return True

# Contains most of the game's logic
class Dice(object):
    def __init__ (self, screen, width, height, x, y):
        self.__screen = screen
        self._width = width
        self._height = height
        self._xLoc = x
        self._yLoc = y
        w, h = pygame.display.get_surface().get_size()
        self.__W = w
        self.__H = h
        self.positions = {1:[None,'roll',[0,0,0,0]],2:[None,'roll',[0,0,0,0]],3:[None,'roll',[0,0,0,0]],
                          4:[None,'roll',[0,0,0,0]],5:[None,'roll',[0,0,0,0]],6:[None,'roll',[0,0,0,0]]}
        self.roll_count = 0
        self.rec_total = {'sheep': 0, 'wheat': 0, 'ore': 0, 'brick': 0, 'wood': 0, 'gold': 0}
        self.soldiers = {'sheep': 0, 'wheat': 0, 'ore': 0, 'brick': 0, 'wood': 0, 'gold': 0}
        self.dice_throw = 0
        self.turn = 1
        self.score = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}
    

    def dice_outline(self):
        for i in range(6):
            x = 85*i - 60
            pygame.draw.rect(screen, (69, 69, 69), (self._xLoc,self._yLoc + x + self._width,self._width,self._height), 5)
            self.positions[(i+1)][2] = [self._xLoc,self._yLoc + x + self._width,self._width,self._height]
            

    def show_roll(self):
        for i in self.positions:
            if self.positions[i][0] is not None:
                value = 'assets/' + self.positions[i][0] + '.png'
            else:
                value = 'assets/blank.png'
            x =85*i - 60
            myfont = pygame.font.SysFont(None, 25)
            picture = pygame.image.load(value)
            screen.blit(picture,(self._xLoc+5,self._yLoc + x + 5))

    def count_recs(self):
        for i in self.rec_total:
            self.rec_total[i] = 0
        for x in self.positions:
            self.rec_total[self.positions[x][0]] += 1


    def roll_dice(self):
        self.throw()
        items = ['sheep', 'wheat', 'ore', 'brick', 'wood', 'gold']
        for i in self.positions:
            if self.positions[i][1] in ['roll']:
                dice_num = random.randint(0,5)
                self.positions[i][0] = items[dice_num]
        self.count_recs()
        

    def freeze_dice(self, click_cord):
        for i in self.positions:
            if ((click_cord[0] >= self.positions[i][2][0]) and 
               (click_cord[0] <= self.positions[i][2][0] + self.positions[i][2][2])):
               if ((click_cord[1] >= self.positions[i][2][1]) and 
                  (click_cord[1] <= self.positions[i][2][1] + self.positions[i][2][3])):
                  if self.positions[i][1] == 'keep':
                      self.positions[i][1] = 'roll'
                  else:
                      self.positions[i][1] = 'keep'

    def is_selected(self, status, cords):
        if status=='keep':
            pygame.draw.rect(screen, (240, 233, 38),tuple(cords),5)
        else:
            pygame.draw.rect(screen, (69, 69, 69),tuple(cords),5)
    


    def throw(self):
        if self.dice_throw == 3:
            for i in self.positions:   
                self.positions[i][1] = 'roll'
            self.dice_throw = 1
            if self.score[self.turn] == 0:
                self.score[self.turn] = -2
            self.turn += 1    
        else:
            self.dice_throw += 1
    
    def show_throw(self):
        myfont = pygame.font.SysFont(None, 20)
        textsurface = myfont.render('Roll: '+str(self.dice_throw), False, (0,0,0))
        screen.blit(textsurface,(506, 570))

    def turn_counter(self):
        pygame.draw.rect(screen, (69, 69, 69), (600, 605 - (self.turn * 34), 22, 10))
        
    def show_score(self):
        myfont = pygame.font.SysFont(None, 20)
        for i in self.score:
            if self.score[i]:
                textsurface = myfont.render(str(self.score[i]), False, (0,0,0))
                screen.blit(textsurface,(655, 600 - (i * 34)))
        
        totalfont = pygame.font.SysFont(None, 40)
        total = totalfont.render(str(sum(self.score.values())), False, (0,0,0))
        screen.blit(total,(625, 25))


    def check(self, rec, rec_list):
        if rec_list[rec] > 0:
            return rec
        elif rec_list['gold'] > 1:
            return 'gold'
        else:
            return False


    def recs_available(self, recipe, totals, soldiers):
        wild_list = soldiers.copy()
        rec_list = totals.copy()
        for i in recipe:
            output = self.check(i, rec_list)
            if output == 'gold':
                rec_list['gold'] -= 2
            elif output is not False:
                rec_list[i] -= 1
            else:
                wilds = self.check(i, wild_list)
                if wilds == 'gold':
                    wild_list['gold'] -= 2
                elif wilds is not False:
                    wild_list[i] -= 1
                else:
                    return False, rec_list, wild_list
        return True, rec_list, wild_list


class Roads(object):
    def __init__(self, screen):
        self.__screen = screen
        self.positions = {1: [[207, 318],'blank','assets/road_right.png',0], 2:[[206, 380],'blank','assets/road_left.png',1],
                          3:[[149, 369],'blank','assets/road.png',1],4:[[207, 450],'blank','assets/road_right.png',2],
                          5:[[204, 509],'blank','assets/road_left.png',4],6:[[148, 498],'blank','assets/road.png',4],
                          7:[[263, 563],'blank','assets/road.png',5],8:[[317, 521],'blank','assets/road_right.png',7],
                          9:[[379, 496],'blank','assets/road.png',8],10:[[429, 453],'blank','assets/road_right.png',9],
                          11:[[430, 377],'blank','assets/road_left.png',10],12:[[430, 322],'blank','assets/road_right.png',11],
                          13:[[318, 444],'blank','assets/road_left.png',8],14:[[318, 385],'blank','assets/road_right.png',13],
                          15:[[317, 314],'blank','assets/road_left.png',14],16:[[318, 255],'blank','assets/road_right.png',15]}
        self.is_visible = [0]

    def road_build(self, pos):
        for i in self.positions:
            if (self.positions[i][3] in self.is_visible) & (self.positions[i][1] == 'blank'):
                if (pos[0] >= road.positions[i][0][0]) & (pos[0] <= road.positions[i][0][0] + 50):
                        if (pos[1] >= road.positions[i][0][1]) & (pos[1] <= road.positions[i][0][1] + 30):
                            road.positions[i][1] = 'fill'
                            if i not in road.is_visible:
                                road.is_visible.append(i)
                            return True


class House(object):
    def __init__(self, screen):
        self.__screen = screen
        self.positions = {1: [[228, 289],'blank',3,[0,0]], 2:[[229, 423],'blank',4,[1,2]],
                          3:[[230, 551],'blank',5,[2,5]], 4:[[342, 486],'blank',7,[3,8]],
                          5:[[342, 354],'blank',8,[4,14]], 6:[[343, 223],'blank',9,[5,16]]}
        self.is_visible = [0]

    def house_build(self, road, pos):
        for i in self.positions:
            if (self.positions[i][3][0] in self.is_visible) \
                & (self.positions[i][3][1] in road.is_visible) \
                & (self.positions[i][1] == 'blank'):
                if (pos[0] >= self.positions[i][0][0]) & (pos[0] <= self.positions[i][0][0] + 20):
                        if (pos[1] >= self.positions[i][0][1]) & (pos[1] <= self.positions[i][0][1] + 20):
                            self.positions[i][1] = 'fill'
                            if i not in self.is_visible:
                                self.is_visible.append(i)
                            return True

class City(object):
    def __init__(self, screen):
        self.__screen = screen
        self.positions = {1:[[111, 353],'blank',7,[0,3]], 2:[[109, 482],'blank',12,[1,6]],
                          3:[[450, 417],'blank',20,[2,10]], 4:[[449, 287],'blank',30,[3,12]]}
        self.is_visible = [0]

    def city_build(self, road, pos):
        for i in self.positions:
            if (self.positions[i][3][0] in self.is_visible) \
                & (self.positions[i][3][1] in road.is_visible) \
                & (self.positions[i][1] == 'blank'):
                if (pos[0] >= self.positions[i][0][0]) & (pos[0] <= self.positions[i][0][0] + 30):
                        if (pos[1] >= self.positions[i][0][1]) & (pos[1] <= self.positions[i][0][1] + 30):
                            self.positions[i][1] = 'fill'
                            if i not in self.is_visible:
                                self.is_visible.append(i)
                            return True

class Sodier(object):
    def __init__(self, screen):
        self.__screen = screen
        self.positions = {1:[[171, 320],'blank',1,0,'ore'], 2:[[177, 444],'blank',2,1,'wheat'],
                          3:[[281, 518],'blank',3,2,'sheep'], 4:[[401, 443],'blank',4,3,'wood'],
                          5:[[401, 317],'blank',5,4,'brick'], 6:[[285, 254],'blank',6,5,'gold']}
        self.is_purchased = [0]
        self.is_used = []

    def soldier_place(self, pos):
        for i in self.positions:
            if (self.positions[i][3] in self.is_purchased) \
                & (self.positions[i][3] not in self.is_used) \
                & (self.positions[i][1] == 'blank'):
                if (pos[0] >= self.positions[i][0][0]) & (pos[0] <= self.positions[i][0][0] + 20):
                        if (pos[1] >= self.positions[i][0][1]) & (pos[1] <= self.positions[i][0][1] + 20):
                            self.positions[i][1] = 'fill'
                            if i not in self.is_purchased:
                                self.is_purchased.append(i)
                            return True

    def logic(self, soldiers):
        for i in self.positions:
            if self.positions[i][1] == 'fill':
                if soldiers[self.positions[i][4]] == 0:
                    self.is_used.append(i)
                    self.positions[i][1] = 'used'



button = Button(screen,85,45,695,540)
die = Dice(screen,75,75,700,10)
road = Roads(screen)
house = House(screen)
soldier = Sodier(screen)
city = City(screen)
gameStatus = True # game is still running
pygame.display.set_caption("Catan - The Dice Game")
done = False
clock = pygame.time.Clock()

 
# -------- Main Program Loop -----------
while not done:
    
    # background image
    screen.fill((255,255,255))
    screen.blit(bg, (0, 0))

    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # --- Spacebar Roll
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                die.roll_dice()
                die.freeze_dice((733, 563))

        # --- Mouse Click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Click to roll
            if (pos[0] > button._xLoc) & (pos[0] < button._xLoc+60):
                if (pos[1] > button._yLoc) & (pos[1] < button._yLoc+40):
                    die.roll_dice()
            die.freeze_dice(pos)

            # Reset button
            if button.reset_pressed(pos) is True:
                die.turn = 16
            
            # Purchasing Road
            if die.recs_available(['wood','brick'], die.rec_total, die.soldiers)[0] == True:            
                if road.road_build(pos):
                    die.rec_total, die.soldiers = die.recs_available(['wood','brick'], die.rec_total, die.soldiers)[1:]
                    die.score[die.turn] += 1
                    die.dice_throw = 3
            
            # Purchasing House
            if die.recs_available(['wood','brick','wheat','sheep'], die.rec_total, die.soldiers)[0] == True:            
                if house.house_build(road, pos):
                    die.rec_total, die.soldiers = die.recs_available(['wood','brick','wheat','sheep'], die.rec_total,die.soldiers)[1:]
                    die.score[die.turn] += house.positions[house.is_visible[-1]][2]
                    die.dice_throw = 3

            # Purchasing City
            if die.recs_available(['ore','ore','ore','wheat','wheat'], die.rec_total, die.soldiers)[0] == True:            
                if city.city_build(road, pos):
                    die.rec_total, die.soldiers = die.recs_available(['ore','ore','ore','wheat','wheat'], die.rec_total, die.soldiers)[1:]
                    die.score[die.turn] += city.positions[city.is_visible[-1]][2]
                    die.dice_throw = 3

            # Purchasing Solier
            if die.recs_available(['sheep','ore','wheat'], die.rec_total, die.soldiers)[0] == True:            
                if soldier.soldier_place(pos):
                    die.rec_total, die.soldiers = die.recs_available(['sheep','ore','wheat'], die.rec_total, die.soldiers)[1:]
                    die.score[die.turn] += soldier.positions[soldier.is_purchased[-1]][2]
                    if soldier.is_purchased[-1] < 6:
                        die.soldiers[soldier.positions[soldier.is_purchased[-1]][4]] = 1
                    elif soldier.is_purchased[-1] == 6:
                        die.soldiers[soldier.positions[soldier.is_purchased[-1]][4]] = 2
                    die.dice_throw = 3
            soldier.logic(die.soldiers)


    
    # --- Display Stuff
    if gameStatus:
        button.draw()
        button.reset()

        # Updating Dice Images
        die.dice_outline()
        die.show_roll()
        for i in die.positions:
            if die.positions[i][1] == 'keep':
                die.is_selected('keep', die.positions[i][2])
            elif die.positions[i][1] == 'freeze':
                die.is_selected('freeze', die.positions[i][2])
        die.show_throw()
        die.turn_counter()
        die.show_score()

        # Display Roads
        for r_num in road.positions:
            if road.positions[r_num][1] == 'fill':
                road_place = pygame.image.load(road.positions[r_num][2])
                screen.blit(road_place, tuple(road.positions[r_num][0]))

        # Display Houses
        for h_num in house.positions:
            if house.positions[h_num][1] == 'fill':
                house_place = pygame.image.load('assets/house.png')
                screen.blit(house_place, tuple(house.positions[h_num][0]))

        # Display Cities
        for c_num in city.positions:
            if city.positions[c_num][1] == 'fill':
                city_place = pygame.image.load('assets/city.png')
                screen.blit(city_place, tuple(city.positions[c_num][0]))

        # Display Soliers
        for s_num in soldier.positions:
            if soldier.positions[s_num][1] == 'fill':
                soldier_place = pygame.image.load('assets/sold_unused.png')
                screen.blit(soldier_place, tuple(soldier.positions[s_num][0]))
            elif soldier.positions[s_num][1] == 'used':
                soldier_place = pygame.image.load('assets/sold_used.png')
                screen.blit(soldier_place, tuple(soldier.positions[s_num][0]))

        if die.turn == 16:
            die.turn = 1
            die.score = dict.fromkeys(die.score, 0)


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 10 frames per second
    clock.tick(5)
 
# Close the window and quit.
pygame.quit()