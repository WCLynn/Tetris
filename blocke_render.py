# block_renderer.py
import pygame

def draw_fill_block(screen, x, y, color):
    fill_rect = pygame.Rect(x, y, 30, 30)
    pygame.draw.rect(screen, color, fill_rect)

def draw_outline_block(screen, x, y, color):
    outline_rect = pygame.Rect(x, y, 30, 30)
    pygame.draw.rect(screen, color, outline_rect, 3)

def create_filled_surface(color):
    surface = pygame.Surface((30, 30))
    surface.fill(color)
    return surface