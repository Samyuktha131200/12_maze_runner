import pygame
import time
from collections import deque
from game.maze import generate_maze, CELL
from game.player import Player

FPS = 60
BG = (240, 235, 220)
WALL_COLOR = (40, 40, 60)
EXIT_COLOR = (80, 200, 80)
PATH_COLOR = (255, 190, 60, 150)  # RGBA highlight for the shortest-path hint
FOG_COLOR = (12, 12, 24, 255)     # hidden cells are fully dark
FOG_RADIUS = 3                    # cells around the player that stay visible
COLS, ROWS = 15, 13

WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + 60

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 22)
        self.big_font = pygame.font.SysFont("monospace", 36, bold=True)
        self.fog = pygame.Surface((WIDTH, ROWS*CELL), pygame.SRCALPHA)
        self.reset()

    def reset(self):
        self.walls = generate_maze(COLS, ROWS)
        self.player = Player(0, 0)
        self.exit_rect = pygame.Rect((COLS-1)*CELL+5, (ROWS-1)*CELL+5, CELL-10, CELL-10)
        self.start_time = time.time()
        self.elapsed = 0
        self.won = False
        self.show_path = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                self.show_path = not self.show_path
        return True

    def find_shortest_path(self):
        """BFS from the player's current cell to the exit cell.
        Returns a list of (row, col) cells, start to goal (empty if no path)."""
        start = (
            min(max(self.player.rect.centery // CELL, 0), ROWS - 1),
            min(max(self.player.rect.centerx // CELL, 0), COLS - 1),
        )
        goal = (ROWS - 1, COLS - 1)

        # walls per cell are [N, S, E, W]; a move is allowed if that wall is down
        moves = [(-1, 0, 0), (1, 0, 1), (0, 1, 2), (0, -1, 3)]  # dr, dc, wall index

        parent = {start: None}
        queue = deque([start])
        while queue:
            cell = queue.popleft()
            if cell == goal:
                break
            r, c = cell
            for dr, dc, wall in moves:
                nr, nc = r + dr, c + dc
                if (0 <= nr < ROWS and 0 <= nc < COLS
                        and not self.walls[r][c][wall]
                        and (nr, nc) not in parent):
                    parent[(nr, nc)] = cell
                    queue.append((nr, nc))

        if goal not in parent:
            return []
        path = []
        cell = goal
        while cell is not None:
            path.append(cell)
            cell = parent[cell]
        path.reverse()
        return path

    def draw_path(self):
        """Highlight each cell on the shortest path (only when the hint is on)."""
        if not self.show_path:
            return
        tile = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
        tile.fill(PATH_COLOR)
        for r, c in self.find_shortest_path():
            self.screen.blit(tile, (c * CELL, r * CELL))

    def player_cell(self):
        """The (row, col) cell the player is currently standing in."""
        return (
            min(max(self.player.rect.centery // CELL, 0), ROWS - 1),
            min(max(self.player.rect.centerx // CELL, 0), COLS - 1),
        )

    def draw_fog(self):
        """Hide every maze cell farther than FOG_RADIUS cells from the player."""
        pr, pc = self.player_cell()
        self.fog.fill(FOG_COLOR)
        for r in range(max(0, pr - FOG_RADIUS), min(ROWS, pr + FOG_RADIUS + 1)):
            for c in range(max(0, pc - FOG_RADIUS), min(COLS, pc + FOG_RADIUS + 1)):
                if (r - pr) ** 2 + (c - pc) ** 2 <= FOG_RADIUS ** 2:
                    self.fog.fill((0, 0, 0, 0), (c*CELL, r*CELL, CELL, CELL))
        self.screen.blit(self.fog, (0, 0))

    def update(self):
        if self.won:
            return
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.walls, ROWS, COLS)
        self.elapsed = time.time() - self.start_time
        if self.player.rect.colliderect(self.exit_rect):
            self.won = True

    def draw_maze(self):
        wall_w = 3
        for r in range(ROWS):
            for c in range(COLS):
                x, y = c*CELL, r*CELL
                w = self.walls[r][c]
                if w[0]: pygame.draw.line(self.screen, WALL_COLOR, (x,y), (x+CELL,y), wall_w)
                if w[1]: pygame.draw.line(self.screen, WALL_COLOR, (x,y+CELL), (x+CELL,y+CELL), wall_w)
                if w[2]: pygame.draw.line(self.screen, WALL_COLOR, (x+CELL,y), (x+CELL,y+CELL), wall_w)
                if w[3]: pygame.draw.line(self.screen, WALL_COLOR, (x,y), (x,y+CELL), wall_w)

    def draw(self):
        self.screen.fill(BG)
        self.draw_path()
        self.draw_maze()
        pygame.draw.rect(self.screen, EXIT_COLOR, self.exit_rect, border_radius=4)
        ex_label = self.font.render("EXIT", True, (20,80,20))
        self.screen.blit(ex_label, (self.exit_rect.x+2, self.exit_rect.y+4))
        self.player.draw(self.screen)
        if not self.won:
            self.draw_fog()

        hud = pygame.Rect(0, ROWS*CELL, WIDTH, 60)
        pygame.draw.rect(self.screen, (30,30,50), hud)
        time_surf = self.font.render(f"Time: {self.elapsed:.1f}s   R = New Maze   H = Hint", True, (200,200,200))
        self.screen.blit(time_surf, (10, ROWS*CELL+18))

        if self.won:
            overlay = pygame.Surface((WIDTH, ROWS*CELL), pygame.SRCALPHA)
            overlay.fill((0,0,0,120))
            self.screen.blit(overlay, (0,0))
            msg = self.big_font.render(f"Solved in {self.elapsed:.1f}s!", True, (80,240,80))
            sub = self.font.render("Press R for a new maze", True, (200,200,200))
            self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, ROWS*CELL//2 - 30))
            self.screen.blit(sub, (WIDTH//2 - sub.get_width()//2, ROWS*CELL//2 + 20))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
