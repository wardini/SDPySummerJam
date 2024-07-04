import os
import pygame
import json
from level_editor.txt_item import Txt_item
import glob
from level_editor.level_methods import load_level,save_level
from level_editor.level_objects import Point,Segment

class Editor:
    def __init__(self,glbls):
        self.done = False
        self.quit = False
        self.next_state = None
        self.glbls = glbls

        with open("constellations/constellations.json","r") as f:
            self.const_names = json.load(f)

        self.lev_num = 0

        bottom = self.glbls["HEIGHT"] - 30

        self.texts = [
            Txt_item("Star Editor",(10,10),True,"Star Mode",fontsize=26),
            Txt_item("Constellation Editor",(170,10),True,"Segment Mode",fontsize=26),
            Txt_item("Solution",(470,10),True,"Swap Images",fontsize=26),
            Txt_item("----",(670,10),False,"None",fontsize=26),
            Txt_item("Quit",(970,10),True,"Quit",fontsize=26),
            Txt_item("Save",(1080,bottom),True,"Save",fontsize=26),
            Txt_item("Load File Up",(150,bottom),True,"File Up",fontsize=26),
            Txt_item("Load File Down",(300,bottom),True,"File Down",fontsize=26),
            Txt_item(self.const_names[self.lev_num],(10,bottom),False,None,fontsize=26),
        ]

    def startup(self):
        self.graphic,self.solution_graphic,self.info = load_level(self.const_names[self.lev_num],self.glbls)
        self.drag_mode = False
        self.use_solution = False
        self.star_mode = True
        self.texts[0].highlight()
        self.segment_mode1 = False
        self.segment_mode2 = False
        self.stars = []
        for xy in self.info["stars"]:
            self.stars.append(Point(*xy))
        self.segments = []
        for s in self.info["segments"]:
            self.segments.append(Segment(self.stars[s[0]]))
            self.segments[-1].add_star(self.stars[s[1]])
        self.point_selected = None

    def update(self,dt):
        pass

    def get_event(self, event):
        if self.drag_mode:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.drag_mode = False
                    return
            if self.point_selected:
                self.point_selected.new_location(*pygame.mouse.get_pos())
            return

        elif event.type == pygame.QUIT:
            self.done = True
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.done = True
                self.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                for t in self.texts:
                    if t.check_select(event.pos):
                        if t.action == "Star Mode":
                            if self.segment_mode2:
                                self.segments.pop()
                            self.star_mode = True
                            self.segment_mode1 = False
                            self.segment_mode2 = False
                            self.texts[0].highlight()
                            self.texts[1].unhighlight()
                            self.texts[3].change_text("--------------")
                            return
                        elif t.action == "Segment Mode":
                            self.star_mode = False
                            self.segment_mode1 = True
                            self.segment_mode2 = False
                            self.texts[0].unhighlight()
                            self.texts[1].highlight()
                            self.texts[3].change_text("Click a first star")
                            return
                        elif t.action == "Swap Images":
                            if self.use_solution:
                                t.change_text("Game Image")
                                self.use_solution = False
                            else:
                                t.change_text("Solution")
                                self.use_solution = True
                            return
                        elif t.action == "Quit":
                            self.done = True
                            self.quit = True
                        elif t.action == "Save":
                            output_dict = {}
                            output_dict["stars"]=[]
                            output_dict["segments"]=[]
                            output_dict["starmap"]=self.const_names[self.lev_num]+".png"
                            output_dict["solution"]="solution_"+self.const_names[self.lev_num]+".png"
                            for s in self.stars:
                                output_dict["stars"].append([s.x,s.y])
                            for e in self.segments:
                                for i,s in enumerate(self.stars):
                                    if s == e.point1:
                                        p1 = i
                                        break
                                for i,s in enumerate(self.stars):
                                    if s == e.point2:
                                        p2 = i
                                        break
                                output_dict["segments"].append([p1,p2])
                            save_level(self.const_names[self.lev_num],output_dict)
                            return
                        elif t.action == "File Up":
                            self.lev_num = (self.lev_num + 1) % len(self.const_names)
                            self.texts[-1].change_text(self.const_names[self.lev_num])
                            self.startup()
                            return
                        elif t.action == "File Down":
                            self.lev_num = (self.lev_num - 1) % len(self.const_names)
                            self.texts[-1].change_text(self.const_names[self.lev_num])
                            self.startup()
                            return

                if self.star_mode:
                    if self.point_selected:
                        self.drag_mode = True
                        self.point_selected.new_location(*event.pos)
                        return
                    else:
                        self.stars.append(Point(*event.pos))
                        return
                elif self.segment_mode1:
                    if self.point_selected:
                        self.segments.append(Segment(self.point_selected))
                        self.texts[3].change_text("Click a second star")
                        self.segment_mode1 = False
                        self.segment_mode2 = True
                elif self.segment_mode2:
                    if self.point_selected:
                        # check if trying to make point1 == point2
                        if self.point_selected == self.segments[-1].point1:
                            return
                        # check if a duplicate of some other segment
                        for j in range(len(self.segments)-1):
                            p1 = self.segments[j].point1
                            p2 = self.segments[j].point2
                            if self.segments[-1].point1 == p1 and self.point_selected == p2:
                                return
                            if self.segments[-1].point1 == p2 and self.point_selected == p1:
                                return
                        self.segments[-1].add_star(self.point_selected)
                        self.texts[3].change_text("Click a first star")
                        self.segment_mode1 = True
                        self.segment_mode2 = False
                        return

            if event.button == 3:  # delete points / segments
                if self.star_mode:
                    if self.point_selected:
                        for i in range(len(self.segments)-1,-1,-1):
                            if self.point_selected in [self.segments[i].point1,self.segments[i].point2]:
                                self.segments.remove(self.segments[i])
                        self.stars.remove(self.point_selected)

        # check for point selection and highlighting
        pos = pygame.mouse.get_pos()
        for s in self.stars:
            if s.close_point(pos):
                self.point_selected = s
                return

        self.point_selected = None

    def draw(self, screen):
        screen.fill(pygame.Color("gray30"))

        if self.use_solution:
            screen.blit(self.solution_graphic,(0,0))
        else:
            screen.blit(self.graphic,(0,0))

        for t in self.texts:
            t.render_text(screen)

        for s in self.stars:
            s.draw(screen)

        for s in self.segments:
            s.draw(screen)

        if self.point_selected:
            self.point_selected.highlight(screen)
