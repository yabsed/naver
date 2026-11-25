# Seol Handong

* email: yabsed@snu.ac.kr
* tel: 010-4163-0786
* city: Yongin/Seoul
* github id: [yabsed](<https://github.com/yabsed>)


## Language Skills
* Korean: Native
* English: Advanced
    * OPIc AL (2026/09/22)

## Education

**Seoul National University**  
B.S. in Computer Science and Engineering  
*Mar 2021 – Feb 2027 (Expected)*  
GPA: 3.64/4.30

## Technical Skills

**Languages**: Python, TypeScript, C++, SQL
**Frameworks**: FastAPI, Django, React, Next.js, Svelte
**ML**: PyTorch, CatBoost, XGBoost, scikit-learn
**Infrastructure**: AWS, Docker, GitHub Actions, CloudFormation
**Databases**: PostgreSQL, MySQL

## Projects 

### 1. Research Projects

#### 1-1. Undergraduate Thesis: Tile-Based Selective Weight Loading Accounting for SSD Throughput Saturation

[yabsed/vlm-in-flash-jupyter](<https://github.com/yabsed/vlm-in-flash-jupyter>)

*Undergraduate Researcher | Sep 2026 - Present*  
*Python, PyTorch, Jupyter, C++*

- Identified a limitation in the optimization objective of [prior research:](<https://arxiv.org/abs/2511.18692>) under an at-most-R row budget, an optimal solution can always be achieved by selecting a single contiguous chunk.
- Reformulated the problem to require exactly R rows and explored tile-based selection by exploiting SSD throughput saturation, where sufficiently large reads have nearly constant per-byte costs.
- Evaluated the proposed approach against dynamic programming and existing selection methods using Qwen2.5-0.5B activation traces and direct SSD I/O benchmarks.

#### 1-2. LLVM Compiler Optimization — SWPP Target Machine

[gs18113/swpp202601-team04](<https://github.com/gs18113/swpp202601-team04>)

*Compiler Optimization Developer (Team Project) | Mar - Jun 2026*  
*C++, LLVM IR, LLVM Pass Manager, FileCheck, Alive2, CMake*

- Developed LLVM IR optimization passes for a custom target machine, including parity-aware arithmetic rewriting, shift-to-multiplication transformations, instruction scheduling, and GEP address canonicalization.
- Implemented popcount loop-idiom recognition and SWAR-based lowering, reducing simulated execution costs by 79–80% across three bit-count benchmarks.
- Integrated LLVM's loop unroll-and-jam optimization with a target-specific profitability heuristic and developed argument-parity specialization, validating transformations using FileCheck, Alive2, and benchmark testing.

#### 1-3. FetalGuard AI: Improving Abnormality Prediction Through CTG Waveform Feature Extraction

[yabsed/fetalguard-ctu-uhb](<https://github.com/yabsed/fetalguard-ctu-uhb>)
[yabsed/fetalguard-results](<https://github.com/yabsed/fetalguard-results>)

*ML Researcher | Aug 2026 - Present*  
*Python, CatBoost, XGBoost, PyTorch, scikit-learn, Jupyter*

**Finalist (Top 15 Teams) — [2026 K-Health Unreleased Medical Data Utilization Competition](<https://daker.ai/community/2026-k-health-medical-data-competition>)**

- Reproduced Google Research's CTG preprocessing and feature-extraction methods, extending them to extract 28 clinically meaningful features from five-minute fetal heart rate and uterine contraction recordings.
- Trained a CatBoost gradient-boosted tree model to predict expert-labeled CTG abnormalities, achieving an AUROC of 0.872 and an average precision of 0.611 on 9,458 held-out segments.
- Evaluated feature contributions, preprocessing sensitivity, and cross-hospital generalization, comparing the feature-based approach against XGBoost and lightweight CNN models.

#### 1-4. Computer Graphics: 3D Rendering & Animation

[yabsed/Computer-Graphics](<https://github.com/yabsed/Computer-Graphics>)

*Individual Coursework Project | Mar - Jun 2025*  
*Python, Pyglet, OpenGL, NumPy, Numba*

- Developed interactive 3D scenes featuring hierarchical transformations, articulated character animation, and Catmull–Rom spline-based motion.
- Implemented a CPU ray tracer supporting Phong lighting, soft shadows, recursive reflections, texture mapping, and supersampling anti-aliasing.
- Optimized ray tracing using Bounding Volume Hierarchies (BVH), Numba JIT compilation, and parallel processing, reducing rendering time from 140.74s to 67.72s in a 200×200 benchmark.

#### 1-5. Math Study — Mathematical Foundations & Algorithms

[yabsed/onlymath](<https://github.com/yabsed/onlymath>)

*Independent Study | Sep 2025 - Present*  
*Linear Algebra, Real Analysis, Number Theory, Machine Learning Theory, C++*

- Pursued independent study in linear algebra, real analysis, and number theory, organizing mathematical notes, textbook proofs, and problem-solving materials.
- Studied the mathematical foundations of machine learning, including convex duality, SVM optimization, generalization bounds, and perceptron convergence, through structured derivations and explanatory notes.
- Implemented and documented algorithms in C++, including graph algorithms, string matching, range-query data structures, and network flow.

### 2. Software Engineering Projects

#### 2-1. Waffletime: Everytime Clone Backend

[yabsed/waffletime](<https://github.com/yabsed/waffletime>)

*Backend Developer | Dec 2021 - Jan 2022*  
*Python, Django REST Framework, MySQL, Firebase, JWT*

- Developed REST APIs for lecture search, timetable management, course reviews, and exam information.
- Implemented timetable scheduling with conflict detection, custom course entries, and user-specific access controls.
- Integrated Kakao and Firebase authentication, JWT-based login, and email verification; developed board favorites and trending-post features.

#### 2-2. tangerine market: Carrot Market Clone Frontend

[yabsed/tangerine](<https://github.com/yabsed/tangerine>)

*Frontend Developer | Jan 2026 - Feb 2026*  
*React, TypeScript, Zustand, TanStack Query, Mantine, GitHub Actions*

- Developed a responsive marketplace frontend featuring product listings, location-based search, auctions, bidding, chat, and virtual-currency transactions.
- Refactored product and auction workflows into reusable components and hooks, using Zustand for state management and TanStack Query for API caching.
- Implemented multilingual support, dark mode, and automated deployments to GitHub Pages and AWS S3/CloudFront using GitHub Actions.

#### 2-3. localhost: Location-Based O2O Rewards Application

[yabsed/localhost-Mobile](<https://github.com/yabsed/localhost-Mobile>)
[yabsed/localhost-commit-analysis](<https://github.com/yabsed/localhost-commit-analysis>)

*Mobile App Developer | Feb 2026*  
*React Native, Expo, TypeScript, Zustand*

**Gold Prize — 3rd Wacathon (2026)**

- Developed a mobile application featuring interactive maps, GPS-based store discovery, and synchronized swipeable store cards.
- Implemented five location-based mission workflows, including receipt verification, camera-based treasure hunts, timed visits, and repeat-visit rewards, integrating backend APIs for validation and reward tracking.
- Integrated persistent user authentication, GPS proximity checks, and camera image compression to support reliable mobile interactions.


#### 2-4. allclear: University Club Discovery & Management Platform  

[wafflestudio/allclear](<https://github.com/wafflestudio/allclear>)
[wafflestudio/allclear-web](<https://github.com/wafflestudio/allclear-web>)
[Play Store](<https://play.google.com/store/apps/details?id=com.padocorp.clubhouse.applicationId&hl=ko>)
[Apple Store](<https://apps.apple.com/us/app/%EC%84%9C%EC%9A%B8%EB%8C%80-%EB%AA%A8%EB%93%A0-%EB%8F%99%EC%95%84%EB%A6%AC-%EC%98%AC%ED%81%B4/id6461214029>)

*Full-Stack Developer | Apr 2026 - Present*  
*TypeScript, Next.js, React, PostgreSQL, TypeORM, Zod*

- Developed REST APIs for club registration, recruitment management, and search, while redesigning database entities and introducing Zod-based OpenAPI documentation.
- Built an administrative dashboard and backend workflows for club approvals, manager assignments, official verification, and change history tracking.
- Extended the mobile application's core features to the web, including club discovery, search, Kakao authentication, saved clubs, and user reviews.

#### 2-5. setdown: Cross-Platform Markdown Editor & Workspace

[yabsed/setdown](<https://github.com/yabsed/setdown>)

*Independent Developer (AI-Assisted) | Sep 2026 - Present*  
*TypeScript, Electron, Svelte, Monaco Editor, Jupyter, GitHub Actions*

- Conceived and directed AI-assisted development of a desktop Markdown editor, featuring seamless transitions between source editing and rendered documents.
- Guided the integration of Jupyter notebooks, language server support, Git version control, web browsing, PDF viewing, and terminal functionality into a unified workspace.
- Coordinated performance optimization and regression testing for Markdown rendering and Git diff previews, using benchmarks and automated tests to evaluate improvements.
- Managed CI/CD workflows and cross-platform releases, distributing Windows and Linux installers through GitHub Actions.

#### 2-6. chess: Real-Time Multiplayer Chess Application

[yabsed/chess](<https://github.com/yabsed/chess>)

*Independent Developer (AI-Assisted) | Oct 2026 - Present*  
*Python, FastAPI, Socket.IO, PostgreSQL, SQLAlchemy, Svelte, AWS, CloudFormation, GitHub Actions*

- Developed a real-time multiplayer chess application featuring matchmaking, private invitations, user authentication, and game-state synchronization through Socket.IO.
- Built a FastAPI backend with PostgreSQL persistence and SQLAlchemy ORM, supporting persistent game sessions, move validation, and reconnection handling.
- Managed AWS infrastructure using CloudFormation, integrating ECS, EC2, RDS, ECR, ALB, and CloudFront with automated CI/CD and deployment verification.
- Optimized infrastructure costs by migrating ECS workloads to ARM-based EC2 instances and eliminating the NAT gateway while preserving private database access.

## Military Service

**Republic of Korea Air Force**  
Communications Specialist (Network & IT Support)  
*Mar 2023 – Dec 2024*

- Maintained and repaired UTP (Ethernet) cabling and wired network connections across military facilities.
- Installed network switches and hubs to expand LAN connectivity, enabling multiple devices to share a single Ethernet uplink.
- Provided unit-wide computer maintenance and troubleshooting, supporting daily IT operations.
