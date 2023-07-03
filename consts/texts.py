import pygame


def render_labels(
        text_color: tuple, texts: tuple,
        font: pygame.font.Font
) -> list:
    labels = []
    for label in texts:
        labels.append(font.render(label, False, text_color))
    return labels


def render_buttons(
        text_color: tuple, texts: tuple, font: pygame.font.Font,
        width: float, height: float, space: int, space_step: int
) -> list:
    buttons = []
    for button in texts:
        render = []
        btn = font.render(button, False, text_color)
        btn_rect = btn.get_rect(topleft=(width, height + space))
        space += space_step
        render.append(btn)
        render.append(btn_rect)
        buttons.append(render)
    return buttons
