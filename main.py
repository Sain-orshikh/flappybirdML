import pygame
from sys import exit
import config
import components
import population

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
population = population.Population(100)

def generate_pipes():
    if config.pipes:
        # Pass the last pipe to constrain new pipe height
        last_pipe = config.pipes[-1]
        config.pipes.append(components.Pipes(config.win_width, last_pipe))
    else:
        # First pipe has no constraints
        config.pipes.append(components.Pipes(config.win_width))

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
def main():

    pipes_spawn_times = 10

    while True:
        quit_game()

        config.window.fill((0, 0, 0))
        
        pipes_text = font.render(f'Pipes Passed: {config.passed}', True, (255, 255, 255))
        config.window.blit(pipes_text, (10, 520))
        
        gen_text = font.render(f'Generation: {population.generation}', True, (255, 255, 255))
        config.window.blit(gen_text, (10, 560))
        
        alive_count = sum(1 for p in population.players if p.alive)
        alive_text = font.render(f'Alive: {alive_count}', True, (255, 255, 255))
        config.window.blit(alive_text, (10, 600))
        
        config.ground.draw(config.window)
        if pipes_spawn_times <= 0:
            generate_pipes()
            pipes_spawn_times = 200
        pipes_spawn_times -= 1

        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.off_screen:
                config.pipes.remove(p)
        if not population.extinct():
            population.update_live_player()
        else:
            config.pipes.clear()
            config.passed = 0
            population.natural_selection()

        clock.tick(480)
        pygame.display.flip()

main()