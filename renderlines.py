import pygame

# Simple functions to easily render pre-wrapped text onto a single
# surface with a uniform background.
# Author: George Paci

# Results with various background color alphas:
#  no background given: ultimate blit will just change figure part of text,
#      not ground i.e. it will be interpreted as a transparent background
#  background alpha = 0: "
#  background alpha = 128, entire bounding rectangle will be equally blended
#      with background color, both within and outside text
#  background alpha = 255: entire bounding rectangle will be background color
#
# (At this point, we're not trying to respect foreground color alpha;
# we could by compositing the lines first onto a transparent surface, then
# blitting to the returned surface.)

def renderLines(lines, font, antialias, color, background=None):
    fontHeight = font.get_height()

    surfaces = [font.render(ln, antialias, color) for ln in lines]
    # can't pass background to font.render, because it doesn't respect the alpha

    maxwidth = max([s.get_width() for s in surfaces])
    result = pygame.Surface((maxwidth, len(lines)*fontHeight), pygame.SRCALPHA)
    if background == None:
        result.fill((90,90,90,0))
    else:
        result.fill(background)

    for i in range(len(lines)):
      result.blit(surfaces[i], (0,i*fontHeight))
    return result

def renderTextBlock(text, font, antialias, color, background=None):
    "This is renderTextBlock"
    brokenText = text.replace("\r\n","\n").replace("\r","\n")
    return renderLines(brokenText.split("\n"), font, antialias, color, background)
