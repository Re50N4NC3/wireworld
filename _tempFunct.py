import pygame

# displays text

# surf = surface at which it should be drawn
# fnt = font
# x, y = x and y positions
# txt = drawn text
# col = text color


def draw_text(surf, fnt, x, y, txt, col):
    text = fnt.render(txt, 1, col)
    surf.blit(text, (x, y))
    pygame.display.flip()
