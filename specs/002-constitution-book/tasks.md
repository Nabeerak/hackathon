# Tasks: Physical AI & Humanoid Robotics Textbook

**Input**: Design documents from `/specs/002-constitution-book/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Manual content review and build verification (not automated TDD)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Documentation**: `docusaurus-book/docs/physical-ai-textbook/`
- **Images**: `docusaurus-book/static/img/physical-ai-textbook/`
- **Config**: `docusaurus-book/sidebars.ts`, `docusaurus-book/docusaurus.config.ts`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure

- [x] T001 Create main textbook directory at docusaurus-book/docs/physical-ai-textbook/
- [x] T002 [P] Create course-overview directory at docusaurus-book/docs/physical-ai-textbook/course-overview/
- [x] T003 [P] Create hardware-infrastructure directory at docusaurus-book/docs/physical-ai-textbook/hardware-infrastructure/
- [x] T004 [P] Create ros2-fundamentals directory at docusaurus-book/docs/physical-ai-textbook/ros2-fundamentals/
- [x] T005 [P] Create digital-twin-simulation directory at docusaurus-book/docs/physical-ai-textbook/digital-twin-simulation/
- [x] T006 [P] Create nvidia-isaac directory at docusaurus-book/docs/physical-ai-textbook/nvidia-isaac/
- [x] T007 [P] Create vision-language-action directory at docusaurus-book/docs/physical-ai-textbook/vision-language-action/
- [x] T008 [P] Create humanoid-robotics directory at docusaurus-book/docs/physical-ai-textbook/humanoid-robotics/
- [x] T009 [P] Create appendices directory at docusaurus-book/docs/physical-ai-textbook/appendices/
- [x] T010 [P] Create image directories for all chapters at docusaurus-book/static/img/physical-ai-textbook/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T011 Update sidebars.ts to add physicalAiTextbook sidebar configuration per contracts/sidebar-schema.ts
- [x] T012 Verify search plugin configuration in docusaurus.config.ts for @easyops-cn/docusaurus-search-local
- [x] T013 Create book introduction page at docusaurus-book/docs/physical-ai-textbook/index.md with frontmatter and overview
- [ ] T014 Test local development server (npm start) to verify setup and navigation structure
- [ ] T015 Run build test (npm run build) to ensure production build succeeds

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Read Comprehensive Textbook Content (Priority: P1) 🎯 MVP

**Goal**: Create comprehensive textbook content covering all Physical AI topics from constitution with proper structure, learning objectives, and code examples

**Independent Test**: Navigate through Docusaurus site and verify all constitutional topics are covered with clear explanations, code examples, and learning objectives

### Implementation for User Story 1

#### Course Overview Section (US1)

- [ ] T016 [P] [US1] Create learning outcomes page at docusaurus-book/docs/physical-ai-textbook/course-overview/learning-outcomes.md with all course objectives
- [ ] T017 [P] [US1] Create weekly breakdown page at docusaurus-book/docs/physical-ai-textbook/course-overview/weekly-breakdown.md mapping 12 weeks to chapters
- [ ] T018 [P] [US1] Create prerequisites page at docusaurus-book/docs/physical-ai-textbook/course-overview/prerequisites.md with required background

#### Hardware & Infrastructure Chapter (US1)

- [ ] T019 [US1] Create hardware chapter index at docusaurus-book/docs/physical-ai-textbook/hardware-infrastructure/index.md with learning objectives
- [ ] T020 [P] [US1] Create digital twin workstation page at docusaurus-book/docs/physical-ai-textbook/hardware-infrastructure/digital-twin-workstation.md with specs table (RTX 4070 Ti+, i7 13th Gen+, 64GB RAM, Ubuntu 22.04)
- [ ] T021 [P] [US1] Create physical AI edge kits page at docusaurus-book/docs/physical-ai-textbook/hardware-infrastructure/physical-ai-edge-kits.md with Jetson Orin Nano/NX, RealSense D435i/D455 specs
- [ ] T022 [P] [US1] Create robot lab options page at docusaurus-book/docs/physical-ai-textbook/hardware-infrastructure/robot-lab-options.md with Unitree Go2/G1, Robotis OP3, Hiwonder TonyPi Pro specs
- [ ] T023 [P] [US1] Create cloud-native alternatives page at docusaurus-book/docs/physical-ai-textbook/hardware-infrastructure/cloud-native-alternatives.md with AWS/Azure Isaac Sim options

#### ROS 2 Fundamentals Chapter (US1)

- [ ] T024 [US1] Create ROS 2 chapter index at docusaurus-book/docs/physical-ai-textbook/ros2-fundamentals/index.md with learning objectives and prerequisites
- [ ] T025 [P] [US1] Create installation page at docusaurus-book/docs/physical-ai-textbook/ros2-fundamentals/installation.md with Ubuntu 22.04 ROS 2 Humble setup
- [ ] T026 [P] [US1] Create nodes and topics page at docusaurus-book/docs/physical-ai-textbook/ros2-fundamentals/nodes-topics.md with publisher/subscriber code examples (Python)
- [ ] T027 [P] [US1] Create services and actions page at docusaurus-book/docs/physical-ai-textbook/ros2-fundamentals/services-actions.md with service client/server code examples
- [ ] T028 [P] [US1] Create parameters and launch files page at docusaurus-book/docs/physical-ai-textbook/ros2-fundamentals/parameters-launch.md with YAML configuration examples
- [ ] T029 [P] [US1] Create navigation stack page at docusaurus-book/docs/physical-ai-textbook/ros2-fundamentals/navigation-stack.md with Nav2 setup and configuration
- [ ] T030 [P] [US1] Create debugging tools page at docusaurus-book/docs/physical-ai-textbook/ros2-fundamentals/debugging-tools.md with ros2 CLI commands

#### Digital Twin Simulation Chapter (US1)

- [ ] T031 [US1] Create digital twin chapter index at docusaurus-book/docs/physical-ai-textbook/digital-twin-simulation/index.md with learning objectives
- [ ] T032 [P] [US1] Create Gazebo basics page at docusaurus-book/docs/physical-ai-textbook/digital-twin-simulation/gazebo-basics.md with world file examples
- [ ] T033 [P] [US1] Create Unity simulation page at docusaurus-book/docs/physical-ai-textbook/digital-twin-simulation/unity-simulation.md with Unity-ROS 2 integration
- [ ] T034 [P] [US1] Create URDF modeling page at docusaurus-book/docs/physical-ai-textbook/digital-twin-simulation/urdf-modeling.md with robot description examples
- [ ] T035 [P] [US1] Create sensor integration page at docusaurus-book/docs/physical-ai-textbook/digital-twin-simulation/sensor-integration.md with camera, lidar, IMU examples
- [ ] T036 [P] [US1] Create physics simulation page at docusaurus-book/docs/physical-ai-textbook/digital-twin-simulation/physics-simulation.md with collision, friction, dynamics

#### NVIDIA Isaac Platform Chapter (US1)

- [ ] T037 [US1] Create NVIDIA Isaac chapter index at docusaurus-book/docs/physical-ai-textbook/nvidia-isaac/index.md with learning objectives
- [ ] T038 [P] [US1] Create Isaac Sim intro page at docusaurus-book/docs/physical-ai-textbook/nvidia-isaac/isaac-sim-intro.md with platform overview
- [ ] T039 [P] [US1] Create Omniverse setup page at docusaurus-book/docs/physical-ai-textbook/nvidia-isaac/omniverse-setup.md with installation and configuration
- [ ] T040 [P] [US1] Create robot brain AI page at docusaurus-book/docs/physical-ai-textbook/nvidia-isaac/robot-brain-ai.md with Isaac SDK AI modules
- [ ] T041 [P] [US1] Create perception systems page at docusaurus-book/docs/physical-ai-textbook/nvidia-isaac/perception-systems.md with computer vision and depth sensing
- [ ] T042 [P] [US1] Create SLAM and navigation page at docusaurus-book/docs/physical-ai-textbook/nvidia-isaac/slam-navigation.md with mapping algorithms
- [ ] T043 [P] [US1] Create sim-to-real transfer page at docusaurus-book/docs/physical-ai-textbook/nvidia-isaac/sim-to-real-transfer.md with domain randomization

#### Vision-Language-Action Chapter (US1)

- [ ] T044 [US1] Create VLA chapter index at docusaurus-book/docs/physical-ai-textbook/vision-language-action/index.md with learning objectives
- [ ] T045 [P] [US1] Create VLA overview page at docusaurus-book/docs/physical-ai-textbook/vision-language-action/vla-overview.md with model architecture explanation
- [ ] T046 [P] [US1] Create multimodal models page at docusaurus-book/docs/physical-ai-textbook/vision-language-action/multimodal-models.md with vision-language foundation models
- [ ] T047 [P] [US1] Create action primitives page at docusaurus-book/docs/physical-ai-textbook/vision-language-action/action-primitives.md with robotic action spaces
- [ ] T048 [P] [US1] Create integration patterns page at docusaurus-book/docs/physical-ai-textbook/vision-language-action/integration-patterns.md with robot control integration
- [ ] T049 [P] [US1] Create training and fine-tuning page at docusaurus-book/docs/physical-ai-textbook/vision-language-action/training-fine-tuning.md with model adaptation

#### Humanoid Robotics Chapter (US1)

- [ ] T050 [US1] Create humanoid robotics chapter index at docusaurus-book/docs/physical-ai-textbook/humanoid-robotics/index.md with learning objectives
- [ ] T051 [P] [US1] Create bipedal locomotion page at docusaurus-book/docs/physical-ai-textbook/humanoid-robotics/bipedal-locomotion.md with walking gait control
- [ ] T052 [P] [US1] Create manipulation control page at docusaurus-book/docs/physical-ai-textbook/humanoid-robotics/manipulation-control.md with arm/hand control
- [ ] T053 [P] [US1] Create balance and stability page at docusaurus-book/docs/physical-ai-textbook/humanoid-robotics/balance-stability.md with ZMP and COM control
- [ ] T054 [P] [US1] Create conversational robotics page at docusaurus-book/docs/physical-ai-textbook/humanoid-robotics/conversational-robotics.md with speech recognition and synthesis
- [ ] T055 [P] [US1] Create GPT integration page at docusaurus-book/docs/physical-ai-textbook/humanoid-robotics/gpt-integration.md with LLM-based control
- [ ] T056 [P] [US1] Create HRI design page at docusaurus-book/docs/physical-ai-textbook/humanoid-robotics/hri-design.md with human-robot interaction principles

**Checkpoint**: At this point, User Story 1 should be fully functional - all core content created with learning objectives and code examples

---

## Phase 4: User Story 2 - Navigate Book Structure (Priority: P2)

**Goal**: Enable easy navigation between chapters and sections using Docusaurus features including sidebar, search, and breadcrumbs

**Independent Test**: Click through sidebar links, use search for technical terms (SLAM, ROS 2, VLA), verify breadcrumb trails work correctly

### Implementation for User Story 2

- [ ] T057 [US2] Verify sidebar navigation structure matches contracts/sidebar-schema.ts with all chapters and sections
- [ ] T058 [US2] Test sidebar expansion and collapse for all chapter categories
- [ ] T059 [US2] Add cross-references between related sections using markdown links
- [ ] T060 [P] [US2] Ensure all pages have proper frontmatter with keywords for search indexing
- [ ] T061 [US2] Test search functionality for key terms: "ROS 2", "SLAM", "Isaac Sim", "VLA", "Gazebo", "URDF"
- [ ] T062 [US2] Verify breadcrumb navigation shows correct hierarchy (Book → Chapter → Section)
- [ ] T063 [US2] Test "Previous" and "Next" page navigation at bottom of content pages
- [ ] T064 [US2] Verify table of contents appears on right sidebar for long pages
- [ ] T065 [US2] Test navigation from any page to related content within 3 clicks (SC-003)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - content is navigable and searchable

---

## Phase 5: User Story 3 - Access Hardware Requirements and Lab Setup (Priority: P3)

**Goal**: Provide detailed hardware specifications with multiple options (workstation, edge kit, cloud-native) for students and administrators

**Independent Test**: Navigate to hardware sections and verify all specs from constitution are documented with clear cost estimates and alternatives

### Implementation for User Story 3

- [ ] T066 [US3] Verify Digital Twin Workstation page has minimum and recommended configurations with cost estimates
- [ ] T067 [US3] Verify Physical AI Edge Kits page documents all components (Jetson Orin Nano/NX, RealSense cameras, IMU, microphone/speaker)
- [ ] T068 [US3] Verify Robot Lab Options page includes detailed specs for all 4 robot platforms (Unitree Go2 Edu, Unitree G1, Robotis OP3, Hiwonder TonyPi Pro)
- [ ] T069 [US3] Verify Cloud-Native Alternatives page explains AWS/Azure instance requirements for Isaac Sim on Omniverse Cloud
- [ ] T070 [P] [US3] Add comparison table showing workstation vs edge kit vs cloud options with pros/cons
- [ ] T071 [P] [US3] Add vendor links and purchase information for all hardware components
- [ ] T072 [US3] Verify hardware chapter provides at least 3 different implementation options (SC-005)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 work independently - hardware information is complete and accessible

---

## Phase 6: User Story 4 - Understand Course Learning Outcomes (Priority: P3)

**Goal**: Provide comprehensive learning outcomes, course structure, and weekly breakdown for students and instructors

**Independent Test**: Review learning outcomes page and verify alignment with weekly breakdown and chapter structure

### Implementation for User Story 4

- [ ] T073 [US4] Verify learning outcomes page lists all major skills students will acquire
- [ ] T074 [US4] Verify weekly breakdown maps all 7 chapters to 12-week course structure
- [ ] T075 [US4] Ensure each week includes reading assignments, lab activities, and deliverables
- [ ] T076 [US4] Verify prerequisites page lists required background knowledge clearly
- [ ] T077 [P] [US4] Add estimated study hours for each week (6-12 hours per week)
- [ ] T078 [P] [US4] Link weekly topics to specific chapter sections for easy navigation
- [ ] T079 [US4] Verify course structure satisfies SC-004 (12-week mapping)

**Checkpoint**: All user stories should now be independently functional - complete textbook with navigation, hardware info, and course structure

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality checks

### Content Quality & Validation

- [ ] T080 [P] Review all chapter indexes to ensure learning objectives are present (SC-008)
- [ ] T081 [P] Verify all code examples include prerequisites and expected output (FR-013)
- [ ] T082 [P] Check all hardware specifications for technical accuracy (SC-009)
- [ ] T083 [P] Validate frontmatter on all pages has required fields (title, sidebar_label, sidebar_position)
- [ ] T084 [P] Ensure consistent terminology usage across all chapters
- [ ] T085 [P] Verify all external links work correctly
- [ ] T086 Review content coverage against FR-001 through FR-015 to ensure 100% compliance

### Appendices

- [ ] T087 [P] Create glossary page at docusaurus-book/docs/physical-ai-textbook/appendices/glossary.md with technical term definitions
- [ ] T088 [P] Create additional resources page at docusaurus-book/docs/physical-ai-textbook/appendices/resources.md with external links
- [ ] T089 [P] Create troubleshooting guide at docusaurus-book/docs/physical-ai-textbook/appendices/troubleshooting.md with common issues

### Images & Diagrams (Optional)

- [ ] T090 [P] Add ROS 2 architecture diagram to docusaurus-book/static/img/physical-ai-textbook/ros2-fundamentals/architecture.svg
- [ ] T091 [P] Add Digital Twin workflow diagram to docusaurus-book/static/img/physical-ai-textbook/digital-twin-simulation/workflow.svg
- [ ] T092 [P] Add VLA model architecture diagram to docusaurus-book/static/img/physical-ai-textbook/vision-language-action/architecture.svg

### Testing & Deployment

- [ ] T093 Run local development server and manually test all navigation paths
- [ ] T094 Test responsive design on mobile device (or browser DevTools mobile view)
- [ ] T095 Run production build (npm run build) and verify success
- [ ] T096 Run build output validation (check for broken links, missing images)
- [ ] T097 Test search functionality returns relevant results for all major terms (SC-007)
- [ ] T098 Verify all success criteria SC-001 through SC-010 are met
- [ ] T099 Deploy to GitHub Pages (npm run deploy) from docusaurus-book directory
- [ ] T100 Verify live site at GitHub Pages URL and test all functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) after Phase 2
  - Or sequentially in priority order: US1 (P1) → US2 (P2) → US3 (P3) → US4 (P3)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories - Creates all core content
- **User Story 2 (P2)**: Can start after US1 content exists - Enhances navigation and search - Independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2 - Hardware content can be written in parallel
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Independent of other stories - Course structure can be written in parallel

### Within Each User Story

- **US1**: Chapter indexes before sections, sections can be parallelized within chapters
- **US2**: Requires US1 content to exist for navigation testing
- **US3**: Hardware pages can all be written in parallel
- **US4**: Course overview pages can be written in parallel

### Parallel Opportunities

- **Phase 1 (Setup)**: All T001-T010 can run in parallel (creating directories)
- **Phase 2 (Foundational)**: T012-T013 can run in parallel after T011
- **Phase 3 (US1)**:
  - T016-T018 (course overview) can run in parallel
  - T020-T023 (hardware sections) can run in parallel after T019
  - T025-T030 (ROS 2 sections) can run in parallel after T024
  - T032-T036 (digital twin sections) can run in parallel after T031
  - T038-T043 (Isaac sections) can run in parallel after T037
  - T045-T049 (VLA sections) can run in parallel after T044
  - T051-T056 (humanoid sections) can run in parallel after T050
- **Phase 5 (US3)**: T066-T072 can have parallel validation tasks (T070-T071)
- **Phase 6 (US4)**: T077-T078 can run in parallel
- **Phase 7 (Polish)**: T080-T092 can run in parallel

---

## Parallel Example: User Story 1 - ROS 2 Chapter

```bash
# After creating chapter index (T024), launch all section pages in parallel:
Task T025: "Create installation page"
Task T026: "Create nodes and topics page"
Task T027: "Create services and actions page"
Task T028: "Create parameters and launch files page"
Task T029: "Create navigation stack page"
Task T030: "Create debugging tools page"
```

## Parallel Example: Phase 7 - Content Quality

```bash
# All quality checks can run in parallel:
Task T080: "Review all chapter indexes"
Task T081: "Verify all code examples"
Task T082: "Check hardware specifications"
Task T083: "Validate frontmatter"
Task T084: "Check terminology consistency"
Task T085: "Verify external links"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T010)
2. Complete Phase 2: Foundational (T011-T015) - CRITICAL
3. Complete Phase 3: User Story 1 (T016-T056)
4. **STOP and VALIDATE**: Manually navigate through all chapters, verify content quality
5. Run build test and deploy to GitHub Pages for review

**MVP Deliverable**: Complete textbook with all 7 chapters covering Physical AI topics

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (T016-T056) → Test navigation → Deploy (MVP!)
3. Add User Story 2 (T057-T065) → Test search and breadcrumbs → Deploy
4. Add User Story 3 (T066-T072) → Verify hardware specs → Deploy
5. Add User Story 4 (T073-T079) → Verify course structure → Deploy
6. Polish (T080-T100) → Final quality checks → Production deploy

### Parallel Team Strategy

With multiple content writers:

1. Team completes Setup + Foundational together (T001-T015)
2. Once Foundational is done:
   - Writer A: Course Overview + Hardware chapter (T016-T023)
   - Writer B: ROS 2 + Digital Twin chapters (T024-T036)
   - Writer C: NVIDIA Isaac + VLA chapters (T037-T049)
   - Writer D: Humanoid Robotics chapter (T050-T056)
3. All writers contribute to Polish phase (T080-T100)

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Use quickstart.md guide for content creation standards
- Follow frontmatter-schema.yaml for all page metadata
- Reference data-model.md for content entity structure
- Verify build succeeds after each major phase
- Each chapter must have minimum 5 sections (SC-002)
- Navigation must be within 3 clicks (SC-003)
- All constitutional topics must be covered (SC-001)

---

## Task Summary

**Total Tasks**: 100 tasks
- **Phase 1 (Setup)**: 10 tasks (all parallelizable)
- **Phase 2 (Foundational)**: 5 tasks (blocks all stories)
- **Phase 3 (US1 - Core Content)**: 41 tasks (MVP - most parallelizable within chapters)
- **Phase 4 (US2 - Navigation)**: 9 tasks
- **Phase 5 (US3 - Hardware)**: 7 tasks (mostly parallelizable)
- **Phase 6 (US4 - Course Structure)**: 7 tasks (mostly parallelizable)
- **Phase 7 (Polish)**: 21 tasks (many parallelizable)

**Parallel Opportunities**: 65+ tasks marked [P] can run concurrently if team capacity allows

**MVP Scope**: Phases 1-3 (56 tasks) deliver complete textbook content

**Independent Test Criteria**:
- **US1**: Navigate all chapters, verify topics covered with learning objectives and code examples
- **US2**: Test sidebar, search, breadcrumbs work correctly
- **US3**: Verify hardware specs complete with 3+ options
- **US4**: Verify 12-week course mapping complete

**Suggested MVP**: Complete US1 first (Phases 1-3), then add US2-US4 incrementally