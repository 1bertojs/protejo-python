"""Anima imagens da pasta 'imagens' usando pygame.

Controles:
  - Espaço: pausar/resumir
  - Seta para a direita: próxima imagem
  - Seta para a esquerda: imagem anterior
  - Seta para cima: aumentar velocidade (diminuir duração)
  - Seta para baixo: diminuir velocidade (aumentar duração)
  - F: alterna modo tela cheia
  - Esc ou fechar janela: sair

Coloque suas imagens em uma pasta chamada 'imagens' no mesmo diretório deste arquivo.
Suporta .png, .jpg, .jpeg, .bmp, .gif, .webp
"""

import os
import sys
import time
import pygame

IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')


def find_image_files(folder):
	if not os.path.isdir(folder):
		return []
	files = [os.path.join(folder, f) for f in sorted(os.listdir(folder))]
	return [f for f in files if os.path.splitext(f)[1].lower() in IMAGE_EXTS]


def load_images(paths):
	images = []
	for p in paths:
		try:
			# load image but do not call convert() / convert_alpha() here because
			# converting requires a video display mode to be set (causes
			# "No video mode has been set" if called too early).
			img = pygame.image.load(p)
			images.append((p, img))
		except Exception as e:
			print(f"Falha ao carregar {p}: {e}")
	return images


def scale_to_fit(img, max_w, max_h):
	w, h = img.get_size()
	if w <= max_w and h <= max_h:
		return img
	scale = min(max_w / w, max_h / h)
	new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
	return pygame.transform.smoothscale(img, new_size)


def main():
	pygame.init()
	folder = os.path.join(os.path.dirname(__file__), 'imagens')
	image_files = find_image_files(folder)

	if not image_files:
		print("Nenhuma imagem encontrada na pasta 'imagens'. Coloque arquivos com extensão png/jpg/jpeg/bmp/gif/webp.")
		# cria uma janela simples para mostrar a mensagem por alguns segundos
		pygame.display.init()
		screen = pygame.display.set_mode((640, 200))
		pygame.display.set_caption('Animação - nenhuma imagem')
		font = pygame.font.SysFont(None, 24)
		screen.fill((30, 30, 30))
		txt = font.render("Nenhuma imagem encontrada em 'imagens'", True, (220, 220, 220))
		screen.blit(txt, (20, 80))
		pygame.display.flip()
		time.sleep(3)
		return

	# carregar imagens
	loaded = load_images(image_files)
	if not loaded:
		print('Nenhuma imagem carregável encontrada.')
		return

	# determinar tamanho da janela: baseado na maior imagem, limitado a 1280x720
	max_w = max(img.get_width() for _, img in loaded)
	max_h = max(img.get_height() for _, img in loaded)
	win_w = min(max_w, 1280)
	win_h = min(max_h, 720)
	# garantir tamanho mínimo razoável
	win_w = max(win_w, 320)
	win_h = max(win_h, 240)

	# abrir em tela cheia (usa resolução atual do monitor)
	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	pygame.display.set_caption('Animação - imagens (tela cheia)')

	# converter imagens para o formato do display (melhora desempenho)
	converted = []
	for path, img in loaded:
		try:
			img = img.convert_alpha()
		except Exception:
			try:
				img = img.convert()
			except Exception:
				pass
		converted.append((path, img))
	loaded = converted

	# Apenas animação: 24 FPS (cada tick avança para a próxima imagem).
	clock = pygame.time.Clock()

	index = 0
	running = True
	FPS = 24

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False

		# Avança frame a cada tick para conseguir 24fps
		index = (index + 1) % len(loaded)

		screen.fill((0, 0, 0))

		# desenhar imagem centralizada e escalada para caber na janela
		path, img = loaded[index]
		sw, sh = screen.get_size()
		disp = scale_to_fit(img, sw, sh)
		dx = (sw - disp.get_width()) // 2
		dy = (sh - disp.get_height()) // 2
		screen.blit(disp, (dx, dy))

		pygame.display.flip()
		clock.tick(FPS)

	pygame.quit()


if __name__ == '__main__':
	main()