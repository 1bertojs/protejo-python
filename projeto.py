import sys, pygame


#config
pygame.init()
time = pygame.time.Clock()

#tela
largura_tela = 1300
altura_tela = 700
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Undyne the undying boss battle")

#sprite
class Undyne(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite = []
        for i in range(0, 90):
            img = pygame.image.load(f'undyne sprites/sprite_{i}.png').convert_alpha()
            self.sprite.append(img)
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


#musga
pygame.mixer.init()
pygame.mixer.music.load('musga.ogg')
pygame.mixer.music.play(-1)

#funcionar
jogo = True
while jogo:

    #mapa
    pygame.draw.rect(tela, (255, 255, 255), (580, 380, 150, 150))
    pygame.draw.rect(tela, (0, 0, 0), (587, 387, 136, 136))
    
    #escudo

    escudoc = pygame.image.load('imagens/escudo cima.png')
    escudocima = pygame.transform.scale(escudoc, (100, 30))
    escudob = pygame.image.load('imagens/escudo baixo.png')
    escudobaixo = pygame.transform.scale(escudob, (100, 30))
    escudod = pygame.image.load('imagens/escudo dir.png')
    escudodireita = pygame.transform.scale(escudod, (30, 100))
    escudoe = pygame.image.load('imagens/escudo esq.png')
    escudoesquerda = pygame.transform.scale(escudoe, (30, 100))
    esc_img = escudocima
    esc_x = 600
    esc_y = 405

    #controles do escudo
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or pygame.K_UP:
                esc_img = escudocima
                esc_x = 600
                esc_y = 385
            elif event.key == pygame.K_s or pygame.K_DOWN:
                esc_img = escudobaixo
                esc_x = 600
                esc_y = 485
            elif event.key == pygame.K_a or pygame.K_LEFT:
                esc_img = escudoesquerda
                esc_x = 550
                esc_y = 435
            elif event.key == pygame.K_d or pygame.K_RIGHT:
                esc_img = escudodireita
                esc_x = 650
                esc_y = 435

    #sprites funfando
    img = pygame.image.load('imagens/coracao.png')
    coracao = pygame.transform.scale(img, (40, 40))
    tela.blit(coracao, (635, 435))
    tela.blit(esc_img, (esc_x, esc_y))
    sprite_undyne.draw(tela)
    sprite_undyne.update()
    pygame.display.flip()
    time.tick(24)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                jogo = False
    pygame.display.update()
