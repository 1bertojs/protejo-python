import sys, pygame, math, random


#config
pygame.init()
relogio = pygame.time.Clock()

#tela
largura_tela = 1300
altura_tela = 700
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Undyne the undying boss battle")


#Sprite Undyne
class Undyne(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite = []
        try:
            for i in range(0, 90):
                img = pygame.image.load(f'undyne sprites/sprite_{i}.png').convert_alpha()
                self.sprite.append(img)
        except Exception:
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


# música
inicio_musica = None
duracao_musica_ms = None
try:
    pygame.mixer.init()
    pygame.mixer.music.load('musga.ogg')
    pygame.mixer.music.play(-1)
    try:
        # Tenta obter a duração do arquivo de música (em ms)
        snd = pygame.mixer.Sound('musga.ogg')
        duracao_musica_ms = int(snd.get_length() * 1000)
    except Exception:
        duracao_musica_ms = None
    inicio_musica = pygame.time.get_ticks()
except Exception:
    inicio_musica = pygame.time.get_ticks()

# carregar imagens
def carregar_imagem(caminho, tamanho=None):
    try:
        imagem = pygame.image.load(caminho).convert_alpha()
        if tamanho:
            imagem = pygame.transform.scale(imagem, tamanho)
        return imagem
    except Exception:
        return None

coracao = carregar_imagem('imagens/coracao.png', tamanho=(50, 50))
escudocima = carregar_imagem('imagens/escudo0.png', tamanho=(100,100))
escudoesquerda = carregar_imagem('imagens/escudo1.png', tamanho=(100,100))
escudobaixo = carregar_imagem('imagens/escudo2.png', tamanho=(100,100))
escudodireita = carregar_imagem('imagens/escudo3.png', tamanho=(100,100))
setacima = carregar_imagem('imagens/setacima.png', tamanho=(50,50))
setabaixo = carregar_imagem('imagens/setabaixo.png', tamanho=(50,50))
setaesquerda = carregar_imagem('imagens/setaesquerda.png', tamanho=(50,50))
setadireita = carregar_imagem('imagens/setadireita.png', tamanho=(50,50))


# posições iniciais
coracao_x, coracao_y = 630, 430
espaco = 10
imagem_escudo = escudocima
escudo_x = coracao_x - 2.5*espaco
escudo_y = coracao_y - imagem_escudo.get_height() + 3*espaco


# sistema de setas
class Seta(pygame.sprite.Sprite):
    def __init__(self, x, y, vel_x, vel_y, imagem=None):
        super().__init__()
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.image = imagem
        self.rect = self.image.get_rect(center=(x,y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)
        if (self.rect.right < 0 or self.rect.left > largura_tela or
            self.rect.bottom < 0 or self.rect.top > altura_tela):
            self.kill()


grupo_setas = pygame.sprite.Group()
temporizador_spawn = 0
ATRASO_SPAWN = 600
vida_coracao = 5
fim_de_jogo = False
tempo_final_ms = 0
pygame.font.init()
fonte = pygame.font.SysFont(None, 32)


#funcionando
jogo = True
while jogo:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo = False
        elif event.type == pygame.KEYDOWN:
            if fim_de_jogo:
                if event.key == pygame.K_r:
                    vida_coracao = 5
                    fim_de_jogo = False
                    tempo_final_ms = 0
                    grupo_setas.empty()
                    temporizador_spawn = pygame.time.get_ticks()
                    try:
                        pygame.mixer.music.play(-1)
                        inicio_musica = pygame.time.get_ticks()
                    except Exception:
                        inicio_musica = pygame.time.get_ticks()
                elif event.key == pygame.K_ESCAPE:
                    jogo = False
                continue

            if event.key in (pygame.K_w, pygame.K_UP):
                imagem_escudo = escudocima
                escudo_x = coracao_x - 2.5*espaco
                escudo_y = coracao_y - imagem_escudo.get_height() + 3*espaco
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                imagem_escudo = escudobaixo
                escudo_x = coracao_x - 2.5*espaco
                escudo_y = coracao_y + 20
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                imagem_escudo = escudoesquerda
                escudo_x = coracao_x - imagem_escudo.get_width() + 3*espaco
                escudo_y = coracao_y + 25 - imagem_escudo.get_height()//2
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                imagem_escudo = escudodireita
                escudo_x = coracao_x + 20
                escudo_y = coracao_y + 30 - imagem_escudo.get_height()//2

    # spawn de setas
    if not fim_de_jogo:
        agora = pygame.time.get_ticks()
        if agora - temporizador_spawn > ATRASO_SPAWN:
            temporizador_spawn = agora
            lado = random.choice(['cima','baixo','esquerda','direita'])
            if lado == 'cima':
                sx = largura_tela//2
                sy = 0
                imagem = setacima
            elif lado == 'baixo':
                sx = largura_tela//2  
                sy = altura_tela
                imagem = setabaixo
            elif lado == 'esquerda':
                sx = 0
                sy = 450
                imagem = setaesquerda
            else:
                sx = largura_tela
                sy = 450
                imagem = setadireita

            # direção
            centro_coracao_x = coracao_x + 25
            centro_coracao_y = coracao_y + 25
            delta_x = centro_coracao_x - sx
            delta_y = centro_coracao_y - sy
            distancia = math.hypot(delta_x, delta_y) or 1
            velocidade = 10
            vel_x = delta_x/distancia * velocidade
            vel_y = delta_y/distancia * velocidade
            seta = Seta(sx, sy, vel_x, vel_y, imagem=imagem)
            grupo_setas.add(seta)

    # desenhar fundo/mapa
    tela.fill((0, 0, 0))
    pygame.draw.rect(tela, (255, 255, 255), (580, 380, 150, 150))
    pygame.draw.rect(tela, (0, 0, 0), (587, 387, 136, 136))

    # desenhar coração
    if coracao:
        tela.blit(coracao, (coracao_x, coracao_y))
    else:
        pygame.draw.circle(tela, (200,50,50), (coracao_x+20, coracao_y+20), 20)

    # desenhar escudo
    tela.blit(imagem_escudo, (int(escudo_x), int(escudo_y)))

    # sprites animados de Undyne
    sprite_undyne.draw(tela)
    sprite_undyne.update()

    #desenhar setas
    if not fim_de_jogo:
        grupo_setas.update()
    for a in grupo_setas:
        tela.blit(a.image, a.rect)

    # colisões
    escudo_rect = imagem_escudo.get_rect(topleft=(int(escudo_x), int(escudo_y)), size=(100, 30))
    rect_coracao = pygame.Rect(coracao_x, coracao_y, 50, 50)
    for a in list(grupo_setas):
        if a.rect.colliderect(escudo_rect):
            a.kill()
            continue

        if a.rect.colliderect(rect_coracao):
            a.kill()
            vida_coracao -= 1
            if vida_coracao <= 0:
                # trigger game over state
                fim_de_jogo = True
                # record survival time
                if inicio_musica:
                    tempo_final_ms = pygame.time.get_ticks() - inicio_musica
                else:
                    tempo_final_ms = pygame.time.get_ticks()
    # mostrar timer e HUD ou tela de Game Over
    if not fim_de_jogo:
        agora_ms = pygame.time.get_ticks()
        if inicio_musica:
            decorrido_ms = agora_ms - inicio_musica
        else:
            decorrido_ms = 0

        if duracao_musica_ms:
            restante_ms = max(0, duracao_musica_ms - decorrido_ms)
            minutos = restante_ms // 60000
            segundos = (restante_ms // 1000) % 60
            texto_timer = fonte.render(f'sobreviva por:  {minutos:02d}:{segundos:02d}', True, (255,255,255))
        else:
            segundos_totais = decorrido_ms // 1000
            minutos = segundos_totais // 60
            segundos = segundos_totais % 60
            texto_timer = fonte.render(f'sobreviva por:  {minutos:02d}:{segundos:02d}', True, (255,255,255))

        x_timer = largura_tela//2 - texto_timer.get_width()//2
        tela.blit(texto_timer, (x_timer, 10))

        texto_vidas = fonte.render(f'Vidas: {vida_coracao}', True, (255,255,255))
        tela.blit(texto_vidas, (20,20))
    else:
        final_secs = tempo_final_ms // 1000
        fmin = final_secs // 60
        fsec = final_secs % 60
        texto_jogo = fonte.render('FIM DE JOGO', True, (255,50,50))
        texto_tempo = fonte.render(f'Você sobreviveu por {fmin:02d}:{fsec:02d}', True, (255,255,255))
        texto_prompt = fonte.render('Pressione R para reiniciar ou ESC para sair', True, (200,200,200))
        tela.blit(texto_jogo, (largura_tela//2 - texto_jogo.get_width()//2, altura_tela//2 - 40))
        tela.blit(texto_tempo, (largura_tela//2 - texto_tempo.get_width()//2, altura_tela//2))
        tela.blit(texto_prompt, (largura_tela//2 - texto_prompt.get_width()//2, altura_tela//2 + 40))

    pygame.display.flip()
    relogio.tick(24)

pygame.quit()
sys.exit(0)
