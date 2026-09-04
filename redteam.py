"""
redteam.py

Lee attacks.json, prueba cada prompt adversarial contra el modelo
simulado (fake_llm.py), y genera un reporte de resultados.
"""

import json
from fake_llm import ask_fake_llm, response_contains_forbidden_content


def load_attacks(filepath="attacks.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def run_attack(attack):
    prompt = attack["prompt"]
    response = ask_fake_llm(prompt)
    bypassed = response_contains_forbidden_content(response)

    return {
        "id": attack["id"],
        "technique": attack["technique"],
        "prompt": prompt,
        "response": response,
        "result": "BYPASS" if bypassed else "BLOCKED",
    }


def print_report(results):
    print("=" * 70)
    print("REPORTE DE RED TEAMING - LLM Jailbreak Tester")
    print("=" * 70)

    for r in results:
        print(f"\n[{r['result']}] {r['technique']} ({r['id']})")
        print(f"  Prompt: {r['prompt']}")
        print(f"  Respuesta: {r['response']}")

    total = len(results)
    bypassed = sum(1 for r in results if r["result"] == "BYPASS")
    success_rate = (bypassed / total * 100) if total else 0

    print("\n" + "=" * 70)
    print(f"Total de ataques: {total}")
    print(f"Bypasses exitosos: {bypassed}")
    print(f"Tasa de éxito: {success_rate:.1f}%")
    print("=" * 70)

    return {"total": total, "bypassed": bypassed, "success_rate": success_rate}


def save_markdown_report(results, summary, filepath="report.md"):
    lines = ["# Reporte de Red Teaming\n"]
    lines.append(f"**Total de ataques:** {summary['total']}  ")
    lines.append(f"**Bypasses exitosos:** {summary['bypassed']}  ")
    lines.append(f"**Tasa de éxito:** {summary['success_rate']:.1f}%\n")
    lines.append("| Técnica | Resultado | ID |")
    lines.append("|---|---|---|")

    for r in results:
        lines.append(f"| {r['technique']} | {r['result']} | {r['id']} |")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nReporte guardado en {filepath}")


if __name__ == "__main__":
    attacks = load_attacks()
    results = [run_attack(a) for a in attacks]
    summary = print_report(results)
    save_markdown_report(results, summary)