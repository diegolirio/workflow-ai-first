"""Gera builder.pptx a partir do deck workflow-proposta-novos-projetos-v2.pptx.

Mantém a capa institucional e o modelo de slide (kicker + título + imagem) do deck base,
troca os textos e coloca o diagrama do Builder (diagrams/png/builder-upstream-downstream.png).

Uso (na raiz do repositório):
    uv run -q --with python-pptx --with pillow python diagrams/builder/build_pptx.py
"""
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Inches

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "workflow-proposta-novos-projetos-v2.pptx"
DIAGRAMA = ROOT / "diagrams/png/builder-upstream-downstream.png"
SAIDA = ROOT / "builder.pptx"

CAPA = 0          # slide 1 do deck base: capa institucional
PIPELINE = 2      # slide 3 do deck base: kicker + título + imagem (Upstream/Downstream)


def trocar_runs(paragrafo, *textos):
    """Escreve os textos nos runs existentes (preserva fonte/cor) e esvazia o resto."""
    runs = paragrafo.runs
    for i, run in enumerate(runs):
        run.text = textos[i] if i < len(textos) else ""


def manter_slides(prs, indices):
    lst = prs.slides._sldIdLst
    for i, sld in reversed(list(enumerate(list(lst)))):
        if i not in indices:
            prs.part.drop_rel(sld.rId)
            lst.remove(sld)


def notas(slide, texto):
    slide.notes_slide.notes_text_frame.text = texto


prs = Presentation(BASE)
capa, pipe = prs.slides[CAPA], prs.slides[PIPELINE]

# ---------- Slide 1: capa ----------
sh = {s.name: s for s in capa.shapes}
trocar_runs(sh["Title 1"].text_frame.paragraphs[0], "Builder", "", "App · Web · Backend")
trocar_runs(sh["Subtitle 2"].text_frame.paragraphs[0], "Da ideia à entrega de produtos e features, com IA")
tb3 = sh["TextBox 3"].text_frame.paragraphs
trocar_runs(tb3[0], "Uma estória, três frentes")
trocar_runs(tb3[1], "A mesma especificação vira app, web e backend, construídos em paralelo.")
tb4 = sh["TextBox 4"].text_frame.paragraphs
trocar_runs(tb4[0], "Guardrails")
trocar_runs(tb4[1], "Constituição, skills e agentes garantem a qualidade: testes integrados, regressivos e end-to-end na pipeline.")
for p in tb4[2:]:
    trocar_runs(p)
notas(capa, (
    "Abertura. Builder é o profissional — e o fluxo — que entrega o produto inteiro: app, web e backend.\n"
    "Mensagem: não é mais PO de um lado e dev de outro; é um fluxo só, da ideia à entrega, com IA executando "
    "e humano decidindo em cada gate.\n"
    "Guardrails: é o que impede a qualidade de depender de disciplina individual."
))

# ---------- Slide 2: Upstream e Downstream ----------
for s in pipe.shapes:
    if s.has_text_frame and s.text_frame.text.strip().upper().startswith("WORKFLOW"):
        trocar_runs(s.text_frame.paragraphs[0], "FLUXO COMPLETO")
    elif s.has_text_frame and s.text_frame.text.strip().startswith("Pipeline"):
        trocar_runs(s.text_frame.paragraphs[0], "Upstream define. Builder entrega em três frentes.")

pic = next(s for s in pipe.shapes if s.shape_type == 13)
box_l, box_t, box_w, box_h = pic.left, pic.top, pic.width, pic.height
rid_antigo = pic._element.blipFill.blip.rEmbed
pic._element.getparent().remove(pic._element)
pipe.part.drop_rel(rid_antigo)  # tira o diagrama antigo do pacote

w_px, h_px = Image.open(DIAGRAMA).size
largura = Inches(12.4)
altura = Emu(int(largura * h_px / w_px))
esquerda = Emu(int((prs.slide_width - largura) / 2))
topo = Emu(int(box_t + (min(box_h, prs.slide_height - box_t - Inches(0.25)) - altura) / 2))
pipe.shapes.add_picture(str(DIAGRAMA), esquerda, topo, largura, altura)

notas(pipe, (
    "Leitura da esquerda para a direita.\n"
    "UPSTREAM (cadência de produto): Metis é o agente de PO; Claude apoia negócio e design de telas; "
    "Jira guarda as estórias; Confluence guarda PRD e decisões. Etapas: Exploratório, Refinamento de Negócio, "
    "Design de Telas, Quebra em Estórias.\n"
    "A fila de Estórias prontas (Definition of Ready) é o único ponto de contato: nenhum lado espera o outro.\n"
    "DOWNSTREAM — o foco: o Refinamento Técnico congela o contrato (endpoints, payloads, eventos). "
    "Com o contrato fechado, App, Web e Backend andam em paralelo; a estória leva o tempo da maior frente, "
    "não a soma das três. Depois: integração e merge (backend → BFF → clientes) e Spec-Driven Testing.\n"
    "Guardrails acompanham todo o Downstream. Final: entrega do produto ou da feature."
))

manter_slides(prs, {CAPA, PIPELINE})
prs.save(SAIDA)
print("ok", SAIDA)
