# Workflow AI-First — Upstream e Downstream

Modelo de trabalho para iniciar novos projetos, do refinamento de negócio até o teste de carga em produção, com execução conduzida por Inteligência Artificial e decisão conduzida por gente.

Este documento é um **contrato de agentes**: cada etapa declara entrada, saída, formato de artefato e gate de saída. É legível por humanos e rigoroso o bastante para virar skill sem reescrita.

---

## 1. O princípio

> **A IA executa, o humano decide.**
>
> **Nunca terceirize suas decisões. Deu certo foi você. Deu errado também foi você.**

"Cem por cento implementado por Inteligência Artificial" não é "cem por cento decidido por Inteligência Artificial", e confundir as duas coisas é o único jeito garantido de este modelo falhar.

A IA escreve o PRD, desenha as telas, quebra as estórias, propõe a arquitetura, escreve o código e escreve os testes. Ela não escolhe qual problema resolver, não decide o que é aceitável, não define o que entra em escopo e não assume o risco. Os seis gates deste fluxo existem para isso: em cada um, uma pessoa lê, entende, discorda se for o caso, e assina embaixo.

Aprovar sem ler é terceirizar a decisão. O fluxo não protege ninguém disso — só torna visível quem assinou.

---

## 2. Visão geral

O sistema é composto por **dois laços que giram em velocidades diferentes**, ligados por uma fila.

**Laço de Iniciativa — Upstream.** Gira na cadência de produto, tipicamente semanas. Uma Iniciativa é uma aposta de negócio, com persona, regras, métricas, gatilhos e telas. Seu produto final não é um documento aprovado: é um **fluxo contínuo de Estórias prontas**, liberadas conforme amadurecem.

**Laço de Estória — Downstream.** Gira na cadência de engenharia, tipicamente dias. Pega uma Estória pronta da fila e a leva até produção com testes. Vários laços giram em paralelo, inclusive de Iniciativas diferentes.

**A fila é o único acoplamento entre os dois.** O Upstream escreve nela, o Downstream lê. Nenhum lado espera o outro terminar — e é isso que impede o modelo de virar cascata com nome novo.

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Helvetica Neue, Helvetica, Arial, sans-serif","fontSize":"18px","lineColor":"#6B6B6B","primaryTextColor":"#2E2E2E"},"flowchart":{"htmlLabels":true,"curve":"basis","nodeSpacing":45,"rankSpacing":95,"padding":30,"useMaxWidth":false}}}%%
flowchart LR
  classDef up fill:#EEF6FA,stroke:#8DC3D6,stroke-width:2px,color:#2E2E2E
  classDef down fill:#F8FBEF,stroke:#B8CF83,stroke-width:2px,color:#2E2E2E
  classDef queue fill:#FFF6CF,stroke:#E7C84E,stroke-width:2px,color:#2E2E2E
  classDef guard fill:#2E2E2E,stroke:#2E2E2E,stroke-width:2px,color:#FFFFFF
  classDef done fill:#FFFFFF,stroke:#5A5A5A,stroke-width:2px,color:#2E2E2E
  classDef gate fill:#F2DDFE,stroke:#F2DDFE,color:#5B4A68,font-size:14px
  classDef spacer fill:transparent,stroke:transparent,color:transparent

  subgraph UP["<div style='text-align:center; width:520px;'>
    <div style='font-size:46px; font-weight:900; letter-spacing:2px;'>UPSTREAM</div>
    <div style='font-size:20px; color:#666; margin-top:6px;'>cadência de produto</div>
  </div>"]
    direction TB
    UPSPACE[" "]

    EX["<div style='width:500px; text-align:left; line-height:1.35; padding:6px 2px;'>
      <div style='font-size:44px; font-weight:800;'>⓿ Exploratório</div><br/>
      <div style='font-size:30px;'>Conversas, dados e hipóteses viram<br/>matéria-prima para a IA.</div>
    </div>"]
    RN["<div style='width:500px; text-align:left; line-height:1.35; padding:6px 2px;'>
      <div style='font-size:44px; font-weight:800;'>❶ Refinamento de Negócio</div><br/>
      <div style='font-size:30px;'>O que resolver, para quem, e qual número<br/>precisa mudar.</div>
    </div>"]
    TL["<div style='width:500px; text-align:left; line-height:1.35; padding:6px 2px;'>
      <div style='font-size:44px; font-weight:800;'>❷ Design de Telas</div><br/>
      <div style='font-size:30px;'>Como o cliente vê e usa, em cada<br/>plataforma.</div>
    </div>"]
    QE["<div style='width:500px; text-align:left; line-height:1.35; padding:6px 2px;'>
      <div style='font-size:44px; font-weight:800;'>❸ Quebra em Estórias</div><br/>
      <div style='font-size:30px;'>Pedaços pequenos, cada um demonstrável<br/>sozinho.</div>
    </div>"]

    UPSPACE --> EX
    EX --> RN
    RN --> PRD["PRD aprovado"]
    PRD --> TL
    TL --> DSG["design aprovado"]
    DSG --> QE
  end

  FILA["<div style='width:360px; text-align:center; line-height:1.35;'>
    <div style='font-size:48px; font-weight:800;'>Estórias prontas</div><br/>
    <div style='font-size:33px;'>Pronto para construir.</div>
  </div>"]

  GR["<div style='width:420px; text-align:center; line-height:1.35;'>
    <div style='font-size:48px; font-weight:900; letter-spacing:1px;'>GUARDRAILS</div><br/>
    <div style='font-size:30px;'>O que impede a qualidade de depender<br/>de disciplina individual.</div>
  </div>"]

  subgraph DOWN["<div style='text-align:center; width:520px;'>
    <div style='font-size:46px; font-weight:900; letter-spacing:2px;'>DOWNSTREAM</div>
    <div style='font-size:20px; color:#666; margin-top:6px;'>cadência de engenharia · N em paralelo</div>
  </div>"]
    direction TB
    DOWNSPACE[" "]

    RT["<div style='width:500px; text-align:left; line-height:1.35; padding:6px 2px;'>
      <div style='font-size:44px; font-weight:800;'>❹ Refinamento Técnico</div><br/>
      <div style='font-size:30px;'>Como construir, com o contrato entre as<br/>stacks fechado antes.</div>
    </div>"]
    IMPL["<div style='width:500px; text-align:left; line-height:1.35; padding:6px 2px;'>
      <div style='font-size:44px; font-weight:800;'>❺ Implementação</div><br/>
      <div style='font-size:30px;'>Código escrito com o teste antes, em cada<br/>stack e em paralelo.</div>
    </div>"]
    TEST["<div style='width:500px; text-align:left; line-height:1.35; padding:6px 2px;'>
      <div style='font-size:44px; font-weight:800;'>❻ Spec-Driven Testing</div><br/>
      <div style='font-size:30px;'>Prova que faz o que foi pedido e que<br/>aguenta o volume previsto.</div>
    </div>"]

    DOWNSPACE --> RT
    RT --> CTR["contrato aprovado"]
    CTR --> IMPL
    IMPL --> CI["integração contínua verde"]
    CI --> TEST
  end

  FIM["<div style='width:420px; text-align:left; line-height:1.35;'>
    <div style='font-size:46px; font-weight:800;'>Fechamento</div><br/>
    <div style='font-size:30px;'>Spec atualizada, histórico guardado e a<br/>métrica cobrada depois.</div>
  </div>"]

  QE --> DOR["Definition of Ready"]
  DOR --> FILA
  FILA --> RT
  GR -.-> IMPL
  TEST --> RAP["relatório aprovado"]
  RAP --> FIM

  class EX,RN,TL,QE up
  class RT,IMPL,TEST down
  class FILA queue
  class GR guard
  class FIM done
  class PRD,DSG,DOR,CTR,CI,RAP gate
  class UPSPACE,DOWNSPACE spacer

  style UP fill:#FBFDFE,stroke:#D5E8EF,stroke-width:2px
  style DOWN fill:#FDFEF9,stroke:#DDE9BE,stroke-width:2px
```

---

## 3. Topologia de repositórios

A especificação **não mora onde o código mora**. O ciclo de vida de uma intenção é o ciclo da Estória de negócio, não o ciclo de build de nenhuma stack.

```
{product}-workspace             ← repositório de especificação · a fonte da verdade
├── initiatives/
│   ├── INI-042/                ← PRD, persona, métricas, volumetria, telas
│   │   └── stories/
│   │       └── PGI-1234/       ← a fila de Estórias
│   └── transcripts/             
│       └── 2026-08-13-passagens-contabeis-previdencia.md
├── knowledge/
│   └── indices.md
├── design-system/              ← tokens e catálogo de componentes, por superfície
├── openspec                    ← change OpenSpec: proposal, design, tasks, specs
    ├── changes/PGI-1234/         ← change OpenSpec: proposal, design, tasks
    └── specs/                    ← capacidades vivas + technical-debt.md
├── architecture
    ├── overview.md               ← Descrição dos sistemas/modulos
    ├── refinement
        └── specs/
            └── PGI-1234/ 
├── clone.sh

##############################
# Dev executa o clone.sh
##############################

{product}-backend                ┐
{product}-bff                    │  BFFs App iBanking
{product}-ibanking               │  BFFs App iBanking
{product}-bff-portal             │  repositórios de código
{product}-ios                    │  cadência e pipeline próprios
{product}-android                │  amarrados por Change-Id
{product}-portal                 ┘
```

**Por que separado.** Repositórios de código já existem, cada um com pipeline, permissão e cadência própria; unificá-los custaria mais do que a agilidade que se busca. Replicar a especificação em cada um garante divergência em semanas. O repositório de especificação dedicado é a única configuração que mantém *uma Estória, uma change* íntegra atravessando stacks distintas.

**O ganho não óbvio:** com repositório próprio, o Upstream inteiro passa a ser versionado e revisável por Pull Request. Produto trabalha com o mesmo mecanismo de revisão que engenharia, em vez de um wiki que ninguém sabe se está atualizado.

### Workspace central

Todo desenvolvedor clona todos os repositórios em uma pasta única:

```
~/workspace/{product}/
├── {product}-specs/
├── {product}-backend/
├── {product}-bff-app/
├── {product}-bff-portal/
├── {product}-ios/
├── {product}-android/
└── {product}-portal/
```

Um passo de bootstrap clona tudo e configura a sessão de Inteligência Artificial para enxergar o repositório de especificação e o repositório alvo lado a lado. Sem isso, o `Change-Id` é convenção no papel. Com isso, o agente lê a Estória e escreve o código na mesma sessão.

---

## 4. Regra de materialização

> **Só existe o que está no git.**

Ferramentas de ideação — Claude Projects, Claude Design — não têm diff, Pull Request nem histórico revisável. São superfícies **descartáveis**.

Nada avança de etapa antes de o resultado ser materializado como arquivo commitado em `{product}-specs`. O protótipo vira tokens, especificações de tela e imagens versionadas. A conversa vira PRD. Conteúdo que ficou apenas na ferramenta não existe, não é aprovado e não desce para o Downstream.

---

## 5. Upstream

Todas as etapas seguem o mesmo formato de contrato: **quem conduz, ferramenta, entrada, saída em arquivos, gate de saída.**

Toda etapa do Upstream mantém um registro de **ambiguidades e gaps** — resolvidos e em aberto. Essa é a função do Upstream: reduzir ambiguidade antes que ela custe caro. Gap em aberto marcado como bloqueante impede a promoção para a etapa seguinte.

### Etapa 0 — Exploratório

**Conduz:** Product Owner
**Ferramenta:** Agente Product Owner, Claude Projects e Claude Cowork, commitando em GitHub
**Entrada:** qualquer coisa — conversa com cliente, dado de operação, reclamação recorrente, benchmark, hipótese solta
**Saída:** `initiatives/INI-042/explorations/`

Esta etapa não produz decisão. Produz **matéria-prima**: transcrições, anotações, prints, números levantados, referências de mercado, perguntas em aberto. Tudo é registrado como arquivo.

A razão é direta: **tudo isso vira contexto para a Inteligência Artificial.** Uma exploração que ficou numa reunião não alimenta nada. A mesma exploração registrada em arquivo alimenta o refinamento de negócio, o design das telas e, mais adiante, a discussão técnica — sem que ninguém precise lembrar do que foi dito.

**Não há gate.** O material exploratório não é aprovado, é acumulado. É a única etapa do fluxo sem porta, e isso é deliberado: exigir aprovação para explorar mata a exploração.

O que existe é uma passagem: quando alguém decide que ali tem uma aposta, a exploração vira insumo da Etapa 1 e o `gaps.md` nasce já povoado pelas perguntas em aberto que a exploração levantou.

### Etapa 1 — Refinamento de Negócio

**Conduz:** Product Owner
**Ferramenta:** Agente Product Owner, Claude Projects para ideação, Claude Cowork para materializar
**Entrada:** uma aposta de negócio, em qualquer nível de maturidade
**Saída:** `initiatives/INI-042/`

| Arquivo | Conteúdo |
|---|---|
| `prd.md` | Problema, regras de negócio, escopo e não-escopo |
| `persona.md` | Quem é, contexto de uso, dores |
| `metrics.md` | Métricas, gatilhos, baseline atual, meta |
| `rollout.md` | Volumetria esperada, se há campanha, pico previsto, sazonalidade |
| `gaps.md` | Ambiguidades e lacunas: resolvidas e em aberto |

**Gate:** Pull Request aprovado pelo Product Owner **e** nenhum gap em aberto marcado como bloqueante.

Dois desses arquivos existem para **fechar ciclo**, não para documentar:

- **`metrics.md` vira instrumentação.** Toda Estória declara quais métricas move; isso gera tarefa de instrumentar no `tasks.md` e o teste end-to-end cobre. Sem esse elo, métrica em PRD é decoração.
- **`rollout.md` vira parâmetro de teste de carga.** "Campanha com duzentos mil clientes no primeiro dia" deixa de ser conversa de corredor e vira o número que alimenta o teste de carga no fim do Downstream. Quem sabe o volume é o Upstream; quem precisa do volume é o Downstream; normalmente os dois nunca se falam.

### Etapa 2 — Design de Telas

**Conduz:** Product Owner e Design
**Ferramenta:** Claude Design
**Entrada:** PRD aprovado
**Saída:** `initiatives/INI-042/screens/{superfície}/`

Uma pasta por design system:

```
screens/app/      ← iOS e Android · design system nativo
screens/web/      ← visão web
screens/portal/   ← ferramenta interna de operação
```

Cada tela é um `{screen-id}.md` com propósito, regras de usabilidade, componentes do design system utilizados e **obrigatoriamente os estados de carregando, vazio e erro**, com a imagem versionada ao lado.

Os três estados são obrigatórios porque são exatamente a ambiguidade que sempre vaza para o Downstream e vira decisão solitária de quem estava com o teclado na mão às três da tarde.

O `design-system/` fica na raiz do repositório, não dentro da Iniciativa. Ele é **entrada** do Claude Design, não saída: sem alimentá-lo, a ferramenta inventa componentes.

**Gate:** Pull Request aprovado por Produto e Design **e** toda tela referencia componentes existentes ou declara explicitamente um componente novo.

Essa última cláusula é deliberada: **um componente novo custa três implementações** — iOS nativo, Android nativo e web. Torná-lo explícito no gate transforma uma decisão hoje tomada por acidente numa decisão consciente, tomada por quem paga a conta.

### Etapa 3 — Quebra em Estórias

**Conduz:** Product Owner, com Tech Lead consultado
**Ferramenta:** Claude Cowork
**Entrada:** PRD e telas aprovados
**Saída:** `initiatives/INI-042/stories/PGI-1234/story.md`
**Gate:** Definition of Ready validado por skill **e** Product Owner aprova

Detalhada na seção seguinte, por ser a peça central do modelo.

---

## 6. A Estória — o contrato de handoff

Todo o resto do sistema depende desta peça estar certa, porque é o único ponto onde Upstream e Downstream se tocam.

### A decisão que faz o sistema funcionar

O critério de aceite da Estória é escrito **no mesmo formato do `#### Scenario` da especificação técnica**. Não é formato parecido — é o mesmo.

O ponto onde processos perdem intenção é a tradução: alguém escreve o critério em linguagem de negócio e outra pessoa o reescreve em linguagem técnica. Toda reescrita perde algo, e o que se perde só aparece em produção. Com o formato unificado, o Refinamento Técnico **transcreve** em vez de traduzir, e a divergência entre o que o negócio pediu e o que o teste verifica deixa de ser possível por construção.

### Formato

```yaml
---
id: PGI-1234
initiative: INI-042
title: Cliente resgata investimento pelo aplicativo
stacks: [backend, bff-app, ios, android]
screens: [app/resgate-valor, app/resgate-confirmacao]
metrics: [taxa-conclusao-resgate]
depends_on: [PGI-1233]
status: ready
---
```

O corpo tem cinco blocos:

1. **Persona e contexto** — referência ao `persona.md` da Iniciativa
2. **Regra de negócio** — o recorte específico desta Estória
3. **Critérios de aceite** — um ou mais blocos WHEN / THEN
4. **Fora de escopo** — o que deliberadamente não entra
5. **Gaps em aberto** — obrigatoriamente vazio para o status ser `ready`

O campo `stacks` decide o que está dentro e o que já está fora de escopo. Ele não é decorativo: as fases do `tasks.md` no Downstream derivam dele automaticamente, na ordem de dependência `backend → BFF → clientes`.

### Definition of Ready verificável

Uma skill roda no Pull Request e valida mecanicamente:

1. `stacks` não vazio, e todo valor mapeia para um repositório conhecido
2. Ao menos um critério de aceite em formato WHEN / THEN
3. Toda tela referenciada existe em `screens/`, quando a Estória tem interface
4. Toda métrica referenciada existe em `metrics.md`
5. Nenhum gap bloqueante em aberto
6. `depends_on` aponta para Estórias existentes, sem ciclo
7. Acima de sete critérios de aceite, sinaliza revisão de fatiamento — aviso, não reprovação

Reprovou, não promove. A Estória volta para o Upstream em vez de virar dúvida no meio da implementação.

O sétimo item é heurística, não regra. Tamanho é julgamento humano; o que a máquina faz bem é lembrar de olhar.

### A regra de fatiamento

> **Uma Estória precisa ser demonstrável sozinha.**

Fatia vertical fina, atravessando as stacks necessárias. Nunca fatia horizontal por camada.

"Criar o endpoint de resgate" não é Estória: não dá para demonstrar, e ninguém sabe se está certo até o aplicativo chegar. "Cliente resgata o valor total de um investimento pelo aplicativo" é Estória: atravessa backend, BFF e cliente, e alguém consegue olhar e dizer se está certo.

Isso não é preferência de estilo. Como uma Estória é uma change com fases por stack, uma fatia horizontal produziria uma change que fecha sem entregar nada verificável, e o gate de fechamento perderia o sentido.

---

## 7. Downstream

### Etapa 4 — Refinamento Técnico e Quebra em Tasks

**Conduz:** Tech Lead
**Ferramenta:** Claude Code com as skills de especificação
**Entrada:** Estória com status `ready`
**Saída:** `changes/PGI-1234/`

| Artefato | Origem |
|---|---|
| `proposal.md` | **Transcreve** os critérios de aceite da Estória — não reescreve |
| `design.md` | O COMO: passos numerados, dependências entre passos, riscos, diagramas |
| `specs/{capability}/spec.md` | Delta `ADDED` / `MODIFIED` / `REMOVED` |
| `tasks.md` | Fases derivadas do campo `stacks`, cada uma declarando seu repositório |
| `tests.md` | Gerado por skill a partir dos cenários |

**Gate:** Pull Request aprovado pelo Tech Lead.

Duas famílias de tarefa entram aqui e normalmente ficam de fora até virarem dívida: **instrumentação** das métricas declaradas na Estória, e **contrato entre stacks**.

#### Contrato congelado, fases em paralelo

Com quatro ou mais stacks em fila, a sequência mataria a agilidade que motivou o modelo. A cláusula que resolve isso:

**O `design.md` congela o contrato — endpoints, payloads, eventos — antes de qualquer implementação começar.** Com o contrato congelado, as fases correm em paralelo, cada desenvolvedor no seu repositório, clientes trabalhando contra o contrato acordado.

A ordem `backend → BFF → clientes` vale para **integração e merge**, não para início do trabalho. Sem essa cláusula, a Estória levaria a soma dos tempos das stacks em vez do maior deles.

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Helvetica Neue, Helvetica, Arial, sans-serif","fontSize":"18px","lineColor":"#5A5A5A","primaryTextColor":"#2E2E2E"},"flowchart":{"htmlLabels":true,"curve":"basis","nodeSpacing":40,"rankSpacing":130,"padding":26,"useMaxWidth":false}}}%%
flowchart LR
    classDef down fill:#F5F8E9,stroke:#A9C46C,stroke-width:3px,color:#2E2E2E
    classDef queue fill:#FDF4C9,stroke:#E3C534,stroke-width:3px,color:#2E2E2E
    classDef done fill:#FFFFFF,stroke:#5A5A5A,stroke-width:3px,color:#2E2E2E

    D("<span style='display:inline-block;width:400px;text-align:center;line-height:1.45'><span style='font-size:34px;font-weight:700'>Contrato congelado</span><br/><br/><span style='font-size:24px'>Endpoints, payloads e eventos definidos no design, antes de escrever código.</span></span>")

    B("<span style='display:inline-block;width:280px;text-align:center'><span style='font-size:30px;font-weight:700'>Backend</span></span>")
    BF("<span style='display:inline-block;width:280px;text-align:center'><span style='font-size:30px;font-weight:700'>BFF</span></span>")
    I("<span style='display:inline-block;width:280px;text-align:center'><span style='font-size:30px;font-weight:700'>iOS</span></span>")
    A("<span style='display:inline-block;width:280px;text-align:center'><span style='font-size:30px;font-weight:700'>Android</span></span>")
    P("<span style='display:inline-block;width:280px;text-align:center'><span style='font-size:30px;font-weight:700'>Portal</span></span>")

    M("<span style='display:inline-block;width:400px;text-align:center;line-height:1.45'><span style='font-size:34px;font-weight:700'>Integração e merge</span><br/><br/><span style='font-size:24px'>Nesta ordem: backend, depois BFF, depois clientes.</span></span>")
    T("<span style='display:inline-block;width:340px;text-align:center'><span style='font-size:32px;font-weight:700'>Spec-Driven Testing</span></span>")

    D --> B
    D --> BF
    D --> I
    D --> A
    D --> P
    B --> M
    BF --> M
    I --> M
    A --> M
    P --> M
    M --> T

    class D queue
    class B,BF,I,A,P down
    class M done
    class T down
    linkStyle default stroke:#5A5A5A,stroke-width:2px
```

### Etapa 5 — Implementação

**Conduz:** desenvolvedor conduzindo agentes
**Ferramenta:** Claude Code, um repositório por vez dentro do workspace central
**Entrada:** change aprovada
**Saída:** código, testes unitários e testes de container em cada repositório tocado

Cada fase vira uma branch com o nome da change no repositório alvo, e cada commit carrega o trailer `Change-Id: PGI-1234`. Rastreabilidade completa sai de um `git log --grep`, sem ferramenta nova.

**Testes unitários e de container são parte da implementação**, não etapa posterior. Desenvolvimento guiado por testes vale: o teste precede o código.

**Gate:** integração contínua verde em todos os repositórios tocados **e** todas as tarefas de todas as fases marcadas.

A change não avança enquanto uma stack estiver aberta. É isso que impede o critério de aceite de negócio de se fragmentar entre repositórios sem dono.

### Etapa 6 — Spec-Driven Testing

**Conduz:** QA conduzindo agentes
**Ferramenta:** Claude Code com as skills de teste
**Entrada:** change implementada e `tests.md`

| Verificação | Como |
|---|---|
| Critérios de aceite | Cada critério da Estória mapeia para ao menos um teste — rastreabilidade um-para-um |
| End-to-end aplicativo | Simulador iOS e Android: `App → BFF → Backend`, cadeia real |
| End-to-end portal | Playwright: `Portal → BFF → Backend`, cadeia real |
| Carga | Parametrizado pelos números do `rollout.md` da Iniciativa |

Sem mocks na cadeia end-to-end. O valor do teste está justamente em atravessar as camadas reais que o BFF introduziu.

O teste de carga é o segundo elo que fecha ciclo: os números não são inventados pelo QA, vêm do que o Upstream declarou de volumetria e campanha.

#### A passagem de bastão

O que torna esta etapa diferente de um ciclo de testes convencional é **o que atravessa** da engenharia para o QA. Não é um documento novo, escrito por alguém que leu o que outra pessoa escreveu: é a **mesma especificação** que guiou a construção.

Em um ciclo convencional, o QA recebe a funcionalidade pronta e reescreve o entendimento dela em casos de teste. Essa reescrita é onde a intenção se perde — e o que se perde só aparece em produção. Aqui, o critério de aceite foi escrito uma vez, no Upstream, e é o mesmo objeto que o código implementou e que o teste verifica.

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Helvetica Neue, Helvetica, Arial, sans-serif","fontSize":"18px","lineColor":"#5A5A5A","primaryTextColor":"#2E2E2E"},"flowchart":{"htmlLabels":true,"curve":"basis","nodeSpacing":45,"rankSpacing":120,"padding":28,"useMaxWidth":false,"subGraphTitleMargin":{"top":18,"bottom":40}}}}%%
flowchart LR
    classDef down fill:#F5F8E9,stroke:#A9C46C,stroke-width:3px,color:#2E2E2E
    classDef queue fill:#FDF4C9,stroke:#E3C534,stroke-width:3px,color:#2E2E2E
    classDef plain fill:#FFFFFF,stroke:#5A5A5A,stroke-width:3px,color:#2E2E2E
    classDef guard fill:#2E2E2E,stroke:#2E2E2E,stroke-width:3px,color:#FFFFFF

    subgraph ENG["<span style='display:inline-block;width:520px;text-align:center;line-height:1.4'><span style='font-size:38px;font-weight:800;letter-spacing:3px'>ENGENHARIA&nbsp;</span><br/><span style='font-size:20px;color:#5A5A5A'>o que já existe quando o código fica pronto</span></span>"]
        direction TB
        SPEC("<span style='display:inline-block;width:470px;text-align:left;line-height:1.45'><span style='font-size:32px;font-weight:700'>Especificação da Estória</span><br/><br/><span style='font-size:24px'>Critérios de aceite escritos uma vez, lá no início.</span></span>")
        COD("<span style='display:inline-block;width:470px;text-align:left;line-height:1.45'><span style='font-size:32px;font-weight:700'>Código entregue</span><br/><br/><span style='font-size:24px'>Já testado por dentro, em cada stack.</span></span>")
    end

    BAST("<span style='display:inline-block;width:440px;text-align:center;line-height:1.45'><span style='font-size:34px;font-weight:700'>Passagem de bastão</span><br/><br/><span style='font-size:24px'>A mesma especificação atravessa. O QA não reescreve o entendimento de ninguém.</span></span>")

    subgraph QAB["<span style='display:inline-block;width:520px;text-align:center;line-height:1.4'><span style='font-size:38px;font-weight:800;letter-spacing:3px'>QA AUTÔNOMO&nbsp;</span><br/><span style='font-size:20px;color:#5A5A5A'>conduzido por agentes</span></span>"]
        direction TB
        GER("<span style='display:inline-block;width:470px;text-align:left;line-height:1.45'><span style='font-size:32px;font-weight:700'>Agente gera os testes</span><br/><br/><span style='font-size:24px'>A partir da especificação, não de interpretação.</span></span>")
        EXEC("<span style='display:inline-block;width:470px;text-align:left;line-height:1.45'><span style='font-size:32px;font-weight:700'>Agente executa e coleta</span><br/><br/><span style='font-size:24px'>Cadeia real, sem simulação. Métricas, registros e dados como evidência.</span></span>")
        GER --> EXEC
    end

    REL("<span style='display:inline-block;width:440px;text-align:center;line-height:1.45'><span style='font-size:34px;font-weight:700'>Evidência publicada</span><br/><br/><span style='font-size:24px'>O que foi prometido, contra o que de fato aconteceu.</span></span>")

    SPEC --> BAST
    COD --> BAST
    BAST --> GER
    EXEC --> REL

    class SPEC,COD down
    class BAST queue
    class GER,EXEC down
    class REL guard

    style ENG fill:#FCFDF8,stroke:#D5E3B4,stroke-width:2px
    style QAB fill:#FCFDF8,stroke:#D5E3B4,stroke-width:2px
    linkStyle default stroke:#5A5A5A,stroke-width:2px
```

#### Quem cobre o quê

A pirâmide separa o que é **parte da implementação** do que é **verificação autônoma depois dela**. É a mesma divisão da passagem de bastão, vista por outro ângulo: a base pertence a quem escreve o código, o topo pertence aos agentes de QA.

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Helvetica Neue, Helvetica, Arial, sans-serif","fontSize":"18px","lineColor":"#5A5A5A","primaryTextColor":"#2E2E2E"},"flowchart":{"htmlLabels":true,"curve":"basis","nodeSpacing":10,"rankSpacing":10,"padding":14,"useMaxWidth":false,"subGraphTitleMargin":{"top":20,"bottom":110}}}}%%
flowchart TB
    classDef sdd fill:#F5F8E9,stroke:#A9C46C,stroke-width:3px,color:#2E2E2E
    classDef sdt fill:#FDF4C9,stroke:#E3C534,stroke-width:3px,color:#2E2E2E
    classDef humano fill:#FFFFFF,stroke:#5A5A5A,stroke-width:3px,color:#2E2E2E

    subgraph PIR["<span style='display:inline-block;width:1000px;text-align:center;line-height:1.4'><span style='font-size:40px;font-weight:800;letter-spacing:3px'>PIRÂMIDE DE TESTES&nbsp;</span><br/><span style='font-size:21px;color:#5A5A5A'>quanto mais alto, menos casos e mais caro cada um</span></span>"]
        direction TB
        P7("<span style='display:inline-block;width:200px;text-align:center;line-height:1.3'><span style='font-size:20px;font-weight:700'>Exploratório<br/>manual</span><br/><span style='font-size:16px;color:#5A5A5A'>humano</span></span>")
        P6("<span style='display:inline-block;width:320px;text-align:center'><span style='font-size:23px;font-weight:700'>Resiliência e caos</span><br/><span style='font-size:17px;color:#5A5A5A'>QA autônomo</span></span>")
        P5("<span style='display:inline-block;width:450px;text-align:center'><span style='font-size:25px;font-weight:700'>Carga</span><br/><span style='font-size:18px;color:#5A5A5A'>QA autônomo</span></span>")
        P4("<span style='display:inline-block;width:580px;text-align:center'><span style='font-size:27px;font-weight:700'>Ponta a ponta pela tela</span><br/><span style='font-size:19px;color:#5A5A5A'>QA autônomo</span></span>")
        P3("<span style='display:inline-block;width:710px;text-align:center'><span style='font-size:29px;font-weight:700'>Ponta a ponta pela interface de programação</span><br/><span style='font-size:20px;color:#5A5A5A'>QA autônomo</span></span>")
        P2("<span style='display:inline-block;width:850px;text-align:center'><span style='font-size:31px;font-weight:700'>Integração e container</span><br/><span style='font-size:21px;color:#5A5A5A'>parte da implementação</span></span>")
        P1("<span style='display:inline-block;width:990px;text-align:center'><span style='font-size:34px;font-weight:700'>Unitários</span><br/><span style='font-size:22px;color:#5A5A5A'>parte da implementação</span></span>")
        P7 ~~~ P6 ~~~ P5 ~~~ P4 ~~~ P3 ~~~ P2 ~~~ P1
    end

    class P1,P2 sdd
    class P3,P4,P5,P6 sdt
    class P7 humano

    style PIR fill:#FDFDFC,stroke:#DDDDD5,stroke-width:2px
```

**Verde é parte da implementação.** Escrito antes do código, pelo mesmo agente que constrói, e nunca tratado como etapa separada. **Amarelo é QA autônomo.** Gerado e executado por agentes a partir da especificação, depois do código pronto — é o que atravessa a passagem de bastão. É a mesma divisão do diagrama anterior, vista por outro ângulo.

Duas leituras que a pirâmide entrega de uma vez. A **base é larga e barata**: muitos casos, rodando a cada commit. O **topo é estreito e caro**: poucos cenários, rodando ao fim da Estória. E o único degrau ainda humano é o exploratório no topo — tudo abaixo dele é automático.

O bloco amarelo é o mesmo recurso visual da fila de Estórias no diagrama da seção 2, e por um motivo: **os dois são pontos de passagem, e nos dois o que atravessa é a especificação.** Uma vez do produto para a engenharia, outra vez da engenharia para o QA. É o mesmo objeto viajando por todo o fluxo.

**Gate:** relatório consolidado aprovado, com todos os critérios de aceite verificados.

### Fechamento

Com o gate de testes aprovado: as especificações de capacidade são sincronizadas, a change vai para `changes/archive/YYYY-MM-DD-PGI-1234/`, a Estória vira `done`, e Jira e Confluence recebem os espelhos.

Quando a última Estória fecha, a Iniciativa vira `delivered`. Depois de rodar em produção, alguém compara a métrica prometida com a métrica real e ela vira `measured`.

---

## 8. Máquinas de estado

### Estória

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Helvetica Neue, Helvetica, Arial, sans-serif","fontSize":"20px","lineColor":"#5A5A5A","primaryTextColor":"#2E2E2E","primaryColor":"#EEF4F6","primaryBorderColor":"#7FB3C0","labelBackgroundColor":"#FFFFFF"},"state":{"useMaxWidth":false,"nodeSpacing":70,"rankSpacing":90}}}%%
stateDiagram-v2
    direction LR
    [*] --> draft
    draft --> ready: Definition of Ready aprovado
    ready --> in_progress: change criada
    ready --> draft: refatiamento necessário
    in_progress --> draft: gap de negócio descoberto
    in_progress --> done: change arquivada
    done --> [*]

    classDef aberto fill:#FDF4C9,stroke:#E3C534,stroke-width:3px,color:#2E2E2E
    classDef andamento fill:#F5F8E9,stroke:#A9C46C,stroke-width:3px,color:#2E2E2E
    classDef fechado fill:#FFFFFF,stroke:#5A5A5A,stroke-width:3px,color:#2E2E2E

    class draft aberto
    class ready,in_progress andamento
    class done fechado
```

### Iniciativa

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Helvetica Neue, Helvetica, Arial, sans-serif","fontSize":"20px","lineColor":"#5A5A5A","primaryTextColor":"#2E2E2E","primaryColor":"#EEF4F6","primaryBorderColor":"#7FB3C0","labelBackgroundColor":"#FFFFFF"},"state":{"useMaxWidth":false,"nodeSpacing":70,"rankSpacing":90}}}%%
stateDiagram-v2
    direction LR
    [*] --> draft
    draft --> active: primeira Estória pronta
    active --> delivered: todas as Estórias entregues
    delivered --> measured: métrica real comparada à meta
    measured --> [*]

    classDef aberto fill:#FDF4C9,stroke:#E3C534,stroke-width:3px,color:#2E2E2E
    classDef andamento fill:#F5F8E9,stroke:#A9C46C,stroke-width:3px,color:#2E2E2E
    classDef fechado fill:#2E2E2E,stroke:#2E2E2E,stroke-width:3px,color:#FFFFFF

    class draft aberto
    class active,delivered andamento
    class measured fechado
```

O estado `measured` fecha o ciclo e evita o vício mais comum deste tipo de processo: definir métrica no começo e nunca mais olhar. **A Iniciativa não termina quando o código sobe — termina quando alguém comparou o gatilho prometido com o número real.**

---

## 9. Rastreabilidade

A cadeia é contínua e navegável nos dois sentidos.

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Helvetica Neue, Helvetica, Arial, sans-serif","fontSize":"18px","lineColor":"#5A5A5A","primaryTextColor":"#2E2E2E"},"flowchart":{"htmlLabels":true,"curve":"basis","nodeSpacing":40,"rankSpacing":80,"padding":26,"useMaxWidth":false}}}%%
flowchart LR
    classDef up fill:#EEF4F6,stroke:#7FB3C0,stroke-width:3px,color:#2E2E2E
    classDef down fill:#F5F8E9,stroke:#A9C46C,stroke-width:3px,color:#2E2E2E
    classDef queue fill:#FDF4C9,stroke:#E3C534,stroke-width:3px,color:#2E2E2E

    L("<span style='display:inline-block;width:260px;text-align:center;line-height:1.4'><span style='font-size:30px;font-weight:700'>Linha de código</span></span>")
    C("<span style='display:inline-block;width:300px;text-align:center;line-height:1.4'><span style='font-size:30px;font-weight:700'>Commit</span><br/><span style='font-size:22px'>Change-Id: PGI-1234</span></span>")
    CH("<span style='display:inline-block;width:280px;text-align:center;line-height:1.4'><span style='font-size:30px;font-weight:700'>Change</span><br/><span style='font-size:22px'>PGI-1234</span></span>")
    E("<span style='display:inline-block;width:280px;text-align:center;line-height:1.4'><span style='font-size:30px;font-weight:700'>Estória</span><br/><span style='font-size:22px'>PGI-1234</span></span>")
    IN("<span style='display:inline-block;width:280px;text-align:center;line-height:1.4'><span style='font-size:30px;font-weight:700'>Iniciativa</span><br/><span style='font-size:22px'>INI-042</span></span>")
    ME("<span style='display:inline-block;width:340px;text-align:center;line-height:1.4'><span style='font-size:30px;font-weight:700'>Métrica</span><br/><span style='font-size:22px'>o que justificou aquilo existir</span></span>")

    L --> C --> CH --> E --> IN --> ME

    class L,C,CH down
    class E,IN up
    class ME queue
    linkStyle default stroke:#5A5A5A,stroke-width:2px
```

Na prática, isso responde à pergunta que quase nenhuma organização consegue responder: pega-se uma linha de código, o `git log` dá o `Change-Id`, o `Change-Id` dá a change, a change dá a Estória, a Estória dá o PRD e a métrica que justificou aquilo existir.

Em setor regulado, com auditoria, isso se paga sozinho.

---

## 10. Papéis, gates e ferramentas

| Etapa | Conduz | Aprova | Ferramenta |
|---|---|---|---|
| 0 · Exploratório | Product Owner | Product Owner | Agente Product Owner, Claude Projects e Cowork, GitHub |
| 1 · Refinamento de Negócio | Product Owner | Product Owner | Agente Product Owner, Claude Projects e Cowork, GitHub |
| 2 · Design de Telas | Product Owner | Design | Agente Product Owner, Claude Design, GitHub |
| 3 · Quebra em Estórias | Product Owner | Skill valida prontidão, Product Owner aprova | Agente Product Owner, Claude Cowork, GitHub, Jira |
| 4 · Refinamento Técnico | Desenvolvedor | Conformidade da especificação | OpenSpec, skills próprias, Claude Code |
| 5 · Implementação | Desenvolvedor | QA, com integração contínua verde | Claude Code com Kotlin, Java, iOS, Android e React |
| 6 · Spec-Driven Testing | QA | Conformidade da especificação e Product Owner | TestSpec, Claude Code, Simulador iOS e Android, Playwright, teste de carga |
| 7 · Fechamento | Desenvolvedor | Product Owner e Tech Lead | GitHub, Jira, Confluence |

Os gates são aprovação de Pull Request, com duas exceções: a integração contínua, que é automática, e a conformidade da especificação, verificada por skill antes de qualquer pessoa olhar.

**O Product Owner conduz todo o Upstream.** O que muda entre as etapas 0 e 3 não é quem trabalha nem com qual ferramenta — é o artefato produzido e quem aprova a saída.

**O Downstream roda sempre com agentes e skills.** Etapa executada à mão é etapa que não é repetível e não é auditável.

Cada envolvido tem um ponto no fluxo onde a decisão é dele e não passa sem ele. É isso que dá corpo ao princípio da seção 1.

---

## 11. Publicação — uma via só

O git é a fonte da verdade. Jira e Confluence recebem espelhos gerados, nunca lidos pelo fluxo para trabalhar.

| Destino | Conteúdo | Público |
|---|---|---|
| **Jira** | Estória, link, status e andamento | Gestão |
| **Confluence** | PRD aprovado, telas e fluxo, relatório de testes | Liderança, risco e compliance, operação, suporte, comercial |

Existe um público que nunca vai abrir o repositório e ainda assim precisa responder "qual era a regra de negócio aprovada quando isso subiu".

Toda página gerada carrega no topo um aviso de página gerada e o link para o commit de origem. **Se alguém editar no destino, a próxima geração sobrescreve.** Isso é intencional e está escrito no contrato.

---

## 12. Quando dá errado

A parte que decide se o processo sobrevive ao contato com a realidade.

| Situação | O que acontece |
|---|---|
| **Gap de negócio descoberto na implementação** | A Estória volta para `draft` e o gap é registrado no `gaps.md`. Ambiguidade de negócio não se resolve dentro da implementação — é ali que ela vira decisão silenciosa de quem estava com o teclado na mão |
| **Contrato precisa mudar depois de congelado** | Atualiza-se o `design.md` por Pull Request e as fases dependentes são notificadas. Nunca se muda o contrato direto no código |
| **Teste end-to-end reprova** | Volta para implementação. Não existe aceitar com ressalva — a ressalva vira o próximo incidente |
| **Dívida técnica identificada** | Registrada em `specs/technical-debt.md`, lida ao explorar e revisitada ao arquivar |
| **Estória grande demais, descoberta tarde** | Refatia-se. A change é arquivada, nunca deletada em silêncio |

---

## 13. O que precisa ser construído

| Item | Estado |
|---|---|
| Este documento | pronto |
| Repositório template `{product}-specs` com estrutura e templates de artefato | a construir |
| Skills do Upstream: negócio, design, quebra em Estórias, validação de prontidão | a construir |
| Skills do Downstream: proposta, aplicação, sincronização, arquivamento | adaptar para multi-repositório |
| Skills de teste: geração, especificação de QA, execução e relatório | adaptar para BFF e Simulador |
| Bootstrap do workspace central | a construir |
| Publicação em Jira e Confluence | parcial |
| Verificação de `Change-Id` e gate agregador multi-repositório na integração contínua | a construir |

O Downstream tem base pronta em modelos de especificação já existentes. O que é genuinamente novo é o **Upstream inteiro** e a **costura multi-repositório**.

## PRDs como conhecimento para POs

```mermaid
flowchart LR
    I[🤖 Agente de<br/>Investimentos]:::agent
    C[🤖 Agente de<br/>CDB]:::agent
    T[🤖 Agente de<br/>Tesouraria Direta]:::agent
    P[🤖 Agente de<br/>Passivos Contábeis]:::agent
    R[🤖 Agente de<br/>Renda Variável]:::agent
    V[🤖 Agente de<br/>Previdência]:::agent
    D[PRDs]:::docs
    I --> C
    I --> T
    I --> P
    I --> R
    I --> V
    P --> D
    classDef agent stroke:#000,stroke-width:0px,font-size:28px;
    classDef docs fill:#fff,stroke:#1638b3,color:#000,stroke-width:3px;
```

---

## 14. Glossário

| Termo | Significado |
|---|---|
| **Iniciativa** | Aposta de negócio com persona, regras, métricas e telas. Unidade do Upstream |
| **Estória** | Fatia vertical demonstrável sozinha. Contrato de handoff entre Upstream e Downstream |
| **Change** | Unidade de mudança técnica: proposta, design, tasks e delta de especificação. Uma por Estória |
| **Fase** | Recorte da change dentro de um repositório de código |
| **Gate** | Ponto onde uma pessoa lê, entende e assina embaixo |
| **Gap** | Ambiguidade ou lacuna registrada. Bloqueante impede promoção de etapa |
| **Change-Id** | Identificador que amarra Estória, change, branch e commits em todos os repositórios |
