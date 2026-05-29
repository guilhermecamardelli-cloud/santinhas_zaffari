import json
import os
import statistics

arquivo_historico = "historico_calculadora.json"


def ler_numero(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Erro: digite apenas números!")


def carregar_historico():
    if os.path.exists(arquivo_historico):
        try:
            with open(arquivo_historico, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except (json.JSONDecodeError, IOError):
            print("[!] Erro ao ler o arquivo de histórico. Iniciando novo.")
            return []
    return []


def salvar_historico(historico):
    try:
        with open(arquivo_historico, "w", encoding="utf-8") as arquivo:
            json.dump(historico, arquivo, indent=4, ensure_ascii=False)
    except IOError:
        print("[!] Erro ao salvar o histórico no disco.")


def gerar_relatorio(historico_geral):
    if not historico_geral:
        print("\n[!] Nenhum cálculo ainda realizado.")
        return
    relatorio = [item["rel"] for item in historico_geral]
    media = statistics.mean(relatorio)
    print("\n" + "=" * 30)
    print("      RELATÓRIO ACUMULADO")
    print("=" * 30)
    print(f"Total de Operações: {len(relatorio)}")
    print(f"Soma de todos:     {sum(relatorio)}")
    print(f"Valor Máximo:      {max(relatorio)}")
    print(f"Valor Mínimo:      {min(relatorio)}")
    print(f"Média dos valores: {media}")
    print("=" * 30 + "\n")


# Carrega os dados ao iniciar
historico_geral = carregar_historico()

if historico_geral:
    print(
        f"[i] Histórico recuperado com sucesso! ({len(historico_geral)} operações encontradas)\n"
    )

while True:
    # Adicionada a opção (z)erar no menu visual
    print(
        "Menu: (c)alcular | (h)istórico | (r)elatório | (z)erar histórico | (s)air"
    )
    opcao = input("Escolha uma opção: ").lower().strip()

    if opcao == "h":
        print("\n--- HISTÓRICO COMPLETO ---")
        if not historico_geral:
            print("Nenhum registro encontrado.")
        for item in historico_geral:
            print(
                f"{item['num1']} {item['op']} {item['num2']} = {item['rel']}"
            )
        print("--------------------------\n")
        input("Pressione Enter para voltar ao menu...")

    elif opcao == "r":
        gerar_relatorio(historico_geral)
        input("Pressione Enter para voltar ao menu...")

    # --- NOVA OPÇÃO PARA ZERAR O HISTÓRICO ---
    elif opcao == "z":
        confirmacao = (
            input(
                "Tem certeza que deseja apagar TODO o histórico? (s/n): "
            )
            .lower()
            .strip()
        )
        if confirmacao == "s":
            historico_geral = []  # Limpa a memória do programa
            salvar_historico(
                historico_geral
            )  # Sobrescreve o arquivo JSON com a lista vazia
            print(
                "\n[✓] Histórico totalmente zerado com sucesso!\n"
            )
        else:
            print("\nAção cancelada. O histórico foi mantido.\n")
        input("Pressione Enter para voltar ao menu...")

    elif opcao == "s":
        salvar_historico(historico_geral)
        print("Saindo e salvando dados... Até logo!")
        break

    elif opcao == "c" or opcao == "":
        print("\n--- NOVO CÁLCULO ---")
        num1 = ler_numero("Digite o primeiro número: ")
        operacao = input("Escolha operação (+, -, *, /): ").strip()
        num2 = ler_numero("Digite o segundo número: ")

        resultado = None

        if operacao == "+":
            resultado = num1 + num2
        elif operacao == "-":
            resultado = num1 - num2
        elif operacao == "*":
            resultado = num1 * num2
        elif operacao == "/":
            if num2 == 0:
                print("Erro: divisão por zero")
            else:
                resultado = num1 / num2
        else:
            print("Operação inválida")

        if resultado is not None:
            print(f"Resultado: {resultado}\n")

            historico_geral.append(
                {"num1": num1, "op": operacao, "num2": num2, "rel": resultado}
            )
            salvar_historico(historico_geral)
    else:
        print("[!] Opção inválida. Tente novamente.\n")