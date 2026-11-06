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
from pptx.enum.dml import MSO_LINE
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


CLAUDE = ("D97757", "Claude Code", "orquestra a feature")
APP = ("2C7E80", "App", "PagBank · iOS e Android")
BACKEND = ("2C7E80", "Backend", "APIs · BFF")

slide_pratica(
    "DOWNSTREAM NA PRÁTICA",
    "O mesmo dev, com conhecimento nas três plataformas",
    EM_ACAO,
    [CLAUDE, APP, ("2C7E80", "Web", "Gerenciador\nPortal PagInvest · CORF Web"), BACKEND],
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
    [CLAUDE, APP, ("2C7E80", "Web", "iBanking PagBank\nMeus investimentos"), BACKEND],
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
        ("D97757", "Claude Design", "telas e design system\nem artifacts navegáveis"),
        ("2C7E80", "Web", "Portal PagInvest · Gerenciador\nCORF Web"),
        ("2C7E80", "Times", "Engenharia e Product Owners\nno mesmo artefato"),
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
    ("1", "Unit", "Regras e comportamentos, de forma rápida"),
    ("2", "Mutation", "Robustez dos testes: acha falhas não cobertas"),
    ("3", "Integration", "Módulos, serviços e dependências"),
    ("4", "Runbook", "Web/App + Backend: fluxo completo do usuário"),
]
cw, cg, top, ch = Inches(2.3), Inches(0.22), Inches(3.75), Inches(1.6)
x0 = Inches(0.93)
for i, (icone, nome, desc) in enumerate(TESTES):
    x = x0 + i * (cw + cg)
    forma(rio, MSO_SHAPE.ROUNDED_RECTANGLE, x, top, cw, ch, preenchimento="FFFFFF", linha="C9D1D5").adjustments[0] = 0.08
    forma(rio, MSO_SHAPE.OVAL, x + cw / 2 - Inches(0.3), top - Inches(0.3), Inches(0.6), Inches(0.6), preenchimento="E3F1F1")
    texto(rio, x + cw / 2 - Inches(0.4), top - Inches(0.3), Inches(0.8), Inches(0.6),
          [(icone, 18, True, TEAL)], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
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
    ("Entrega com qualidade e previsibilidade", 13, True, "FFFFFF"),
], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

# Pergunta para a sala.
by, bh = ly + Inches(0.35), Inches(0.75)
barra = forma(rio, MSO_SHAPE.ROUNDED_RECTANGLE, x0, by, prs.slide_width - x0 - Inches(0.45), bh, preenchimento=CLARO)
barra.adjustments[0] = 0.3
texto(rio, x0 + Inches(0.25), by, Inches(4.0), bh, [("Testes integrados (E2E)", 18, True, ESCURO)], ancora=MSO_ANCHOR.MIDDLE)
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


# ---------- Slide 7: Onde estamos ----------
status, _ = novo_slide("ONDE ESTAMOS", "Validando o Builder na campanha de investimentos")
L0 = Inches(0.93)
LW = prs.slide_width - L0 - Inches(0.6)   # faixas ocupam a largura toda
y0 = Inches(1.8)

# Cabeçalho.
texto(status, L0, y0, Inches(1.2), Inches(0.4), [("AGORA", 13, True, TEAL)], ancora=MSO_ANCHOR.MIDDLE)
pil = forma(status, MSO_SHAPE.ROUNDED_RECTANGLE, L0 + Inches(1.05), y0 + Inches(0.05), Inches(1.6), Inches(0.3), preenchimento=TEAL)
pil.adjustments[0] = 0.5
texto(status, L0 + Inches(1.05), y0 + Inches(0.05), Inches(1.6), Inches(0.3),
      [("EM VALIDAÇÃO", 10, True, "FFFFFF")], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
texto(status, L0 + Inches(2.8), y0, Inches(5.5), Inches(0.4),
      [("Campanha de investimentos · Portal PagInvest", 13, False, CINZA)], ancora=MSO_ANCHOR.MIDDLE)

# Camadas e repositórios, com o dono de cada um.
CAMADAS = [
    ("Frontend", [("portal-paginvest-core", "Lirio · frontend"),
                      ("portal-paginvest-prize-campaign", "Lirio · micro-frontend")]),
    ("BFF", [("bff-portal-paginvest", "Lirio")]),
    ("Backend", [("prize-campaign", "Lirio"),
                     ("cdb · fixed-income", "Rubens · cdb-transaction e outros")]),
]
rh, rg = Inches(1.0), Inches(0.2)
lw = Inches(2.0)
y = y0 + Inches(0.6)
for camada, repos in CAMADAS:
    forma(status, MSO_SHAPE.RECTANGLE, L0, y, LW, rh, preenchimento=CLARO)
    rot = forma(status, MSO_SHAPE.RECTANGLE, L0, y, lw, rh, preenchimento=TEAL)
    texto(status, L0, y, lw, rh, [(camada, 15, True, "FFFFFF")], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    area_x = L0 + lw + Inches(0.15)
    area_w = LW - lw - Inches(0.3)
    cw2 = Emu(int((area_w - Inches(0.15)) / 2))
    for j, (repo, dono) in enumerate(repos):
        x = area_x + j * (cw2 + Inches(0.15))
        chip = forma(status, MSO_SHAPE.ROUNDED_RECTANGLE, x, y + Inches(0.15), cw2, rh - Inches(0.3),
                     preenchimento="FFFFFF", linha="C9D1D5")
        chip.adjustments[0] = 0.15
        cor_dono = TEAL if dono.startswith("Lirio") else "B7791F"
        texto(status, x + Inches(0.05), y + Inches(0.15), cw2 - Inches(0.1), rh - Inches(0.3), [
            (repo, 14, True, ESCURO),
            (dono, 12, True, cor_dono),
        ], ancora=MSO_ANCHOR.MIDDLE)
    y += rh + rg

texto(status, L0, y + Inches(0.05), Inches(11.5), Inches(0.45), [
    ("Do backend ao micro-frontend com o mesmo dev: 4 das 5 frentes com o Lirio.", 15, True, ESCURO)
])

notas(status, (
    "Onde estamos: validando o fluxo do Builder na campanha de investimentos (Investment Prize Draw) "
    "do Portal PagInvest.\n"
    "Backend: prize-campaign (Lirio); cdb, fixed-income, cdb-transaction e demais serviços de produto (Rubens).\n"
    "BFF: bff-portal-paginvest (Lirio). Frontend: portal-paginvest-core (Lirio) e o micro-frontend "
    "portal-paginvest-prize-campaign (Lirio).\n"
    "Ponto da fala: o mesmo dev atravessando backend, BFF, frontend e micro-frontend — é o slide 3 acontecendo."
))


# ---------- Slide 8: Linha do tempo dos marcos ----------
# Dados dos commits do piloto (campanha de investimentos). Dia 0 = 24/10; fim do marco é inclusivo.
# Dias não úteis (fim de semana e feriado de 02/11) ficam em cinza e não entram na contagem.
from datetime import date, timedelta
INICIO = date(2026, 10, 24)
DIAS = 19                       # eixo de 24/10 a 11/11
CORTE = date(2026, 11, 6)
FERIADOS = {date(2026, 11, 2)}
CONCLUIDO, ANDAMENTO, AGUARDANDO = TEAL, "E3A038", "9ED5D6"
NAO_UTIL = "E6E9EB"


def dia(d):
    return (d - INICIO).days


def util(d):
    return d.weekday() < 5 and d not in FERIADOS


def dias_uteis(ini, fim):
    return sum(util(ini + timedelta(k)) for k in range((fim - ini).days + 1))


MARCOS = [  # (nome, datas, início, fim inclusivo, cor, em aberto, etapas do chamado)
    ("Upstream: definições de negócio", "25/10 – 06/11 (prev.)", date(2026, 10, 25), date(2026, 11, 6), ANDAMENTO, False, []),
    ("Upstream: design", "30/10", date(2026, 10, 30), date(2026, 10, 30), CONCLUIDO, False, []),
    ("Desenvolvimento api-campanha", "30/10 – 04/11", date(2026, 10, 30), date(2026, 11, 4), CONCLUIDO, False, []),
    ("Desenvolvimento BFF", "05/11", date(2026, 11, 5), date(2026, 11, 5), CONCLUIDO, False, []),
    ("Desenvolvimento Frontend", "04/11 – 05/11", date(2026, 11, 4), date(2026, 11, 5), CONCLUIDO, False, []),
    ("Desenvolvimento api-cdb", "desde 04/11", date(2026, 11, 4), CORTE, ANDAMENTO, True, []),
    ("Banco de dados (infra)", "desde 30/10", date(2026, 10, 30), CORTE, AGUARDANDO, True,
     [date(2026, 10, 30), date(2026, 11, 3), date(2026, 11, 4)]),
    ("Disponibilizado em QA", "06/11 – 09/11 (prev.)", date(2026, 11, 6), date(2026, 11, 9), ANDAMENTO, False, []),
]

tl, _ = novo_slide("LINHA DO TEMPO", "Quatro entregas concluídas em até 3 dias úteis cada")
texto(tl, Inches(0.93), Inches(1.5), Inches(11.5), Inches(0.4),
      [("Piloto da campanha de investimentos · dados dos commits · corte em 06/11 · contagem em dias úteis",
        13, False, CINZA)])

# Legenda.
lx, ly_leg = Inches(0.93), Inches(2.0)
for cor, nome, tipo in [(CONCLUIDO, "Concluído", "barra"), (ANDAMENTO, "Em andamento", "barra"),
                        (AGUARDANDO, "Aguardando entrega", "barra"), (NAO_UTIL, "Dia não útil", "barra"),
                        (None, "Etapa do chamado", "losango"), (None, "Corte (06/11)", "corte")]:
    if tipo == "barra":
        forma(tl, MSO_SHAPE.ROUNDED_RECTANGLE, lx, ly_leg + Inches(0.07), Inches(0.22), Inches(0.16), preenchimento=cor)
    elif tipo == "corte":
        c = tl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, lx, ly_leg + Inches(0.15), lx + Inches(0.22), ly_leg + Inches(0.15))
        c.line.color.rgb = RGBColor.from_string(ESCURO); c.line.width = Pt(1.5); c.line.dash_style = MSO_LINE.DASH
    else:
        forma(tl, MSO_SHAPE.DIAMOND, lx + Inches(0.03), ly_leg + Inches(0.05), Inches(0.18), Inches(0.2),
              preenchimento="FFFFFF", linha=ESCURO, espessura=1.25)
    largura_txt = Inches(0.2 + 0.08 * len(nome))
    texto(tl, lx + Inches(0.27), ly_leg, largura_txt, Inches(0.3), [(nome, 11, False, CINZA)], ancora=MSO_ANCHOR.MIDDLE)
    lx += Inches(0.27) + largura_txt + Inches(0.1)

# Eixo de dias, faixas cinza dos dias não úteis e grade.
cx0, cx1 = Inches(3.75), prs.slide_width - Inches(0.55)
dw = (cx1 - cx0) / DIAS
ay = Inches(2.45)
y_rows, rh8 = Inches(2.8), Inches(0.5)
y_fim = y_rows + rh8 * len(MARCOS)
for k in range(DIAS):
    d = INICIO + timedelta(k)
    x = Emu(int(cx0 + k * dw))
    if not util(d):
        forma(tl, MSO_SHAPE.RECTANGLE, x, ay + Inches(0.3), Emu(int(dw)), y_fim - ay - Inches(0.3), preenchimento=NAO_UTIL)
    texto(tl, x, ay, Emu(int(dw)), Inches(0.3),
          [(d.strftime("%d/%m"), 9, util(d), CINZA if util(d) else "A7B0B6")], PP_ALIGN.CENTER)
for k in range(DIAS + 1):
    x = Emu(int(cx0 + k * dw))
    g = tl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x, ay + Inches(0.3), x, y_fim)
    g.line.color.rgb = RGBColor.from_string("E3E7EA"); g.line.width = Pt(0.75)

# Barras.
for i, (nome, datas, ini, fim, cor, aberto, etapas) in enumerate(MARCOS):
    y = y_rows + i * rh8
    n_uteis = dias_uteis(ini, fim)
    texto(tl, Inches(0.93), y, Inches(2.8), rh8, [
        (nome, 12, True, ESCURO),
        (f"{datas} · {n_uteis} {'dia útil' if n_uteis == 1 else 'dias úteis'}", 10, False, CINZA),
    ], ancora=MSO_ANCHOR.MIDDLE)
    # A barra é quebrada nos dias não úteis: um segmento por bloco de dias úteis seguidos.
    blocos, atual = [], None
    for k in range((fim - ini).days + 1):
        d = ini + timedelta(k)
        if util(d):
            atual = [d, d] if atual is None else [atual[0], d]
        elif atual:
            blocos.append(atual); atual = None
    if atual:
        blocos.append(atual)
    for b_ini, b_fim in blocos:
        x = Emu(int(cx0 + dia(b_ini) * dw + Inches(0.02)))
        w = Emu(int((dia(b_fim) - dia(b_ini) + 1) * dw - Inches(0.04)))
        barra = forma(tl, MSO_SHAPE.ROUNDED_RECTANGLE, x, y + Inches(0.13), w, rh8 - Inches(0.26), preenchimento=cor)
        barra.adjustments[0] = 0.3
        if aberto:  # ainda sem entrega: borda tracejada até o corte
            barra.line.color.rgb = RGBColor.from_string(CINZA); barra.line.width = Pt(1); barra.line.dash_style = MSO_LINE.DASH
    for e in etapas:
        ex_ = Emu(int(cx0 + (dia(e) + 0.5) * dw))
        forma(tl, MSO_SHAPE.DIAMOND, ex_ - Inches(0.09), y + Inches(0.15), Inches(0.18), rh8 - Inches(0.3),
              preenchimento="FFFFFF", linha=ESCURO, espessura=1.25)

# Link para a linha do tempo interativa (artifact).
LINK_TIMELINE = "https://claude.ai/artifact/Vr1wcw5NHvqRs5hAQLnkXp?sk=9-ZTb7HgJNADmTAv3E5GBg"
tf_link = texto(tl, prs.slide_width - Inches(4.6), y_fim + Inches(0.08), Inches(4.05), Inches(0.35),
                [("Ver a linha do tempo interativa  >", 12, True, TEAL)], PP_ALIGN.RIGHT, MSO_ANCHOR.MIDDLE)
run_link = tf_link.paragraphs[0].runs[0]
run_link.hyperlink.address = LINK_TIMELINE
run_link.font.underline = True
run_link.font.color.rgb = RGBColor.from_string(TEAL)

# Corte no fim do dia 06/11.
xc = Emu(int(cx0 + (dia(CORTE) + 1) * dw))
c = tl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, xc, ay + Inches(0.3), xc, y_fim + Inches(0.05))
c.line.color.rgb = RGBColor.from_string(ESCURO); c.line.width = Pt(1.5); c.line.dash_style = MSO_LINE.DASH

notas(tl, (
    "Linha do tempo do piloto, montada a partir dos commits. Corte em 06/11 (hoje).\n"
    "Contamos só dias úteis: fins de semana (24–25/10, 31/10–01/11, 07–08/11) e o feriado de 02/11 "
    "aparecem em cinza e ficam fora da conta.\n"
    "Concluídos: design em 1 dia útil (30/10), api-campanha em 3 (30/10–04/11), frontend em 2 (04–05/11) "
    "e BFF em 1 (05/11) — é o Builder funcionando.\n"
    "Em andamento: definições de negócio, prevista até 06/11, e api-cdb desde 04/11.\n"
    "Banco de dados (infra) segue o fluxo do chamado com o time de banco; os losangos são as etapas "
    "(30/10, 03/11 e 04/11).\n"
    "Próximo marco: disponibilizar em QA, previsto de 06/11 a 09/11 (2 dias úteis)."
))


# ---------- Slide 9: Próximo passo — App e iBanking ----------
PROX_APP = ROOT / "diagrams/png/builder-proximo-app.png"
PROX_IB = ROOT / "diagrams/png/builder-proximo-ibanking.png"
prox, _ = novo_slide("PRÓXIMO PASSO", "App e iBanking: a mesma experiência de investimentos")

top9, alt9 = Inches(2.3), Inches(4.05)
proporcao = lambda f: (lambda w, h: w / h)(*Image.open(f).size)
aw, seta, vao = Inches(2.75), Inches(0.9), Inches(0.35)
total9 = aw + seta + Emu(int(alt9 * (proporcao(PROX_APP) + proporcao(PROX_IB)))) + vao
ax = Emu(int((prs.slide_width - total9) / 2))   # composição centralizada

# Coluna "agora": o que está em validação.
agora = forma(prox, MSO_SHAPE.ROUNDED_RECTANGLE, ax, top9, aw, alt9, preenchimento=CLARO, linha=TEAL, espessura=2)
agora.adjustments[0] = 0.06
texto(prox, ax, Inches(1.85), aw, Inches(0.4), [("AGORA", 13, True, TEAL)], ancora=MSO_ANCHOR.MIDDLE)
texto(prox, ax + Inches(0.15), top9, aw - Inches(0.3), alt9, [
    ("Portal", 22, True, ESCURO),
    ("PagInvest", 22, True, ESCURO),
    ("", 8, False, CINZA),
    ("campanha de", 14, False, CINZA),
    ("investimentos", 14, False, CINZA),
    ("", 8, False, CINZA),
    ("em validação", 13, True, TEAL),
], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

forma(prox, MSO_SHAPE.RIGHT_ARROW, ax + aw + Inches(0.15), top9 + alt9 / 2 - Inches(0.35), Inches(0.55), Inches(0.7),
      preenchimento="E3A038")

# As duas próximas frentes, com a tela de cada uma.
texto(prox, ax + aw + seta, Inches(1.85), Inches(8.0), Inches(0.4), [("PRÓXIMO", 13, True, "B7791F")], ancora=MSO_ANCHOR.MIDDLE)
w_px, h_px = Image.open(PROX_APP).size
app_w = Emu(int(alt9 * w_px / h_px))
app_x = ax + aw + seta
prox.shapes.add_picture(str(PROX_APP), app_x, top9, app_w, alt9)
w_px, h_px = Image.open(PROX_IB).size
ib_x = app_x + app_w + vao
ib_w = Emu(int(alt9 * w_px / h_px))
prox.shapes.add_picture(str(PROX_IB), ib_x, top9, ib_w, alt9)

for x, w, nome, sub in [(app_x, app_w, "App PagBank", "iOS e Android"),
                        (ib_x, ib_w, "iBanking", "Meus investimentos na web")]:
    texto(prox, x, top9 + alt9 + Inches(0.08), w, Inches(0.6), [
        (nome, 15, True, ESCURO), (sub, 11, False, CINZA)], PP_ALIGN.CENTER)

notas(prox, (
    "Próximo passo: depois de validar o fluxo no Portal PagInvest, levar a experiência de investimentos "
    "para o App PagBank (iOS e Android) e para o iBanking.\n"
    "As telas são as do slide 4: Meus investimentos no app e na web.\n"
    "Mensagem: o mesmo fluxo do Builder — mesma especificação, o mesmo dev nas frentes — agora no cliente final."
))

n = len(prs.slides)
manter_slides(prs, {CAPA, PIPELINE, n - 7, n - 6, n - 5, n - 4, n - 3, n - 2, n - 1})
prs.save(SAIDA)
print("ok", SAIDA)
