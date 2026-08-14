Você é um designer de apresentações executivas. Gere um deck de 7 slides em português do Brasil a partir da fonte anexada (workflow.md), sobre um modelo de trabalho AI-First para iniciar novos projetos.

REGRAS GERAIS
- Público misto: liderança executiva e time técnico. Slides 3 e 5 precisam ser compreensíveis por quem não é de tecnologia.
- Densidade baixa: no máximo 6 bullets por slide, no máximo 12 palavras por bullet. Sem parágrafos.
- Não use acrônimos sem expandir na primeira ocorrência.
- Não invente conteúdo fora da fonte. Se algo não estiver na fonte, omita.
- Fale sempre em "Product Engineering", nunca em "Product Owner e desenvolvedor". O papel central é o profissional focado em produtividade e entrega de produto, que conduz agentes de ponta a ponta.
- Trate "Guardrails" como conceito nomeado: constituições, skills e agentes específicos que garantem qualidade e agilidade via testes integrados, testes regressivos na pipeline e testes end-to-end envolvendo aplicativo e backend.

IDENTIDADE VISUAL
- Fundo verde-água claro sólido em todos os slides.
- Título em preto, peso bold, alinhado à esquerda. Subtítulo em verde-petróleo dessaturado.
- Corpo em cinza-escuro. Tipografia sans-serif, sem sombras, sem gradientes, sem ícones decorativos.
- Muito espaço em branco. Diagramas com linhas finas e no máximo duas cores além do texto.

ESTRUTURA — 7 SLIDES

Slide 1 — Capa
Título: "Workflow AI-First" em preto; segunda linha "Proposta para novos projetos" em verde-petróleo.
Subtítulo: "Fluxo de desenvolvimento de ponta a ponta implementado por IA".
Dois blocos de apoio no rodapé:
- "Product Engineering": não falamos de PO e desenvolvedor, mas do profissional com foco em produtividade para entrega de produtos.
- "Guardrails": garantem agilidade e qualidade — constituições, skills e agentes específicos executando testes integrados, regressivos na pipeline e end-to-end envolvendo aplicativo e backend.

Slide 2 — A pipeline inteira
Um único diagrama horizontal, intuitivo, sem texto explicativo ao redor.
Mostre dois blocos girando em cadências diferentes, ligados por uma fila:
- UPSTREAM (cadência de produto): Refinamento de Negócio → Design de Telas → Quebra em Estórias
- FILA DE ESTÓRIAS PRONTAS (o único acoplamento entre os dois lados)
- DOWNSTREAM (cadência de engenharia, várias em paralelo): Refinamento Técnico → Implementação → Spec-Driven Testing
Marque visualmente os 6 gates de aprovação entre as etapas.
Legenda única embaixo: "Upstream e Downstream não esperam um pelo outro."

Slide 3 — Upstream: o que entra e o que sai
Visão executiva, sem jargão técnico. Duas colunas.
ENTRA: uma aposta de negócio, em qualquer nível de maturidade.
SAI: um fluxo contínuo de estórias prontas para construir — não um documento aprovado.
Liste o que é produzido no caminho: regras de negócio, persona, métricas e gatilhos, volumetria esperada e campanha, telas por plataforma, registro de ambiguidades.
Destaque em caixa separada as duas conexões que fecham ciclo:
- Métricas viram instrumentação obrigatória no código.
- Volumetria vira o número que alimenta o teste de carga.

Slide 4 — Upstream: agentes, skills e metodologias
Tabela ou três colunas mapeando etapa → ferramenta → método.
- Ideação da iniciativa: Claude Projects.
- Protótipo e telas: Claude Design, alimentado pelo design system da empresa por superfície (aplicativo nativo, web, portal interno).
- PRD, refinamento e quebra em estórias: Claude Cowork, commitando no repositório de especificação.
Metodologias a destacar:
- Agente de brainstorming remove ambiguidades e lacunas em cada etapa.
- Lacuna bloqueante impede avançar de etapa.
- Definition of Ready validado automaticamente por skill antes de liberar a estória.
- Regra dura: só existe o que está no Git.

Slide 5 — Downstream: o que entra e o que sai
Visão executiva. Duas colunas.
ENTRA: uma estória pronta, com critério de aceite já em formato testável.
SAI: funcionalidade em produção, testada de ponta a ponta, rastreável até a métrica que a justificou.
Mostre que uma estória vira uma unidade de mudança com fases por plataforma — backend, camada intermediária, iOS, Android, portal — e que as fases correm em paralelo porque o contrato técnico é congelado antes.
Destaque: a entrega só fecha quando todas as plataformas fecham.

Slide 6 — Downstream: agentes, skills e metodologias
Organize em quatro grupos.
1. Especificação técnica — OpenSpec: proposta, design, tarefas por fase, delta de especificação, sincronização e arquivamento.
2. Especificação de testes — TestSpec: geração da especificação de testes a partir dos cenários, especificação de QA, execução e relatório consolidado.
3. Execução end-to-end — Claude Code com Simulador iOS e Android para o caminho aplicativo → camada intermediária → backend; Claude Code com Playwright para o caminho portal → camada intermediária → backend; teste de carga parametrizado pela volumetria do Upstream.
4. Guardrails — constituição do projeto, testes guiados por testes antes do código, testes unitários e de container como parte da implementação, testes regressivos na pipeline, gate agregador entre repositórios, registro de dívida técnica.
Nota de rodapé: o Downstream roda sempre com agentes e skills; etapa feita à mão não é repetível nem auditável.

Slide 7 — Conclusão
Abra com a frase em destaque, grande, ocupando o terço superior do slide:
"A IA executa, o humano decide. Nunca terceirize suas decisões. Deu certo foi você. Deu errado também foi você."
Abaixo, três ganhos em uma linha cada:
- Agilidade: duas cadências independentes, sem espera mútua.
- Rastreabilidade: de uma linha de código até a métrica que a justificou.
- Qualidade: guardrails automáticos em vez de disciplina individual.
Encerre com os próximos passos: repositório template de especificação, skill de validação de prontidão da estória, costura entre múltiplos repositórios.

TOM
Direto e sóbrio. Presente do indicativo. Sem palavras de preenchimento como "basicamente", "simplesmente" ou "apenas". Sem superlativos de marketing.
