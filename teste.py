import sys, pygame


# --- config
pygame.init()
clock = pygame.time.Clock()

# tela
largura_tela = 1300
altura_tela = 700
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Undyne the undying boss battle")


# --- Sprite Undyne (kept from original file, with a safe fallback)
class Undyne(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite = []
        # tentar carregar uma sequência de sprites; se falhar, usar um placeholder
        try:
            for i in range(0, 90):
                img = pygame.image.load(f'undyne sprites/sprite_{i}.png').convert_alpha()
                self.sprite.append(img)
        except Exception:
            # fallback: um único quadrado simples
            s = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 150, 200), s.get_rect())
            self.sprite = [s]

        self.sprite_atual = 0
        self.image = self.sprite[self.sprite_atual]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def update(self):
        self.sprite_atual += 1
        if self.sprite_atual >= len(self.sprite):
            self.sprite_atual = 0
        self.image = self.sprite[self.sprite_atual]


sprite_undyne = pygame.sprite.Group()
undyne = Undyne(550, 75)
sprite_undyne.add(undyne)


# --- música (mantido do arquivo antigo)
try:
    pygame.mixer.init()
    pygame.mixer.music.load('musga.ogg')
    pygame.mixer.music.play(-1)
except Exception:
    # se não conseguir tocar música, continuar sem travar
    print('Aviso: não foi possível tocar musga.ogg (falta arquivo ou formato incompatível)')


# --- carregar imagens do coração e dos escudos sem usar `os`
def load_image_or_none(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except Exception:
        return None

coracao = load_image_or_none('imagens/coracao.png', size=(50, 50))
esc_up = load_image_or_none('imagens/escudo0.png', size=(100,100))
esc_left = load_image_or_none('imagens/escudo1.png', size=(100,100))
esc_down = load_image_or_none('imagens/escudo2.png', size=(100,100))
esc_right = load_image_or_none('imagens/escudo3.png', size=(100,100))

# fallbacks simples (formas) quando imagens não existirem
def fazer_escudo_superficie(color):
    s = pygame.Surface((48,48), pygame.SRCALPHA)
    pygame.draw.circle(s, color, (24,24), 20)
    pygame.draw.circle(s, (255,255,255), (24,24), 8)
    return s

if not esc_up:
    esc_up = fazer_escudo_superficie((120,180,255))
if not esc_down:
    esc_down = fazer_escudo_superficie((100,200,150))
if not esc_left:
    esc_left = fazer_escudo_superficie((200,150,100))
if not esc_right:
    esc_right = fazer_escudo_superficie((200,100,180))
if not coracao:
    coracao = None


# --- posições e estado inicial do escudo
HEART_X, HEART_Y = 630, 430
gap = 10
esc_img = esc_up
esc_x = HEART_X + 25 - esc_img.get_width()//2
esc_y = HEART_Y - esc_img.get_height() + 3*gap

# --- setas (projetéis) que se movem em direção ao coração
import math, random

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, img=None):
        super().__init__()
        self.vx = vx
        self.vy = vy
        self.speed = math.hypot(vx, vy)
        # imagem opcional: desenhar uma pequena flecha apontando para a direção
        if img:
            self.image = img
        else:
            # criar superfície triangular simples
            s = pygame.Surface((14,8), pygame.SRCALPHA)
            pygame.draw.polygon(s, (220,220,100), [(0,4),(10,0),(10,3),(14,3),(14,5),(10,5),(10,8)])
            # rotacionar para apontar na direção de (vx,vy)
            angle = -math.degrees(math.atan2(vy, vx))
            self.image = pygame.transform.rotate(s, angle)
        self.rect = self.image.get_rect(center=(x,y))

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # matar se sair da tela
        if (self.rect.right < 0 or self.rect.left > largura_tela or
            self.rect.bottom < 0 or self.rect.top > altura_tela):
            self.kill()


arrows = pygame.sprite.Group()
spawn_timer = 0
SPAWN_DELAY = 900  # ms entre spawns
HEART_LIVES = 5

# fonte para HUD
try:
    font = pygame.font.SysFont(None, 32)
except Exception:
    pygame.font.init()
    font = pygame.font.SysFont(None, 32)


# --- loop principal
jogo = True
while jogo:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo = False
        elif event.type == pygame.KEYDOWN:
            # debug
            # print('KEYDOWN', event.key)
            if event.key in (pygame.K_w, pygame.K_UP):
                esc_img = esc_up
                esc_x = HEART_X + 25 - esc_img.get_width()//2
                esc_y = HEART_Y - esc_img.get_height() + 3*gap
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                esc_img = esc_down
                esc_x = HEART_X + 25 - esc_img.get_width()//2
                esc_y = HEART_Y + 20
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                esc_img = esc_left
                esc_x = HEART_X - esc_img.get_width() + 3*gap
                esc_y = HEART_Y + 25 - esc_img.get_height()//2
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                esc_img = esc_right
                esc_x = HEART_X + 20
                esc_y = HEART_Y + 25 - esc_img.get_height()//2

    # desenhar fundo/mapa
    tela.fill((0, 0, 0))
    pygame.draw.rect(tela, (255, 255, 255), (580, 380, 150, 150))
    pygame.draw.rect(tela, (0, 0, 0), (587, 387, 136, 136))

    # desenhar coração
    if coracao:
        tela.blit(coracao, (HEART_X, HEART_Y))
    else:
        pygame.draw.circle(tela, (200,50,50), (HEART_X+20, HEART_Y+20), 20)

    # desenhar escudo
    tela.blit(esc_img, (int(esc_x), int(esc_y)))

    # spawn de setas periodicamente
    now = pygame.time.get_ticks()
    if now - spawn_timer > SPAWN_DELAY:
        spawn_timer = now
        # spawn em uma borda aleatória
        side = random.choice(['top','bottom','left','right'])
        if side == 'top':
            sx = random.randint(0, largura_tela)
            sy = -10
        elif side == 'bottom':
            sx = random.randint(0, largura_tela)
            sy = altura_tela + 10
        elif side == 'left':
            sx = -10
            sy = random.randint(0, altura_tela)
        else:
            sx = largura_tela + 10
            sy = random.randint(0, altura_tela)

        # direção para o centro do coração
        heart_cx = HEART_X + 25
        heart_cy = HEART_Y + 25
        dx = heart_cx - sx
        dy = heart_cy - sy
        dist = math.hypot(dx, dy) or 1
        speed = random.uniform(3.0, 5.0)
        vx = dx/dist * speed
        vy = dy/dist * speed
        arrow = Arrow(sx, sy, vx, vy)
        arrows.add(arrow)

        # atualizar e desenhar setas
    arrows.update()
    for a in arrows:
        tela.blit(a.image, a.rect)

    # colisões: seta com escudo -> destruir seta
    shield_rect = esc_img.get_rect(topleft=(int(esc_x), int(esc_y)))
    heart_rect = pygame.Rect(HEART_X, HEART_Y, 50, 50)
    for a in list(arrows):
        if a.rect.colliderect(shield_rect):
            a.kill()
            # poderia tocar som aqui
        elif a.rect.colliderect(heart_rect):
            a.kill()
            HEART_LIVES -= 1
            print('Heart hit! Lives remaining:', HEART_LIVES)

    # desenhar HUD de vidas
    lives_surf = font.render(f'Lives: {HEART_LIVES}', True, (255,255,255))
    tela.blit(lives_surf, (20,20))

    # sprites animadas de Undyne
    sprite_undyne.draw(tela)
    sprite_undyne.update()

    pygame.display.flip()
    clock.tick(24)

pygame.quit()
sys.exit(0)
