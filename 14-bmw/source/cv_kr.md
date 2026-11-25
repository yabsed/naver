# 설한동

* 이메일: yabsed@snu.ac.kr
* 전화: 010-4163-0786
* 거주지: 용인/서울
* GitHub: [yabsed](<https://github.com/yabsed>)

## 어학 능력

* 한국어: 모국어
* 영어: 고급
    * OPIc AL (2026/09/22)

## 학력

**서울대학교**  
컴퓨터공학부 학사 과정  
*2021년 3월 – 2027년 2월 (졸업 예정)*  
학점: 3.64/4.30

## 기술 역량

**프로그래밍 언어**: Python, TypeScript, C++, SQL
**프레임워크**: FastAPI, Django, React, Next.js, Svelte
**머신러닝**: PyTorch, CatBoost, XGBoost, scikit-learn
**인프라**: AWS, Docker, GitHub Actions, CloudFormation
**데이터베이스**: PostgreSQL, MySQL

## 프로젝트

### 1. 연구 프로젝트

#### 1-1. 학부 졸업논문: SSD 처리량 포화를 고려한 타일 기반 선택적 가중치 로딩

[yabsed/vlm-in-flash-jupyter](<https://github.com/yabsed/vlm-in-flash-jupyter>)

*학부 연구생 | 2026년 9월 – 현재*  
*Python, PyTorch, Jupyter, C++*

- [선행 연구](<https://arxiv.org/abs/2511.18692>)의 최적화 목적함수에서 한계를 발견함. 최대 R개의 행을 선택하는 제약 아래에서는 하나의 연속 구간을 선택하는 것만으로도 항상 최적해를 얻을 수 있음을 확인함.
- 정확히 R개의 행을 선택하도록 문제를 재정의하고, 충분히 큰 읽기 요청에서는 바이트당 비용이 거의 일정해지는 SSD 처리량 포화 특성을 활용하여 타일 기반 선택 방식을 탐구함.
- Qwen2.5-0.5B 활성화 추적 데이터와 직접 SSD I/O 벤치마크를 사용하여 제안 방식을 동적 계획법 및 기존 선택 방식과 비교 평가함.

#### 1-2. LLVM 컴파일러 최적화 — SWPP 타깃 머신

[gs18113/swpp202601-team04](<https://github.com/gs18113/swpp202601-team04>)

*컴파일러 최적화 개발 담당 (팀 프로젝트) | 2026년 3월 – 6월*  
*C++, LLVM IR, LLVM Pass Manager, FileCheck, Alive2, CMake*

- 커스텀 타깃 머신을 위한 LLVM IR 최적화 패스를 개발함. 홀짝 정보를 활용한 산술식 재작성, 시프트 연산의 곱셈 변환, 명령어 스케줄링, GEP 주소 정규화를 구현함.
- popcount 루프 패턴 인식과 SWAR 기반 저수준 변환을 구현하여, 세 가지 비트 수 계산 벤치마크에서 시뮬레이션 실행 비용을 79–80% 절감함.
- 타깃 특화 이득 판단 휴리스틱을 적용하여 LLVM의 loop unroll-and-jam 최적화를 통합하고, 인자의 홀짝 정보에 따른 특수화를 개발함. FileCheck, Alive2 및 벤치마크 테스트로 변환을 검증함.

#### 1-3. FetalGuard AI: CTG 파형 특징 추출을 통한 이상 예측 성능 개선

[yabsed/fetalguard-ctu-uhb](<https://github.com/yabsed/fetalguard-ctu-uhb>)
[yabsed/fetalguard-results](<https://github.com/yabsed/fetalguard-results>)

*머신러닝 연구 담당 | 2026년 8월 – 현재*  
*Python, CatBoost, XGBoost, PyTorch, scikit-learn, Jupyter*

**본선 진출 (상위 15개 팀) — [2026 K-Health 미공개 의료데이터 활용 경진대회](<https://daker.ai/community/2026-k-health-medical-data-competition>)**

- Google Research의 CTG 전처리 및 특징 추출 방법을 재현하고 확장하여, 5분 길이의 태아 심박수와 자궁 수축 기록에서 임상적으로 의미 있는 특징 28개를 추출함.
- 전문가가 이상 여부를 판정한 CTG 데이터를 예측하도록 CatBoost 그래디언트 부스팅 트리 모델을 학습시킴. 평가용으로 분리한 9,458개 구간에서 AUROC 0.872, 평균 정밀도(AP) 0.611을 달성함.
- 특징별 기여도, 전처리 민감도 및 병원 간 일반화 성능을 평가하고, 특징 기반 접근법을 XGBoost 및 경량 CNN 모델과 비교함.

#### 1-4. 컴퓨터 그래픽스: 3D 렌더링 및 애니메이션

[yabsed/Computer-Graphics](<https://github.com/yabsed/Computer-Graphics>)

*개인 교과 프로젝트 | 2025년 3월 – 6월*  
*Python, Pyglet, OpenGL, NumPy, Numba*

- 계층적 변환, 관절형 캐릭터 애니메이션 및 Catmull–Rom 스플라인 기반 움직임을 갖춘 인터랙티브 3D 장면을 개발함.
- Phong 조명, 부드러운 그림자, 재귀적 반사, 텍스처 매핑 및 슈퍼샘플링 안티앨리어싱을 지원하는 CPU 레이 트레이서를 구현함.
- 경계 볼륨 계층 구조(BVH), Numba JIT 컴파일 및 병렬 처리로 레이 트레이싱을 최적화하여, 200×200 벤치마크에서 렌더링 시간을 140.74초에서 67.72초로 단축함.

#### 1-5. 수학 학습 — 수학적 기초 및 알고리즘

[yabsed/onlymath](<https://github.com/yabsed/onlymath>)

*자기주도 학습 | 2025년 9월 – 현재*  
*선형대수학, 실해석학, 정수론, 머신러닝 이론, C++*

- 선형대수학, 실해석학 및 정수론을 자기주도적으로 학습하며 수학 노트, 교재 증명 및 문제 풀이 자료를 정리함.
- 체계적인 유도 과정과 해설 노트를 통해 볼록 쌍대성, SVM 최적화, 일반화 오차 경계 및 퍼셉트론 수렴 등 머신러닝의 수학적 기초를 학습함.
- 그래프 알고리즘, 문자열 매칭, 구간 질의 자료구조 및 네트워크 플로우 등의 알고리즘을 C++로 구현하고 문서화함.

### 2. 소프트웨어 개발 프로젝트

#### 2-1. Waffletime: 에브리타임 클론 백엔드

[yabsed/waffletime](<https://github.com/yabsed/waffletime>)

*백엔드 개발 담당 | 2021년 12월 – 2022년 1월*  
*Python, Django REST Framework, MySQL, Firebase, JWT*

- 강의 검색, 시간표 관리, 강의평 및 시험 정보를 위한 REST API를 개발함.
- 시간 중복 감지, 사용자 정의 강의 입력 및 사용자별 접근 제어를 포함한 시간표 관리 기능을 구현함.
- 카카오 및 Firebase 인증, JWT 기반 로그인, 이메일 인증을 통합하고, 게시판 즐겨찾기와 인기 게시물 기능을 개발함.

#### 2-2. tangerine market: 당근마켓 클론 프런트엔드

[yabsed/tangerine](<https://github.com/yabsed/tangerine>)

*프런트엔드 개발 담당 | 2026년 1월 – 2월*  
*React, TypeScript, Zustand, TanStack Query, Mantine, GitHub Actions*

- 상품 목록, 위치 기반 검색, 경매, 입찰, 채팅 및 가상화폐 거래 기능을 갖춘 반응형 마켓플레이스 프런트엔드를 개발함.
- 상품 및 경매 관련 흐름을 재사용 가능한 컴포넌트와 훅으로 리팩터링하고, Zustand로 상태를 관리하며 TanStack Query로 API 응답을 캐싱함.
- 다국어 지원과 다크 모드를 구현하고, GitHub Actions를 통해 GitHub Pages 및 AWS S3/CloudFront로의 자동 배포를 구성함.

#### 2-3. localhost: 위치 기반 O2O 리워드 애플리케이션

[yabsed/localhost-Mobile](<https://github.com/yabsed/localhost-Mobile>)
[yabsed/localhost-commit-analysis](<https://github.com/yabsed/localhost-commit-analysis>)

*모바일 앱 개발 담당 | 2026년 2월*  
*React Native, Expo, TypeScript, Zustand*

**금상 — 제3회 와커톤 (2026)**

- 인터랙티브 지도, GPS 기반 매장 탐색 및 지도와 연동되는 스와이프형 매장 카드를 갖춘 모바일 애플리케이션을 개발함.
- 영수증 인증, 카메라 기반 보물찾기, 지정 시간 방문 및 재방문 보상 등을 포함한 다섯 가지 위치 기반 미션 흐름을 구현하고, 검증과 보상 추적을 위한 백엔드 API를 연동함.
- 로그인 상태 유지, GPS 근접 여부 확인 및 카메라 이미지 압축을 통합하여 안정적인 모바일 이용을 지원함.

#### 2-4. allclear: 대학 동아리 탐색 및 관리 플랫폼

[wafflestudio/allclear](<https://github.com/wafflestudio/allclear>)
[wafflestudio/allclear-web](<https://github.com/wafflestudio/allclear-web>)
[Google Play](<https://play.google.com/store/apps/details?id=com.padocorp.clubhouse.applicationId&hl=ko>)
[App Store](<https://apps.apple.com/us/app/%EC%84%9C%EC%9A%B8%EB%8C%80-%EB%AA%A8%EB%93%A0-%EB%8F%99%EC%95%84%EB%A6%AC-%EC%98%AC%ED%81%B4/id6461214029>)

*풀스택 개발 담당 | 2026년 4월 – 현재*  
*TypeScript, Next.js, React, PostgreSQL, TypeORM, Zod*

- 동아리 등록, 모집 관리 및 검색을 위한 REST API를 개발하고, 데이터베이스 엔티티를 재설계하며 Zod 기반 OpenAPI 문서화를 도입함.
- 동아리 승인, 관리자 지정, 공식 인증 및 변경 이력 추적을 위한 관리 대시보드와 백엔드 처리 흐름을 구축함.
- 동아리 탐색과 검색, 카카오 인증, 관심 동아리 저장 및 사용자 리뷰 등 모바일 애플리케이션의 핵심 기능을 웹으로 확장함.

#### 2-5. setdown: 크로스 플랫폼 Markdown 편집기 및 작업 공간

[yabsed/setdown](<https://github.com/yabsed/setdown>)

*개인 개발 (AI 활용) | 2026년 9월 – 현재*  
*TypeScript, Electron, Svelte, Monaco Editor, Jupyter, GitHub Actions*

- 소스 편집과 렌더링된 문서 사이를 자연스럽게 전환할 수 있는 데스크톱 Markdown 편집기를 기획하고, AI를 활용한 개발을 주도함.
- Jupyter 노트북, 언어 서버 지원, Git 버전 관리, 웹 탐색, PDF 보기 및 터미널 기능을 하나의 작업 공간에 통합하도록 개발을 이끎.
- Markdown 렌더링과 Git diff 미리보기의 성능 최적화 및 회귀 테스트를 조율하고, 벤치마크와 자동화 테스트로 개선 효과를 평가함.
- CI/CD 흐름과 크로스 플랫폼 릴리스를 관리하고, GitHub Actions를 통해 Windows 및 Linux 설치 파일을 배포함.

#### 2-6. chess: 실시간 멀티플레이어 체스 애플리케이션

[yabsed/chess](<https://github.com/yabsed/chess>)

*개인 개발 (AI 활용) | 2026년 10월 – 현재*  
*Python, FastAPI, Socket.IO, PostgreSQL, SQLAlchemy, Svelte, AWS, CloudFormation, GitHub Actions*

- 매치메이킹, 비공개 초대, 사용자 인증 및 Socket.IO를 통한 게임 상태 동기화 기능을 갖춘 실시간 멀티플레이어 체스 애플리케이션을 개발함.
- PostgreSQL 데이터 저장과 SQLAlchemy ORM을 활용하는 FastAPI 백엔드를 구축하여, 게임 세션 영속성, 수 유효성 검증 및 재접속 처리를 지원함.
- CloudFormation으로 AWS 인프라를 관리하고, ECS, EC2, RDS, ECR, ALB 및 CloudFront를 자동화된 CI/CD와 배포 검증에 통합함.
- ECS 워크로드를 ARM 기반 EC2 인스턴스로 이전하고, 데이터베이스의 비공개 접근을 유지하면서 NAT 게이트웨이를 제거하여 인프라 비용을 최적화함.

## 병역

**대한민국 공군**  
통신 담당 (네트워크 및 IT 지원)  
*2023년 3월 – 2024년 12월*

- 군 시설 내 UTP(이더넷) 케이블과 유선 네트워크 연결을 유지보수하고 수리함.
- 네트워크 스위치와 허브를 설치하여 LAN 연결을 확장하고, 여러 장치가 하나의 이더넷 업링크를 공유할 수 있도록 구성함.
- 부대 전반의 컴퓨터 유지보수와 문제 해결을 담당하며 일상적인 IT 운영을 지원함.
