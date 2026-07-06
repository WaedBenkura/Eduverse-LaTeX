# EduVerse Implementation Analysis Report

This report is based on the current EduVerse repository contents only. It uses the application code, API routes, shared libraries, tests, migrations, and project documentation in this repository as the source of truth. Where a capability is not present or not clearly implemented, that is stated explicitly.

## 1. Project Overview

EduVerse is implemented as a multi-organization learning workspace built on a Next.js web application. The codebase supports organization-scoped dashboards and class spaces with role-aware access to chat, materials, assignments, exams, live sessions, results, AI assistance, and extensions. The overall design is centered on a single authenticated user being able to belong to multiple organizations and to operate under different roles inside a selected organization.

The main implemented roles are:

- **Organization Administrator**: the code uses the internal role name `org_admin`. This role is associated with organization setup, feature configuration, user and invite management, public join links and requests, class management, archived class history, and organization settings.
- **Teacher**: teacher workflows include class creation and editing where permitted, roster activity within assigned classes, materials, assignments, grading, exams, live sessions, results visibility control in allowed cases, and AI-assisted academic support features.
- **Student**: student workflows include joining or accepting access to organizations, viewing enabled classes, chatting, opening materials, submitting assignments, taking exams, joining live sessions, viewing results when released, and using enabled class tools such as the AI agent or IDE.

This repository clearly contains the web application. It does **not** contain the mobile companion source code, but the README explicitly references a sibling repository `../Eduverse-mobile-app` as the mobile companion.

## 2. Technology Stack

- **Frontend framework and language**: Next.js 16 App Router, React 19, and TypeScript.
- **Backend/API approach**: backend behavior is implemented primarily through Next.js route handlers under `app/api/*`, with shared domain logic in `lib/*`. A separate standalone backend service was not found.
- **Database and authentication services**: Supabase Postgres and Supabase Auth.
- **Storage services**: AWS S3, accessed from server-side helpers for materials and assignment files.
- **Real-time/live-session services**: LiveKit is used for live session tokens and room access; Supabase Realtime is used for live-session state updates.
- **AI-related services**: OpenRouter is used for chat completions and AI generation. The repository also includes AI-backed material extraction and study summary generation, including PDF/image handling.
- **Important libraries**:
  - UI: Radix UI packages, Lucide icons, `sonner`, `react-resizable-panels`
  - Validation/forms: `zod`, `react-hook-form`, `@hookform/resolvers`
  - Routing: Next.js App Router
  - State management: custom React context store in `lib/store.tsx`
  - Charts: `recharts`
  - Theming: `next-themes`
  - IDE: `@monaco-editor/react`
  - PDF and visual extraction support: `pdfjs-dist` imports in code and `@napi-rs/canvas`

## 3. System Architecture

The implemented system is a web-first application in which the browser client renders role-specific pages and communicates with server-side route handlers. Those route handlers coordinate with Supabase for authentication, database access, RPC execution, and some realtime-aware state, while AWS S3, LiveKit, and OpenRouter are used for specialized services.

At a high level:

- The browser loads pages from the Next.js App Router and uses client-side state from `lib/store.tsx`.
- Authentication state is read from Supabase and guarded both in the app shell and in route handlers.
- Most mutations and guarded reads go through `app/api/*` routes rather than direct client-side database writes.
- Route handlers query Supabase tables directly and also call Supabase SQL functions for important workflows such as organization creation, role selection, visibility rules, join links, class permissions, and live-session claiming.
- File uploads are server-mediated: the Next.js API receives the file, validates it, uploads it to S3, and stores metadata in Supabase.
- File downloads are mediated by short-lived signed URLs, and some material content is also streamed through a server route.
- Live classroom participation uses LiveKit access tokens issued by the server and session state stored in Supabase.
- AI routes gather class context from Supabase, then call OpenRouter to generate answers, summaries, or drafts.

Simple textual architecture description:

```text
Browser (Next.js pages, React client components, local UI state)
  -> Next.js API routes (app/api/*)
    -> Supabase Auth + Postgres tables + RPC functions + Realtime
    -> AWS S3 for materials and assignment files
    -> LiveKit for live audio/video session access
    -> OpenRouter for AI responses, summaries, and draft generation
```

No repository-native architecture diagram was found, so this section stays textual.

## 4. Implemented Features by Role

**Organization Administrator**

- Create a new organization with presets, feature overrides, and public-access settings.
- Switch the default active organization and select the active role inside an organization.
- Manage organization users, invites, and additional roles for existing members.
- Create and review public join links and join requests.
- Configure organization-level feature enablement, extension availability, and organization settings.
- Create, edit, archive, and manage classes, including teacher assignment, organization visibility, and results visibility rules.
- Review archived class history and student previous-term data.

**Teacher**

- Access a teacher dashboard with class metrics, grading workload, and archived-term summaries.
- Create classes when organization settings permit it, and manage their own classes when allowed.
- Edit class details and, where permitted, control student results visibility.
- Add materials, upload prompt files, create assignments, review submissions, grade work, and release feedback-related outcomes.
- Create, publish, grade, flag, void, and release exams, including retake handling.
- Start and end live sessions and use the synchronized whiteboard.
- Use AI-backed routes for class help, assignment support, exam drafting, and submission feedback drafting.

**Student**

- Accept invited access or public join access to an organization.
- View active classes available to the selected role and hide/show classes from the dashboard.
- Access enabled class areas such as chat, materials, assignments, exams, live sessions, results, AI, and IDE.
- Submit assignment work through allowed text and/or file submission modes.
- Start exams, save answers, operate in exam lock mode, and view released results.
- Join active live sessions and receive synchronized whiteboard state.
- Use the class AI agent within role-constrained guidance rules.

## 5. Main Functional Modules

- **Authentication and account access**: implemented through Supabase Auth with sign-in, sign-up, password reset, auth callback exchange, password change, and protected app-shell redirects.
- **Organization management**: implemented through organization creation, settings, feature presets, membership loading, invite creation, public join links, join requests, and archived organization/class data views.
- **Role switching and membership**: implemented through `organization_membership_roles`, `selected_role_id`, role menus, `/api/me` updates, and class-access filtering based on the selected role.
- **Class management**: implemented through class creation/editing, teacher assignment, roster operations, organization-visible classes, archived classes, and teacher-permission settings.
- **Materials and file uploads/downloads**: implemented through server-side upload validation, S3 storage, metadata in `class_materials`, signed download URLs, and inline content streaming routes.
- **Chat and announcements**: implemented through `class_messages` with text, announcement, and media kinds; announcement notifications; and announcement-carousel visibility flags.
- **Assignments**: implemented through draft/published assignments, prompt files, text/file submission modes, late-submission control, grading, and notification side effects.
- **Exams and integrity events**: implemented through exams, questions, attempts, answers, passcodes, grading, results release, retakes, integrity event capture, suspicious-status handling, and audit logging.
- **Live sessions and whiteboard**: implemented through LiveKit token issuance, session claiming and heartbeat updates, live-session presence records, and a synchronized whiteboard with strokes, shapes, text, viewport sync, clear, undo, and redo.
- **Results and dashboards**: implemented through role-specific dashboards and class results pages. Results visibility to students is configurable at the class level.
- **AI Agent / AI learning support**: implemented through the class AI agent route, material extraction and study summary generation, assignment AI support routes, exam drafting routes, and role-aware prompt policies.
- **IDE / coding lab**: implemented as a browser-based coding workspace with Monaco, templates, preview, file tree, virtual terminal, and browser-safe runners. Real OS process execution is not implemented.
- **Notifications**: implemented through notification tables, API routes, Supabase RPC helpers, realtime UI updates, read/unread tracking, and delete actions.
- **Feature availability and extensions**: implemented through feature definitions, organization and class feature settings, organization extensions, class extension settings, a feature registry, and a custom extension page that launches configured URLs in a sandboxed iframe.
- **Mobile companion functionality**: mobile code is not implemented in this repository. Only a README reference to a sibling mobile repository and shared API expectations is present.

## 6. Database and Backend Services

The repository shows a Supabase-centered backend with a mixture of direct table access and RPC-based workflow control.

### Main database tables or domains visible in the repository

- Organization and access domain: `organization_memberships`, `organization_membership_roles`, `organization_invites`, `organization_join_links`, `organization_join_requests`, `organization_settings`, `organization_teacher_class_permissions`
- Feature and extension domain: `feature_definitions`, `feature_presets`, `feature_preset_items`, `organization_feature_settings`, `class_feature_settings`, `organization_extensions`, `class_extension_settings`
- Class domain: `classes`, `class_memberships`, `class_visibility_preferences`, archived class support, previous-grade support
- Learning content domain: `class_materials`, `class_messages`, `class_assignments`, `class_assignment_files`, `class_assignment_submissions`
- Assessment domain: `exams`, `exam_questions`, `exam_attempts`, `exam_answers`, `audit_logs`
- Communication and session domain: `notifications`, `class_live_sessions`
- Historical domain: `student_previous_grades`

### Database access handling

- Request-scoped route handlers use `requireRouteUser()` and the Supabase request client built from cookies or bearer tokens.
- Backend workflows also call Supabase RPCs such as `create_organization`, `set_selected_organization_role`, `can_manage_class`, `claim_class_live_session`, `set_class_results_visibility`, `set_class_organization_visibility`, `accept_organization_join_link`, and invite/join management functions.
- A privileged service-role client exists in `lib/supabase/server.ts` and is used selectively for server-only operations such as exam audit logs, result aggregation reads, and some registration lookups.

### Authentication, authorization, and role-based access

- Authentication is handled by Supabase Auth.
- Authorization is layered:
  - app-shell route protection in `app/(app)/layout.tsx`
  - route-level user enforcement in `requireRouteUser()`
  - selected-role resolution through `organization_membership_roles`
  - class-level checks through helper logic and RPCs such as `can_manage_class` and `is_class_member`
  - database-side RLS policies declared in migrations

### File storage and delivery

- File uploads are handled server-side and written to S3 using AWS credentials stored in server environment variables.
- Download access is issued through signed S3 URLs with short expiration windows.
- Material content also has an inline streaming route that fetches the signed URL server-side and returns cached content with `ETag` support.

### Real-time subscriptions and live services

- The client store subscribes to Supabase realtime updates for `class_live_sessions`.
- Live session participation itself is handled through LiveKit rooms and tokens.

## 7. Integration and Security Implementation

### Actual integrations found

- **Supabase**: authentication, database queries, RPCs, some privileged service-role access, and realtime subscriptions.
- **AWS S3**: materials and assignment file storage, with server-generated storage keys and signed download URLs.
- **LiveKit**: room-token generation and live-session connection control.
- **OpenRouter**: AI chat completions for the class agent, summaries, and drafting flows.
- **Gmail API**: organization invite email delivery when Gmail OAuth environment variables are configured.

### Actual security mechanisms found

- **Protected application shell**: unauthenticated users are redirected to `/auth`, and users without an active organization are prevented from opening organization-bound pages.
- **Cookie or bearer-token route authentication**: `requireRouteUser()` supports standard app sessions and bearer-token access, which is relevant to the repository's mobile-companion guidance.
- **Role-based access control**: selected roles are stored and resolved through organization membership role records; APIs frequently require the user to operate under the correct selected role.
- **RLS policies**: migrations explicitly enable row-level security on feature, material, chat, assignment, exam, notification, live-session, join-link, join-request, settings, and previous-grade tables.
- **Server-side validation**: route handlers validate assignment input, file uploads, exam data, and material handling before persistence.
- **Signed file access**: S3 downloads use short-lived signed URLs, and material inline rendering stays behind an authenticated route.
- **Invite security**: invite acceptance is bound to the authenticated email address, not just possession of the token.
- **Public join controls**: public join links support enable/disable state, expiration, max-use counts, default role, and approval-required behavior.
- **Exam integrity controls**: exam lock mode records `fullscreen_exit`, `route_leave_attempt`, `visibility_hidden`, and `window_blur` events; passcodes are hashed and invalid-attempt cooldown logic exists; attempts can be flagged or voided; audit logs are written.
- **Privacy on shared results**: student-facing class summary data suppresses peer email addresses, and the student summary route excludes the requesting student from the shared list it returns.

This repository does **not** show webcam-based proctoring, biometric checks, or direct client-side S3 upload tokens.

## 8. Implementation Challenges and Solutions

- **Multi-organization access**: the codebase must let one user belong to multiple organizations and choose a current workspace. It addresses this through default-organization selection, organization-aware API routes, and role-aware organization payloads loaded from `/api/me`.
- **Multiple roles within the same organization**: the repository supports more than one active role per membership. It addresses this with `organization_membership_roles`, `selected_role_id`, a role-switching UI, and selected-role checks in APIs.
- **Controlled public access**: the project supports public join links without making all content public. It addresses this by separating public organization features, organization-visible classes, join-link approval modes, join requests, and class visibility preferences.
- **Server-owned file handling**: the project needs uploads and downloads without exposing storage credentials to browsers. It addresses this with server-side S3 upload helpers, signed download URLs, and authenticated content proxy routes.
- **Live-session concurrency and stale session recovery**: the project needs one active session per class while tolerating reconnects. It addresses this through `claim_class_live_session`, heartbeat updates, stale-session windows, session end routes, and realtime synchronization of live-session records.
- **Exam integrity and fairness**: the project needs more than a simple form submission for exams. It addresses this with passcode checks, lock mode, automatic event reporting, audit logs, flagged/voided states, retakes, and explicit results release.
- **AI feature control**: the project needs AI support without giving unrestricted answers in assessment contexts. It addresses this through role-aware prompts, class-context loading, and student-specific guidance rules that avoid direct final answers for active assignments or exams.
- **Feature modularity**: organizations and classes need different tool sets. The project addresses this through a feature registry, organization/class feature settings, extension settings, and preset-based organization creation.
- **Web/mobile consistency**: the repository anticipates a separate mobile companion. It addresses this partly by supporting bearer-token route authentication and by documenting that mobile should call server-owned API routes. However, the mobile implementation itself is not present here.

## 9. Testing and Evaluation Evidence

### Implemented evidence found in the repository

- Automated tests exist and are run with `bun test`.
- The tests I found are focused on core domain logic and high-risk UI behavior rather than end-to-end browser automation.
- Implemented test coverage visible in the repository includes:
  - exam service, grading, and integrity logic
  - exam lock behavior and manager result-state logic
  - feature-registry resolution
  - IDE preview and runner logic
  - class selector/access helpers
- Validation and error handling are visible throughout the codebase:
  - route handlers return explicit 4xx/5xx errors
  - upload helpers validate file type and size
  - assignment and exam inputs are validated before persistence
  - client dashboards and pages display failure toasts for load/update errors
- Protected routes are clearly visible in both the app shell and API routes.

I did **not** find a dedicated end-to-end test suite such as Playwright or Cypress in the repository paths reviewed.

### Recommended thesis functional test cases

- Verify sign-up, sign-in, password reset, invite acceptance, and protected-route redirects.
- Verify organization creation with different presets and confirm that enabled/disabled class features match the chosen preset.
- Verify organization admin role switching and confirm that route access changes when the selected role changes.
- Verify public join links in both approval-required and instant-join modes, including expired and max-use links.
- Verify class creation/editing, teacher assignment, class archiving, and organization-visible class behavior.
- Verify material upload, summary generation, signed download access, and inline content rendering.
- Verify chat text, announcement posting restrictions, media sharing, and announcement notifications.
- Verify assignment creation with text-only, file-only, and mixed submission modes, including late-submission blocking and grading.
- Verify exam passcodes, start windows, answer autosave, integrity event capture, grading, result release, retake, flag, and void flows.
- Verify live-session start/join/end behavior for teacher and student roles, including stale-session recovery and whiteboard synchronization.
- Verify results visibility toggling and confirm student behavior when class-wide results are hidden versus visible.
- Verify IDE usage, save/restore behavior, preview generation, and the current limitation that real process execution is not available.

### Recommended thesis non-functional test cases

- **Compatibility**: test major desktop browsers for the class workspace, Monaco IDE, LiveKit session UI, and fullscreen exam behavior.
- **Security**: test unauthorized access to class-bound APIs, expired invite/join tokens, cross-role misuse, and signed-download expiration behavior.
- **Performance**: test large class rosters, high message volume, large material files, exam result aggregation, and whiteboard synchronization under multiple participants.
- **Usability**: test role switching clarity, invite/join flows, assignment submission clarity, exam lock messaging, and dashboard comprehensibility for each role.

## 10. Limitations and Future Work

### Current limitations based on the repository

- The repository contains the web application, but not the mobile companion source code.
- The IDE is browser-based and explicitly does **not** execute real OS processes such as `node`, `npm`, or native compilers; it uses browser-safe runners instead.
- The profile page contains a language selector UI, but it is disabled, so language switching is not currently implemented.
- The current test suite is focused on unit and logic-level coverage; a full end-to-end test suite was not found.
- Exam integrity is event-based. I found browser and navigation event monitoring, but not webcam/audio proctoring or biometric verification.
- Some AI and material routes include compatibility fallbacks for missing summary/cache columns, which suggests the implementation is designed to tolerate schema variance rather than assuming one fixed production state.
- The README explicitly states that some mock data still remains for parts of dashboard history, sample activity, and empty-state support.

### Realistic future work items

- Add end-to-end integration tests for cross-role workflows such as invite acceptance, submission, grading, and exam release.
- Implement a secure backend execution sandbox if the IDE is expected to support real command execution or compiled-language workflows.
- Complete user-facing localization if multilingual operation is a project requirement.
- Expand mobile/web contract testing or API documentation, especially because the mobile companion is maintained in a separate repository.
- Extend exam integrity controls if stronger proctoring requirements arise beyond the current browser-event model.
- Add richer analytics/reporting if thesis evaluation or production reporting needs move beyond current dashboard and class-result summaries.

## 11. Evidence Table

| Claim | Evidence file/path | Notes |
| --- | --- | --- |
| EduVerse is a Next.js web application with role-based educational workflows. | `README.md`<br>`app/(app)/layout.tsx` | README and app shell both reflect a workspace application, not a starter scaffold. |
| The frontend stack uses Next.js, React, TypeScript, and Tailwind. | `package.json` | Dependencies and scripts show the implemented stack. |
| Authentication uses Supabase Auth. | `app/auth/page.tsx`<br>`lib/api/supabase-route.ts` | Sign-in, sign-up, password reset, and route-user enforcement are implemented. |
| The app shell protects authenticated routes. | `app/(app)/layout.tsx` | Redirects unauthenticated users and blocks organization-bound pages without an active organization. |
| The system supports multiple organizations per user. | `README.md`<br>`lib/store.tsx`<br>`app/api/me/route.ts` | Organization payloads and active-organization selection are implemented. |
| One membership can expose multiple active roles, and the active role is selectable. | `lib/api/selected-role.ts`<br>`components/top-bar/role-menu.tsx`<br>`app/api/me/route.ts` | Uses `organization_membership_roles` plus `selected_role_id` and a role menu. |
| Organization creation supports presets, public access, and feature overrides. | `features/organization/organization-create-page.tsx`<br>`supabase/migrations/20260628120000_atomic_org_creation_overrides.sql` | The UI calls `create_organization` with preset and feature override data. |
| Organization admin dashboards include classes, history, users, features, public links, and settings. | `components/dashboards/admin-dashboard.tsx` | Admin dashboard tabs map directly to these modules. |
| Teachers have their own dashboard with class metrics, assignment load, and archived terms. | `components/dashboards/teacher-dashboard.tsx` | Teacher dashboard code loads assignment metrics and archived classes. |
| Students have their own dashboard with assignments, exams, live status, progress, and hidden classes. | `components/dashboards/student-dashboard.tsx` | Student dashboard tracks deadlines, progress, live sessions, and class hiding. |
| Class access depends on selected role, membership, and public organization-visible rules. | `lib/api/class-access.ts` | `org_admin`, teacher/member access, and student access to `organization_visible` classes are implemented. |
| The backend is implemented through Next.js API routes plus Supabase RPCs, not a separate backend service. | `app/api/`<br>`lib/api/supabase-route.ts` | API routes and shared server helpers are the main backend layer found. |
| Materials are stored in AWS S3 with server-side helpers and signed download URLs. | `lib/api/s3-materials.ts`<br>`app/api/classes/[classId]/materials/[materialId]/download-url/route.ts` | Upload helpers, bucket access, and short-lived signed URLs are implemented. |
| Material content can also be streamed inline through an authenticated route. | `app/api/classes/[classId]/materials/[materialId]/content/route.ts` | The route fetches signed S3 content and returns it with cache headers and `ETag`. |
| Material upload can trigger AI extraction and AI study summaries. | `app/api/classes/[classId]/materials/upload/route.ts`<br>`app/api/classes/[classId]/materials/[materialId]/ai/summary/route.ts`<br>`lib/ai/material-extraction.ts` | The code caches `ai_extracted_content` and `ai_summary` when supported. |
| Chat supports text, announcements, and media-backed messages. | `app/api/classes/[classId]/messages/route.ts`<br>`app/api/classes/[classId]/messages/media/route.ts` | Message kinds include `text`, `announcement`, and `media`. |
| Announcements are restricted to class managers and produce notifications. | `app/api/classes/[classId]/messages/route.ts`<br>`lib/api/notifications.ts` | The route blocks non-managers from posting announcements and sends `chat_announcement`. |
| Assignments support draft/published state, due dates, late rules, and text/file submission modes. | `app/api/classes/[classId]/assignments/route.ts` | Validation and persistence for these fields are implemented in the route. |
| Student assignment submission is role-constrained and supports text/file uploads plus resubmission handling. | `app/api/classes/[classId]/assignments/[assignmentId]/submission/route.ts`<br>`lib/api/s3-assignments.ts` | Students must use the student role and can upload submission files to S3. |
| Assignment publication and submission trigger notifications. | `app/api/classes/[classId]/assignments/route.ts`<br>`app/api/classes/[classId]/assignments/[assignmentId]/submission/route.ts`<br>`lib/api/notifications.ts` | `assignment_published` and `assignment_submitted` are implemented. |
| The exam subsystem includes exams, questions, attempts, answers, grading, retakes, release, flagging, and voiding. | `lib/exams/service.ts`<br>`supabase/migrations/20260503190000_create_exam_system.sql` | Core exam logic and schema are implemented. |
| Exam integrity monitors fullscreen exit, blur, visibility loss, and route-leave attempts. | `lib/exams/integrity.ts`<br>`features/exam/use-exam-session.ts`<br>`features/exam/exam-lock.tsx` | Integrity events are explicitly enumerated and reported. |
| Exam audit logs are written through a privileged service client. | `lib/exams/audit.ts`<br>`lib/supabase/server.ts` | Audit writes use the service-role helper. |
| Live sessions use LiveKit tokens and Supabase-backed session records. | `app/api/livekit/token/route.ts`<br>`app/api/classes/[classId]/live-session/route.ts` | LiveKit access and session presence management are both implemented. |
| The client subscribes to live-session updates in realtime. | `lib/store.tsx`<br>`app/api/organizations/[organizationId]/live-sessions/route.ts` | The store opens a Supabase channel for `class_live_sessions`. |
| The live whiteboard is implemented with synchronization, drawing tools, and undo/redo behavior. | `features/session/use-whiteboard.ts`<br>`features/session/live-session-provider.tsx` | Whiteboard code includes state sync, viewport sync, shapes, text, and history actions. |
| Notifications are stored, queried, and updated through dedicated APIs and helpers. | `app/api/notifications/route.ts`<br>`app/api/notifications/[notificationId]/route.ts`<br>`lib/api/notifications.ts` | Notification types, unread counts, read/delete actions, and RPC helpers are implemented. |
| Results visibility is configurable, and student-facing summaries are privacy-filtered. | `app/api/classes/[classId]/results/summary/route.ts`<br>`app/api/classes/[classId]/results/visibility/route.ts`<br>`features/results/class-results-screen.tsx` | Student email suppression and configurable visibility are implemented. |
| Feature availability is controlled at organization/class level and extended through custom extensions. | `lib/features/feature-registry.ts`<br>`app/api/feature-definitions/route.ts`<br>`app/(app)/classes/[classId]/extensions/[extensionId]/page.tsx` | The registry and custom-extension page show real feature modularity. |
| The IDE is implemented as a browser-based coding lab with virtual commands and preview, not real process execution. | `app/(app)/classes/[classId]/ide/page.tsx`<br>`features/ide/terminal.ts`<br>`features/ide/runners.ts` | The terminal explicitly states that real process execution needs a secure backend sandbox. |
| Route authentication supports bearer tokens in addition to cookie sessions. | `lib/api/supabase-route.ts` | This is relevant to the README's mobile-companion guidance. |
| Privileged service-role access is used selectively for server-only reads and writes. | `lib/supabase/server.ts`<br>`app/api/classes/[classId]/results/summary/route.ts`<br>`app/api/organizations/[organizationId]/registrations/route.ts` | Not all database access is performed with the same client. |
| RLS policies are implemented for major domains including features, materials, chat, assignments, exams, notifications, live sessions, join links, join requests, and settings. | `supabase/migrations/20260429120000_feature_enablement_model.sql`<br>`supabase/migrations/20260501143000_create_class_materials.sql`<br>`supabase/migrations/20260502120000_create_class_chat_messages.sql`<br>`supabase/migrations/20260502150000_create_class_assignments.sql`<br>`supabase/migrations/20260503190000_create_exam_system.sql`<br>`supabase/migrations/20260504100000_create_notifications.sql`<br>`supabase/migrations/20260504105000_create_class_live_sessions.sql`<br>`supabase/migrations/20260616120000_create_public_join_links.sql`<br>`supabase/migrations/20260624120000_create_organization_settings.sql` | The migrations explicitly enable row-level security and define policies. |
| Organization invite delivery integrates with Gmail when configured and falls back to shareable links otherwise. | `lib/email/gmail.ts`<br>`app/api/organizations/[organizationId]/invites/route.ts`<br>`app/api/organizations/[organizationId]/registrations/route.ts` | Gmail OAuth is optional; manual invite-link sharing remains supported. |
| Public join links can require approval, expire, and limit usage. | `app/api/join/[token]/route.ts`<br>`supabase/migrations/20260616120000_create_public_join_links.sql` | Join-link metadata and approval flow are implemented. |
| The mobile companion is referenced but not implemented in this repository. | `README.md` | README points to `../Eduverse-mobile-app`; no mobile source tree is present here. |
| Automated tests exist and are focused on core logic and selected UI behavior. | `package.json`<br>`tests/lib/exams/service.test.ts`<br>`tests/lib/exams/integrity.test.ts`<br>`tests/lib/exams/grading.test.ts`<br>`tests/lib/features/feature-registry.test.ts`<br>`tests/features/exam/exam-lock.test.ts`<br>`tests/features/exam/manager-detail-state.test.ts`<br>`tests/features/ide/runners.test.ts`<br>`tests/features/ide/preview.test.ts`<br>`tests/lib/education/selectors.test.ts`<br>`lib/education/classes.test.ts` | The visible test suite is unit/logic oriented. |
| Some mock-data support remains in the codebase. | `README.md`<br>`lib/store.tsx` | README explicitly says some mock data remains; the store still has a fallback mock user. |
| Language switching is not currently implemented for end users. | `features/profile/profile-screen.tsx` | The language toggle exists but is disabled. |
