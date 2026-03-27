from tkinter import SEL
import pygame as pg
pg.init()
pg.display.set_caption("Card Game")
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

import pygame as pg

class Card:
    def __init__(self, x, y, width, height, name, cost, color=(255,255,255)): # x & y are the top-left corner of the card
        self.rect = pg.Rect(x, y, width, height)
        self.color = color

        self.name = name
        self.cost = cost

        self.hovered = False
        self.selected = False
        self.dragging = False

        self.offset= pg.Vector2(0,0)

        self.font = pg.font.SysFont(None, 24)

    def update(self, dt, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

        self.selected = self.hovered and pg.mouse.get_pressed()[0]

        if self.dragging:
            self.rect.x = mouse_pos[0] + self.offset.x
            self.rect.y = mouse_pos[1] + self.offset.y

        if self.hovered:
            print(f"Hovering over {self.name}")
        else :
            pass

        if self.selected:
            print(f"Selected {self.name}")
        else:
            pass


    def draw(self, screen):
        color = (200, 200, 200) if self.hovered else self.color
        pg.draw.rect(screen, color, self.rect, border_radius=8)

        pg.draw.rect(screen, (0,0,0), self.rect, 2, border_radius=8)

        name_text = self.font.render(self.name, True, (0,0,0))
        cost_text = self.font.render(str(self.cost), True, (0,0,0))

        screen.blit(name_text, (self.rect.x + 10, self.rect.y + 10))
        screen.blit(cost_text, (self.rect.right - 20, self.rect.y + 10))

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
        self.reposition()

    def reposition(self):
        start_x = 300
        y = 500
        spacing = 120

        for i, card in enumerate(self.cards):
            card.rect.topleft = (start_x + i * spacing, y)


    def draw(self, screen):
        for card in self.cards:
            card.draw(screen)

hand = Hand()

hand.add_card(Card(0, 0, 100, 150, "Strike", 1))
hand.add_card(Card(0, 0, 100, 150, "Defend", 1))
hand.add_card(Card(0, 0, 100, 150, "Fireball", 2))


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                for card in hand.cards:
                    if card.rect.collidepoint(event.pos):
                        card.dragging = True

                        mouse_x, mouse_y = event.pos

                        card.offset.x = card.rect.x - mouse_x
                        card.offset.y = card.rect.y - mouse_y
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                for card in hand.cards:
                    card.dragging = False

    mouse_pos = pg.mouse.get_pos()
    dt = clock.tick(60) / 1000

    for card in hand.cards:
        card.update(dt, mouse_pos)

    screen.fill((0, 128, 0))
    hand.draw(screen)

    pg.display.flip()