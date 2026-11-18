def centralizar(janela, largura, altura):
    """Posiciona a janela no centro da tela, com o tamanho informado."""
    janela.update_idletasks()
    x = (janela.winfo_screenwidth() - largura) // 2
    y = (janela.winfo_screenheight() - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
