# TradeCare-Agent: 중한 B2B 무역 고객 지원을 위한 Reflection 기반 Multi-Agent RAG 시스템

## 초록

중한 B2B 무역 고객 지원에서는 정확한 문의 접수, 도메인 지식에 근거한 안내, 그리고 신중한 리스크 처리가 필요하다. 고객은 OEM 생산, 구매대행, 중국 시장조사, 불량 클레임, 물류, 통관, 라벨링, 인증과 관련하여 불완전한 질문을 하는 경우가 많다. 단일 대규모 언어모델(LLM)의 응답은 필요한 정보를 빠뜨리거나, 공급처 확인, 통관, 보상 가능성에 대해 과도하게 확정적인 답변을 생성할 수 있다. 본 연구는 검색 증강 생성(RAG)과 Reflection을 결합한 Multi-Agent 고객 지원 아키텍처인 TradeCare-Agent를 제안한다. 본 시스템은 문의 분류, 지식 검색, 무역 전문 답변 생성, 리스크 검토, Critic 기반 자기수정 단계를 분리한다. 또한 본 시스템을 실행 가능한 FastAPI 웹앱으로 구현하고, 중한 B2B 무역 지원을 위해 구축한 30개 케이스 벤치마크로 평가한다. 실험에서는 단일 호출 baseline과 RAG-only baseline을 비교하며, 정성 평가와 데모 준비를 위해 실제 고객 문의에 가까운 20개 사례도 함께 구성하였다.

## 1. 서론

B2B 무역대행 고객은 실무적으로 바로 활용할 수 있는 답변을 필요로 하지만, 초기 문의는 정보가 부족한 경우가 많다. 예를 들어 OEM 문의에서는 수량, 도면, 로고 파일, 납기 일정이 누락될 수 있다. 불량 클레임 문의에서는 증빙 자료, 불량률, 검수 이력, 거래 기록이 빠질 수 있다. 통관 문의에서는 제품 카테고리, 소재, HS Code, 인증 관련 정보가 필요할 수 있다.

본 프로젝트는 중한 무역대행 고객센터를 대상으로 한다. 목표는 사람 무역 담당자를 대체하는 것이 아니라, 필요한 정보를 수집하고, 근거 있는 절차 안내를 제공하며, 안전하지 않거나 환각에 기반한 응답을 줄이는 것이다.

## 2. 관련 연구

검색 증강 생성(Retrieval-Augmented Generation, RAG)은 외부 지식을 검색하여 생성 과정에 반영함으로써 사실 기반성을 높인다. ReAct 계열 Agent는 추론과 도구 사용을 결합하여 다단계 문제를 해결한다. Reflexion 및 Critic 기반 접근법은 자기 평가 루프를 도입하여 Agent가 약한 출력을 식별하고 수정할 수 있도록 한다. TradeCare-Agent는 이러한 아이디어를 좁은 범위의 B2B 무역 고객 지원 환경에 적용한다.

## 3. 과제 정의

입력은 한국어 고객 문의이다.

출력은 근거 기반 고객센터 응답이다. 이 응답은 문의 의도 분류, 누락된 필수 정보 요청, 다음 단계 안내, 검색된 서비스 지식 활용, 그리고 단가, 납기, 통관 가능성, 인증, 환불, 교환 등에 대한 과도한 확정 표현 방지를 포함해야 한다.

대상 의도는 OEM/ODM, 구매대행, 시장조사, 불량 클레임, 물류/통관, 일반 또는 범위 외 문의이다.

## 4. 방법론

TradeCare-Agent는 Intake Agent, Retrieval Agent, Trade Specialist Agent, Risk Agent, Critic Agent의 다섯 Agent로 구성된다.

Intake Agent는 고객 문의의 의도를 분류하고 누락된 필수 정보를 식별한다. Retrieval Agent는 재현 가능한 TF-IDF 검색기를 사용하여 로컬 Markdown 지식 문서를 검색한다. Trade Specialist Agent는 접수 결과와 검색된 문맥을 활용하여 고객에게 전달할 답변 초안을 작성한다. Risk Agent는 무조건적인 가능 여부, 환불 보장, 통관 보장 등 안전하지 않은 표현을 수정한다. Critic Agent는 답변 품질을 평가하고 가벼운 Reflection 단계를 수행한다.

다섯 Agent를 사용하는 이유는 중한 무역 지원 업무에 서로 다른 실패 지점이 존재하기 때문이다. Intake 실패는 제품 사진, 수량, 사양, 검수 기록, 배송 정보 누락으로 이어질 수 있다. Retrieval 실패는 회사의 문서화된 서비스 범위를 반영하지 못한 근거 없는 답변으로 이어질 수 있다. Drafting 실패는 고객이 실제로 행동하기 어려운 답변을 만들 수 있다. Risk 실패는 공급 가능 여부, 가격, 납기, 통관, 인증, 환불, 보상에 대해 과도하게 확정하는 문제를 만들 수 있다. Reflection 실패는 이러한 문제를 최종 단계에서 확인하지 못하게 한다. 역할을 분리하면 각 실패 지점을 명확히 드러낼 수 있고, 단일 호출 응답과 구조화된 Multi-Agent workflow를 비교할 수 있다.

### RAG 지식 베이스 출처

RAG 지식 베이스는 `data/knowledge_base/*.md`에 로컬 Markdown 파일로 저장된다. 여기에는 회사 소개, OEM/ODM 서비스 안내, 구매대행 안내, 이우시장 및 중국 시장조사 안내, 불량 클레임 절차, 물류/통관 안내, 견적 필수 정보, FAQ가 포함된다. 이 문서들은 프로젝트 개발 과정에서 윤항무역의 서비스 범위, 홈페이지에 공개 가능한 서비스 정보, 운영자가 제공한 고객 상담 규칙을 바탕으로 수동 정리하였다.

이 출처 설계는 아키텍처의 정당성을 설명하는 데 중요하다. 단일 LLM 응답은 일반적인 사전지식에 의존하여 회사별 제약을 놓칠 수 있다. 반면 Retrieval Agent는 필수 OEM 정보, 공급처 확인 필요성, 불량 증빙 요구사항, 통관/인증 불확실성 등 문서화된 서비스 규칙에 답변을 근거시킨다. 이후 Risk Agent와 Critic Agent는 생성된 답변이 검색된 제약을 따르는지 다시 점검한다.

## 5. 시스템 구현

TradeCare-Agent는 아키텍처가 개념적 설계에 그치지 않고 실제로 실행 가능함을 보이기 위해 로컬 웹 애플리케이션으로 구현하였다. 백엔드는 Python FastAPI와 Uvicorn ASGI 서버를 사용한다. 루트 엔드포인트 `/`는 고객센터 사용자 인터페이스를 제공하고, `/api/chat`은 Multi-Agent workflow를 실행한다. `/health` 엔드포인트는 배포 및 상태 점검을 위해 제공된다.

프론트엔드는 정적 HTML, CSS, JavaScript로 구현하였다. 인터페이스는 고객 채팅, 생성된 AI 응답, 탐지된 의도, Critic 점수, 필수 및 누락 정보, 선택적 RAG/Reflection trace를 보여준다. 이러한 레이아웃은 발표자나 운영자가 최종 답변만 보는 것이 아니라, Agent가 특정 답변을 생성한 이유를 함께 확인할 수 있게 한다.

앱은 재현 가능한 데모를 위해 외부 API 키 없이도 deterministic fallback logic으로 실행될 수 있다. `OPENAI_API_KEY`가 제공되는 경우 OpenAI-compatible model 설정을 선택적으로 사용할 수 있으며, 기본 모델명은 `gpt-4.1-mini`이다. 현재 제출용 정량 평가는 재현성을 위해 deterministic local script를 사용한다.

향후 실제 홈페이지 배포 시에는 앱을 `trade-yh.com`에 위젯 또는 iframe 방식으로 연결할 수 있으며, API는 예를 들어 `https://api.trade-yh.com/api/chat`처럼 별도로 호스팅할 수 있다. 현재 저장소에는 앱 코드, 정적 프론트엔드 파일, 프롬프트, 로컬 RAG 문서, 평가 스크립트, 발표자료, 배포 안내가 포함되어 있다.

## 6. 실험

본 연구는 30개 케이스 벤치마크를 구축하였다. 구성은 OEM/ODM 6개, 구매대행 6개, 시장조사 5개, 불량 클레임 5개, 물류/통관 5개, 일반 또는 범위 외 문의 3개이다.

모든 시스템은 동일한 데이터셋인 `data/eval_cases/trade_support_30_cases.jsonl`에서 평가되며, 동일한 평가 스크립트인 `experiments/evaluate.py`를 사용한다.

Baseline은 다음과 같다.

- Baseline LLM: 검색이나 Reflection 없이 직접 단일 응답을 생성하는 baseline
- Baseline RAG: 의도 분류와 검색은 수행하지만, 역할이 분리된 Risk Agent 또는 Critic loop가 없는 baseline
- Proposed: Multi-Agent + RAG + Reflection

재현성을 위해 제출된 정량 결과는 외부 GPT 또는 Claude API 호출이 아니라 deterministic local script로 생성하였다. 앱 구현은 선택적으로 OpenAI-compatible model 설정을 지원하며, `OPENAI_API_KEY`가 제공되는 경우 기본 모델은 `gpt-4.1-mini`이다. 본 보고된 실험에서는 Claude를 사용하지 않았다.

평가 지표는 다음과 같다.

- Intent accuracy
- Groundedness proxy
- Required-information coverage
- Overpromise rate
- Human-review signal
- Average latency

주요 보고 점수는 required-information coverage이다. 각 벤치마크 케이스마다 제품 사진, 수량, 사양, 검수 증빙, 배송지, 통관/인증 맥락 등 필수 키워드 또는 정보 항목을 정의한다. 이 지표는 답변에 포함된 필수 항목의 비율을 계산한 뒤 30개 케이스에 대해 평균을 낸다.

결과는 다음과 같다.

- Baseline LLM: required-information coverage 0.139
- Baseline RAG: required-information coverage 0.678
- Proposed Multi-Agent + RAG + Reflection: required-information coverage 0.967

### 정성 비교

본 연구는 답변 양상도 정성적으로 비교하였다. OEM/샘플 제작 문의에서 일반 GPT-style baseline은 제조에 대한 일반적인 안내를 제공하는 경향이 있다. 답변은 자연스러울 수 있지만, 제품 이미지, 상세 사양, 패턴, 수량, 로고/패키지 파일, 희망 납기, 배송지와 같은 업무별 접수 정보를 누락할 수 있다. 또한 공급처 확인 전에도 제작 가능성을 암시할 수 있다.

RAG-only baseline은 `services_oem_odm.md`와 `quotation_required_fields.md` 같은 서비스 문서를 검색하므로 근거성이 개선된다. 그러나 별도의 Risk Agent와 Critic Agent가 없기 때문에 안전하지 않은 확정 표현을 통제하는 능력과 최종 답변이 필수 정보를 실제로 요청했는지 검토하는 Reflection 능력이 약하다.

TradeCare-Agent는 세 단계를 결합하여 응답을 개선한다. 먼저 문의를 OEM/ODM으로 분류하고, 관련 지식 베이스 문서를 검색하며, 구체적인 누락 정보를 요청한다. 또한 MOQ, 샘플비, 납기, 생산 가능 여부, 통관, 인증, 환불, 보상은 최종 안내 전에 반드시 확인되어야 한다고 명시한다. 따라서 제안 시스템은 단일 LLM 응답보다 근거성이 높을 뿐 아니라, 실제 고객센터 접수 workflow에 더 실용적이다.

### 고객 질문 20개 사례

30개 정량 벤치마크 외에도, 발표와 정성 평가를 위해 실제 고객 문의에 가까운 20개 사례를 준비하였다. 이 사례들은 통관 지연, 무역 계약서 검토, EU 의류 수출 서류, 선적 정보 수정, 통관 신고 금액 수정, 식품 수입 검역, 세관 압류, FOB 비용 책임, 저위험 결제 방식, 운송 중 화물 손상 청구, 전자제품 수입 관세, 원산지 증명서 재발급, 혼적 화물 통관 신고, CIF/CFR 보험 책임, 통관 지연 및 경매 위험, 중국 거래처 수출입 자격 조회, 항공 및 해상 운임 계산, 수하인의 화물 포기, FTA 관세 우대 증빙, 관세 연체료 감면을 포함한다.

각 사례에는 예상 답변 핵심, 즉 gold-standard checklist를 정의하였다. 예를 들어 통관 지연 문의는 지연 원인 확인, 세관 공식 문의, 추가 서류 필요 여부 확인을 포함해야 한다. 화물 손상 사례는 책임 주체 분석, 청구 서류, 청구 절차, 보험 연계 처리를 포함해야 한다. 이러한 20개 사례는 TradeCare-Agent가 프로젝트 평가를 넘어 실제 고객 서비스 FAQ와 데모 시나리오 라이브러리로 확장될 수 있음을 보여준다.

사람 평가를 위해서는 required-information coverage, actionability, groundedness, risk handling에 대해 1-5점 rubric을 사용할 것을 권장한다.

## 7. 한계와 윤리

본 시스템은 법률, 통관, 인증, 공급처 책임, 환불에 대한 최종 결정을 내릴 수 없다. 무역 지원은 문서, 계약, 검수 기록, 공급처 협상, 규정에 따라 달라지는 경우가 많다. 따라서 본 시스템은 자율적인 최종 결정자가 아니라 접수 및 상담 보조 도구로 사용되어야 한다.

잠재적 위험에는 회사 역량에 대한 환각, 부정확한 통관 조언, 고객 문서의 개인정보 유출, 책임 민감도가 높은 분쟁의 과도한 자동화가 포함된다. 완화 방안으로는 RAG 기반 근거화, 리스크 필터링, Critic Reflection, 사람 검토 단계, 명시적 불확실성 표현이 있다.

## 8. 결론

TradeCare-Agent는 현실적인 중한 B2B 무역 고객 지원 과제에서 Multi-Agent 설계, RAG, Reflection을 결합할 수 있음을 보여준다. 본 프로젝트는 실행 가능한 코드, FastAPI 웹앱, 로컬 지식 문서, 프롬프트, 벤치마크 케이스, 20개 실제형 고객 질문 사례, baseline 비교, 재현 가능한 평가 스크립트, 발표자료, GitHub 저장소 산출물을 제공한다.

