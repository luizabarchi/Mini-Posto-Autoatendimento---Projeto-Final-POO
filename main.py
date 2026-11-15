from src.cli.main_cli import iniciar_cli
from src.gui.menu_principal import TelaMenuPrincipal

if __name__ == "__main__":
    modo = input("Escolha o modo (1 - Terminal | 2 - Interface Gráfica): ").strip()
    if modo == "1":
        iniciar_cli()
    else:
        TelaMenuPrincipal().mainloop()
