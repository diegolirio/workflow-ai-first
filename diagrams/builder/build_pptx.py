"""Gera builder.pptx a partir do deck workflow-proposta-novos-projetos-v2.pptx.

Mantém a capa institucional e o modelo de slide (kicker + título + imagem) do deck base,
troca os textos e coloca o diagrama do Builder (diagrams/png/builder-upstream-downstream.png).

Uso (na raiz do repositório):
    uv run -q --with python-pptx --with pillow python diagrams/builder/build_pptx.py
"""
import copy
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "workflow-proposta-novos-projetos-v2.pptx"
DIAGRAMA = ROOT / "diagrams/png/builder-upstream-downstream.png"
EM_ACAO = ROOT / "diagrams/png/builder-downstream-em-acao.png"
IBANKING = ROOT / "diagrams/png/builder-downstream-ibanking.png"
CLAUDE_DESIGN = ROOT / "diagrams/png/builder-claude-design.png"
RIO = ROOT / "diagrams/png/builder-rio-circulo.png"
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

# ---------- Slides 3 e 4: Downstream na prática ----------
# Mesmo layout do slide 2: copia a barra de destaque, o kicker e o título;
# imagem da tela à esquerda e, à direita, quem orquestra e as três frentes.
def novo_slide(kicker, titulo_slide):
    """Slide no layout do slide 2: barra de destaque, kicker e título. Devolve (slide, caixa do título)."""
    novo = prs.slides.add_slide(pipe.slide_layout)
    for s in pipe.shapes:
        if s.shape_type != 13:
            novo.shapes._spTree.append(copy.deepcopy(s._element))
    caixa_titulo = None
    for s in novo.shapes:
        if s.has_text_frame and s.text_frame.text.startswith("FLUXO"):
            trocar_runs(s.text_frame.paragraphs[0], kicker)
        elif s.has_text_frame and s.text_frame.text.startswith("Upstream"):
            trocar_runs(s.text_frame.paragraphs[0], titulo_slide)
            caixa_titulo = s
    return novo, caixa_titulo


def texto(slide, x, y, w, h, linhas, alinhar=PP_ALIGN.LEFT, ancora=MSO_ANCHOR.TOP):
    """Caixa de texto; linhas = [(texto, tamanho, negrito, cor)]."""
    tf = slide.shapes.add_textbox(x, y, w, h).text_frame
    tf.word_wrap = True; tf.vertical_anchor = ancora
    tf.margin_left = tf.margin_right = Inches(0.05)
    for i, (txt, tam, neg, cor) in enumerate(linhas):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = alinhar
        r = p.add_run(); r.text = txt
        r.font.size, r.font.bold, r.font.name = Pt(tam), neg, "Arial"
        r.font.color.rgb = RGBColor.from_string(cor)
    return tf


def forma(slide, tipo, x, y, w, h, preenchimento=None, linha=None, espessura=1.0):
    f = slide.shapes.add_shape(tipo, x, y, w, h)
    if preenchimento:
        f.fill.solid(); f.fill.fore_color.rgb = RGBColor.from_string(preenchimento)
    else:
        f.fill.background()
    if linha:
        f.line.color.rgb = RGBColor.from_string(linha); f.line.width = Pt(espessura)
    else:
        f.line.fill.background()
    f.shadow.inherit = False
    return f


def slide_pratica(kicker, titulo_slide, imagem, cards, texto_notas):
    s3, _ = novo_slide(kicker, titulo_slide)

    w_px, h_px = Image.open(imagem).size
    alt = Inches(5.15)
    larg = Emu(int(alt * w_px / h_px))
    s3.shapes.add_picture(str(imagem), Inches(0.7), Inches(1.75), larg, alt)

    x = Inches(0.7) + larg + Inches(0.3)
    w = prs.slide_width - x - Inches(0.55)
    gap, y = Inches(0.24), Inches(1.75)
    h = Emu(int((alt - gap * (len(cards) - 1)) / len(cards)))  # cards ocupam a altura da imagem
    for cor, titulo, legenda in cards:
        card = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
        card.fill.solid(); card.fill.fore_color.rgb = RGBColor.from_string("F2F5F6")
        card.line.fill.background(); card.shadow.inherit = False
        barra = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.1), h)
        barra.fill.solid(); barra.fill.fore_color.rgb = RGBColor.from_string(cor)
        barra.line.fill.background(); barra.shadow.inherit = False
        tf = s3.shapes.add_textbox(x + Inches(0.25), y, w - Inches(0.3), h).text_frame
        tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        linhas = [(titulo, 20, True, "1A1F24")] + [(l, 13, False, "4D5358") for l in legenda.split("\n")]
        for i, (txt, tam, neg, c) in enumerate(linhas):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            r = p.add_run(); r.text = txt
            r.font.size, r.font.bold, r.font.name = Pt(tam), neg, "Arial"
            r.font.color.rgb = RGBColor.from_string(c)
        y += h + gap
    notas(s3, texto_notas)


CLAUDE = ("D97757", "✳  Claude Code", "orquestra a feature")
APP = ("2C7E80", "📱  App", "PagBank · iOS e Android")
BACKEND = ("2C7E80", "⚙️  Backend", "APIs · BFF")

slide_pratica(
    "DOWNSTREAM NA PRÁTICA",
    "O mesmo dev, com conhecimento nas três plataformas",
    EM_ACAO,
    [CLAUDE, APP, ("2C7E80", "🌐  Web", "Gerenciador\nPortal PagInvest · CORF Web"), BACKEND],
    "Este é o Downstream de verdade, numa tela só.\n"
    "À esquerda, a sessão do Claude Code com o plano da feature: analisar requisitos, definir arquitetura, "
    "implementar APIs, ajustar telas do app e do portal, executar testes E2E.\n"
    "No meio, o App PagBank; à direita, o Portal PagInvest; por trás dos dois, o backend com as APIs.\n"
    "Mensagem: é o mesmo dev, com conhecimento nas três plataformas, tocando a feature de ponta a ponta — "
    "o Claude executa e ele decide. "
    "Não são três times esperando um ao outro.",
)

slide_pratica(
    "DOWNSTREAM NA PRÁTICA · IBANKING",
    "App e iBanking entregues pelo mesmo dev",
    IBANKING,
    [CLAUDE, APP, ("2C7E80", "🌐  Web", "iBanking PagBank\nMeus investimentos"), BACKEND],
    "Mesma ideia do slide anterior, agora no cliente final.\n"
    "À esquerda, o Claude Code com o plano: integração da experiência de Investimentos PagBank no app e no "
    "iBanking — requisitos, arquitetura, APIs, telas mobile e web, testes E2E.\n"
    "No meio, o App PagBank; à direita, o iBanking com Meus investimentos; por trás, o mesmo backend.\n"
    "Mensagem: o cliente vê a mesma experiência no app e na web porque foi o mesmo dev, com a mesma "
    "especificação, que entregou as três frentes.",
)

slide_pratica(
    "CLAUDE DESIGN · ARTIFACTS",
    "Design mais rápido, entregas mais rápidas",
    CLAUDE_DESIGN,
    [
        ("D97757", "✳  Claude Design", "telas e design system\nem artifacts navegáveis"),
        ("2C7E80", "🌐  Web", "Portal PagInvest · Gerenciador\nCORF Web"),
        ("2C7E80", "👥  Times", "Engenharia e Product Owners\nno mesmo artefato"),
    ],
    "Antes da linha de código, o design. Esta é a tela do Claude Design com os artifacts do Portal PagInvest: "
    "design system mínimo, lista de campanhas (web e mobile), criar/editar campanha e detalhe da campanha.\n"
    "O mesmo vale para o Gerenciador e o CORF Web.\n"
    "Quem usa: Engenharia e Product Owners, juntos, olhando o mesmo artefato — clicável, não um print.\n"
    "Mensagem: design mais rápido é entrega mais rápida. A tela chega aprovada no Downstream, "
    "e o dev implementa o que o PO já viu funcionando.",
)


# ---------- Slide 6: Testes E2E (curva de rio) ----------
TEAL, ESCURO, CINZA, CLARO = "2C7E80", "1A1F24", "4D5358", "F2F5F6"
rio, caixa_titulo = novo_slide("TESTES END-TO-END", "Hoje, o E2E é uma curva de rio")
caixa_titulo.width = Inches(8.2)

# Rio em círculo no canto superior direito, com um anel verde-água atrás (passa por cima do logo do layout).
d = Inches(4.3)
cx, cy = prs.slide_width - Inches(3.2), Inches(-0.45)
forma(rio, MSO_SHAPE.OVAL, cx - Inches(0.22), cy, d + Inches(0.22), d + Inches(0.1), preenchimento="9ED5D6")
rio.shapes.add_picture(str(RIO), cx, cy, d, d)

texto(rio, Inches(0.93), Inches(1.55), Inches(8.0), Inches(0.5),
      [("Lentos, custosos e geram problemas no fluxo de desenvolvimento.", 16, False, CINZA)])

forma(rio, MSO_SHAPE.RECTANGLE, Inches(0.93), Inches(2.35), Inches(0.08), Inches(0.72), preenchimento=TEAL)
texto(rio, Inches(1.13), Inches(2.28), Inches(7.6), Inches(1.1), [
    ("Nova estratégia de testes", 20, True, ESCURO),
    ("4 tipos de testes no desenvolvimento: o E2E deixa de ser curva de rio.", 15, False, CINZA),
])

TESTES = [
    ("</>", "Unit", "Regras e comportamentos, de forma rápida"),
    ("🧪", "Mutation", "Robustez dos testes: acha falhas não cobertas"),
    ("🧩", "Integration", "Módulos, serviços e dependências"),
    ("🖥️", "Runbook", "Web/App + Backend: fluxo completo do usuário"),
]
cw, cg, top, ch = Inches(2.3), Inches(0.22), Inches(3.75), Inches(1.6)
x0 = Inches(0.93)
for i, (icone, nome, desc) in enumerate(TESTES):
    x = x0 + i * (cw + cg)
    forma(rio, MSO_SHAPE.ROUNDED_RECTANGLE, x, top, cw, ch, preenchimento="FFFFFF", linha="C9D1D5").adjustments[0] = 0.08
    forma(rio, MSO_SHAPE.OVAL, x + cw / 2 - Inches(0.3), top - Inches(0.3), Inches(0.6), Inches(0.6), preenchimento="E3F1F1")
    texto(rio, x + cw / 2 - Inches(0.4), top - Inches(0.3), Inches(0.8), Inches(0.6),
          [(icone, 16, True, TEAL)], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    texto(rio, x + Inches(0.1), top + Inches(0.4), cw - Inches(0.2), ch - Inches(0.5), [
        (nome, 17, True, ESCURO),
        (desc, 13, False, CINZA),
    ], PP_ALIGN.CENTER)

# Linha do tempo com marcadores sob cada card, terminando em seta.
ly = top + ch + Inches(0.28)
fim = x0 + 4 * cw + 3 * cg + Inches(0.15)
linha = rio.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x0, ly, fim, ly)
linha.line.color.rgb = RGBColor.from_string(TEAL); linha.line.width = Pt(2.5)
ln = linha.line._get_or_add_ln()
ln.append(ln.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"}))
for i in range(4):
    mx = x0 + i * (cw + cg) + cw / 2
    forma(rio, MSO_SHAPE.OVAL, mx - Inches(0.11), ly - Inches(0.11), Inches(0.22), Inches(0.22),
          preenchimento="FFFFFF", linha=TEAL, espessura=2.5)

# Resultado ao fim da linha.
ex = fim + Inches(0.2)
ent = forma(rio, MSO_SHAPE.ROUNDED_RECTANGLE, ex, top + Inches(0.17), prs.slide_width - ex - Inches(0.45), Inches(1.25), preenchimento=TEAL)
ent.adjustments[0] = 0.12
texto(rio, ex + Inches(0.1), top + Inches(0.17), prs.slide_width - ex - Inches(0.65), Inches(1.25), [
    ("✓", 22, True, "FFFFFF"),
    ("Entrega com qualidade e previsibilidade", 13, True, "FFFFFF"),
], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

# Pergunta para a sala.
by, bh = ly + Inches(0.35), Inches(0.75)
barra = forma(rio, MSO_SHAPE.ROUNDED_RECTANGLE, x0, by, prs.slide_width - x0 - Inches(0.45), bh, preenchimento=CLARO)
barra.adjustments[0] = 0.3
texto(rio, x0 + Inches(0.25), by, Inches(4.0), bh, [("⏱  Testes integrados (E2E)", 18, True, ESCURO)], ancora=MSO_ANCHOR.MIDDLE)
texto(rio, x0 + Inches(4.4), by, Inches(5.0), bh, [("Quanto tempo estamos levando hoje?", 16, False, CINZA)], ancora=MSO_ANCHOR.MIDDLE)
px = prs.slide_width - Inches(0.45) - Inches(2.2)
pilula = forma(rio, MSO_SHAPE.ROUNDED_RECTANGLE, px, by + Inches(0.1), Inches(2.0), bh - Inches(0.2), preenchimento="FCEFD6", linha="E3A038", espessura=1.5)
pilula.adjustments[0] = 0.5
texto(rio, px, by + Inches(0.1), Inches(2.0), bh - Inches(0.2), [("~ X horas", 20, True, ESCURO)], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

notas(rio, (
    "Curva de rio: é onde a água bate nas pedras, perde velocidade e faz espuma. Hoje o E2E é isso no nosso fluxo: "
    "lento, caro e é onde os problemas aparecem tarde.\n"
    "Nova estratégia: distribuir a qualidade ao longo do desenvolvimento, com 4 tipos de testes.\n"
    "Unit: regras e comportamento, rápido. Mutation: testa os testes, acha o que não está coberto. "
    "Integration: módulos, serviços e dependências reais. Runbook: o fluxo completo do usuário, web/app + backend.\n"
    "Quando o código chega no E2E, ele já passou por tudo isso: o E2E vira fluxo estável, não curva de rio.\n"
    "Pergunta para a sala: quanto tempo estamos levando hoje nos testes integrados? (deixar a sala responder; "
    "o ~X horas é proposital)."
))

n = len(prs.slides)
manter_slides(prs, {CAPA, PIPELINE, n - 4, n - 3, n - 2, n - 1})
prs.save(SAIDA)
print("ok", SAIDA)
