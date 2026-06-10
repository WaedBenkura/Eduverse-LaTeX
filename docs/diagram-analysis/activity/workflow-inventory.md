# EduVerse Activity Workflow Inventory

## Scope

This inventory is based on the implemented EduVerse codebase only. The analysis was grounded in these source areas:

- `app/`
- `features/`
- `lib/`
- `app/api/`
- `supabase/migrations/`

Actor normalization for documentation is restricted to the three supported roles only:

- `owner`
- `teacher`
- `student`

Some inspected file paths use legacy internal naming, but the workflow descriptions below keep the documentation actor set limited to the three supported roles.

## Included Workflows Summary

| ID | Workflow | Actors | Implementation status |
| --- | --- | --- | --- |
| WF-01 | Authentication and dashboard entry | owner, teacher, student | Implemented |
| WF-02 | Organization creation | owner | Implemented |
| WF-03 | Organization invite acceptance | teacher, student | Implemented |
| WF-04 | Workspace and active-role switching | owner, teacher, student | Implemented |
| WF-05 | Organization member invitation and invite revocation | owner | Implemented |
| WF-06 | Organization feature and extension configuration | owner | Implemented |
| WF-07 | Class lifecycle management | owner | Implemented |
| WF-08 | Class member management | owner, teacher | Implemented |
| WF-09 | Class access and feature gating | owner, teacher, student | Implemented |
| WF-10 | Class chat and announcements | owner, teacher, student | Implemented |
| WF-11 | Class materials management | owner, teacher, student | Implemented |
| WF-12 | Assignment lifecycle management | owner, teacher | Implemented |
| WF-13 | Assignment submission and resubmission | student | Implemented |
| WF-14 | Assignment grading and student notification | owner, teacher | Implemented |
| WF-15 | Exam lifecycle management | owner, teacher | Implemented |
| WF-16 | Exam attempt | student | Implemented |
| WF-17 | Exam grading, result release, integrity handling, and retake | owner, teacher | Implemented |
| WF-18 | Live session lifecycle | owner, teacher, student | Implemented |
| WF-19 | Results review | teacher, student | Implemented |
| WF-20 | Notifications handling | owner, teacher, student | Implemented |

## Workflow Details

### WF-01 Authentication and dashboard entry

Diagram title: Activity diagram for authentication and dashboard entry

Actors: `owner`, `teacher`, `student`

Related files inspected: `app/auth/page.tsx`, `app/(app)/dashboard/page.tsx`, `lib/store.tsx`, `lib/supabase/app-user.ts`

Main activity steps:
1. User opens the authentication page.
2. The page checks for an existing session and redirects to `next` or `/dashboard` when a session already exists.
3. User chooses sign in or sign up.
4. Sign in calls Supabase password authentication.
5. Sign up calls Supabase registration.
6. Application refreshes user, organization, and role context through `useApp()`.
7. Dashboard renders the role-specific dashboard for the resolved current role.

Decision points:
- Does the user already have an active session?
- Is the user signing in or signing up?
- Did sign-up return an immediate session, or does the user need email confirmation?
- Does the user have an organization context available after authentication?

Alternative paths:
- Invalid credentials or invalid registration data keep the user on the authentication page with an error.
- Sign-up may end in an email-confirmation message instead of immediate dashboard entry.
- Existing session bypasses the form entirely.

Assumptions or partially implemented behavior:
- Dashboard routing is fully code-backed, but the documentation should describe role output using `owner`, `teacher`, and `student` only.

### WF-02 Organization creation

Diagram title: Activity diagram for organization creation

Actors: `owner`

Related files inspected: `features/organization/organization-create-page.tsx`, `lib/store.tsx`, `supabase/migrations/20260501142000_use_membership_roles_for_auth.sql`

Main activity steps:
1. User enters organization name, slug, and preset.
2. UI calls the `create_organization` RPC.
3. Database validates authentication, name, preset, and slug rules.
4. Database creates the organization and seeds organization-level feature settings.
5. Database creates the owner membership and sets the default organization.
6. Client refreshes app state and routes back to `/dashboard`.

Decision points:
- Is the user authenticated?
- Is the requested slug valid and available?
- Is the preset value valid?

Alternative paths:
- Validation failure returns an error and stops organization creation.
- Successful creation immediately places the user into the new organization workspace.

Assumptions or partially implemented behavior:
- Preset handling is implemented as setup data, not as a separate post-creation workflow in the inspected UI.

### WF-03 Organization invite acceptance

Diagram title: Activity diagram for organization invite acceptance

Actors: `teacher`, `student`

Related files inspected: `app/invite/[token]/page.tsx`, `app/auth/page.tsx`, `features/admin/users-tab.tsx`, `supabase/migrations/20260419150902_class_management_workflow.sql`

Main activity steps:
1. Invite recipient opens `/invite/[token]`.
2. If the recipient is signed out, the app redirects to `/auth?next=/invite/[token]`.
3. Signed-in recipient calls `accept_organization_invite`.
4. Database validates token status, expiry, and email match.
5. Database activates the organization membership.
6. Database activates any pending class invites for the same email in the same organization.
7. Database sets the default organization if the profile does not already have one.
8. Client refreshes app state and returns the user to the workspace.

Decision points:
- Is the recipient authenticated?
- Is the invite token still valid and unused?
- Does the signed-in email match the invited email?
- Are there linked pending class invites to activate?

Alternative paths:
- Expired, used, or mismatched-email invites fail with an error.
- If no class invites are linked, only the organization membership is activated.

Assumptions or partially implemented behavior:
- The inspected UI exposes invitation paths for `teacher` and `student`; this inventory does not extend the actor list beyond the supported documentation roles.

### WF-04 Workspace and active-role switching

Diagram title: Activity diagram for workspace and active-role switching

Actors: `owner`, `teacher`, `student`

Related files inspected: `components/top-bar/organization-menu.tsx`, `components/top-bar/role-menu.tsx`, `features/profile/profile-screen.tsx`, `lib/store.tsx`, `supabase/migrations/20260501141000_add_selected_organization_role.sql`

Main activity steps:
1. User opens the organization switcher and selects a different organization.
2. Client calls `setDefaultOrganization`.
3. Store refreshes memberships, classes, users, and live session state for the selected organization.
4. User opens the role switcher from the top bar or profile page.
5. Client calls `setActiveOrganizationRole`.
6. Database validates that the selected role is active for the current organization membership.
7. If needed, the app redirects the user away from class-sensitive routes and back to `/dashboard`.

Decision points:
- Does the user belong to more than one organization?
- Is the requested role active for the current organization membership?
- Is the current route tied to class access that may no longer be valid after switching role?

Alternative paths:
- Invalid role selection is rejected by the RPC.
- Switching organization or role can leave the user in the same route when access remains valid.

Assumptions or partially implemented behavior:
- This flow is important because student-only actions such as assignment submission and exam attempts depend on the currently selected organization role.

### WF-05 Organization member invitation and invite revocation

Diagram title: Activity diagram for organization member management

Actors: `owner`

Related files inspected: `features/admin/users-tab.tsx`, `supabase/migrations/20260501142000_use_membership_roles_for_auth.sql`, `supabase/migrations/20260419142150_revoke_organization_invites.sql`

Main activity steps:
1. Owner opens the member-management screen.
2. Owner enters an email address and chooses `teacher` or `student`.
3. UI calls `invite_organization_member`.
4. Database checks whether a profile already exists for that email.
5. Existing-profile path activates membership immediately.
6. Missing-profile path creates or refreshes a pending organization invite token.
7. UI refreshes the user list and pending invites list.
8. Owner can revoke a pending invite through `revoke_organization_invite`.

Decision points:
- Does the target email already belong to an existing profile?
- Is there already a pending invite for that email in the organization?
- Is the invite still pending when revoke is requested?

Alternative paths:
- Existing users receive active membership immediately.
- New users stay in pending-invite state until they accept the invite link.
- Re-inviting updates the pending invite token and expiry.

Assumptions or partially implemented behavior:
- The documented actor is `owner`, even though some inspected files use broader internal naming for the same management screen.

### WF-06 Organization feature and extension configuration

Diagram title: Activity diagram for organization feature and extension configuration

Actors: `owner`

Related files inspected: `features/admin/features-tab.tsx`, `lib/supabase/features.ts`, `features/admin/classes-tab.tsx`

Main activity steps:
1. Owner opens the features screen.
2. UI loads feature definitions and current organization feature settings.
3. Owner toggles organization-level features on or off.
4. UI upserts the chosen state to `organization_feature_settings`.
5. Owner optionally adds a custom extension with name, URL, and description.
6. UI inserts a new row into `organization_extensions`.
7. Owner can enable or disable a custom extension later.

Decision points:
- Is the selected feature allowed by its parent feature state?
- Is the owner toggling a built-in feature or a custom extension?
- Are the extension fields valid enough to save?

Alternative paths:
- Disabled parent features lock child feature toggles.
- Organization extensions can exist but remain disabled.

Assumptions or partially implemented behavior:
- The implementation clearly backs feature toggles and extension records. Launching the extension itself belongs to class-side navigation rather than this owner-side configuration workflow.

### WF-07 Class lifecycle management

Diagram title: Activity diagram for class lifecycle management

Actors: `owner`

Related files inspected: `features/admin/classes-tab.tsx`, `lib/education/classes.ts`, `supabase/migrations/20260419150902_class_management_workflow.sql`, `supabase/migrations/20260501130000_fix_create_class_ambiguous_class_id.sql`, `supabase/migrations/20260504104000_preserve_class_memberships_on_update.sql`

Main activity steps:
1. Owner opens the class-management screen.
2. Owner creates a class or opens an existing class for editing.
3. UI submits class metadata and teacher email through `create_class` or `update_class`.
4. Database validates the request and ensures the teacher has the needed organization membership.
5. Database creates or updates the class record and teacher linkage.
6. UI upserts class feature settings and class extension settings.
7. Owner can delete a class through `delete_class`.

Decision points:
- Is the action create, update, or delete?
- Does the teacher email belong to an existing profile?
- Is the teacher changing during update?

Alternative paths:
- Create fails when the provided teacher profile does not exist.
- Update preserves existing memberships when the teacher does not change.
- Delete removes the class from the organization workflow.

Assumptions or partially implemented behavior:
- Class feature and extension settings are saved as part of class management in the inspected UI, so they belong in the same diagram unless the report prefers a separate configuration diagram.

### WF-08 Class member management

Diagram title: Activity diagram for class member management

Actors: `owner`, `teacher`

Related files inspected: `features/classes/class-home-screen.tsx`, `lib/education/classes.ts`, `supabase/migrations/20260419150902_class_management_workflow.sql`

Main activity steps:
1. Manager opens the class home screen.
2. Manager reviews the current teacher and student roster.
3. Manager enters an email and chooses a class role.
4. UI calls `invite_class_member`.
5. Database checks access and validates the requested class role.
6. Existing-profile path creates or updates membership immediately.
7. Missing-profile path creates or refreshes the linked organization invite and class invite.
8. Manager can remove a student through `remove_class_student`.

Decision points:
- Is the current user allowed to manage the class?
- Is the invited email already tied to a profile?
- Is the requested class role `teacher` or `student`?
- Is the removal target a student membership?

Alternative paths:
- Existing users receive active class membership immediately.
- New users stay in invite state until organization invite acceptance.
- Teacher assignment is owner-facing; teacher-led class management focuses on student roster changes.

Assumptions or partially implemented behavior:
- The implemented removal workflow deletes student memberships only. No separate teacher-removal workflow was found in the inspected class-home path.

### WF-09 Class access and feature gating

Diagram title: Activity diagram for class access and feature gating

Actors: `owner`, `teacher`, `student`

Related files inspected: `app/(app)/classes/[classId]/home/page.tsx`, `features/classes/class-home-screen.tsx`, `features/classes/use-class-route.tsx`, `lib/features/feature-registry.ts`, `lib/education/classes.ts`

Main activity steps:
1. User opens a class route.
2. Route helper loads class context for the current organization and selected role.
3. Helper verifies that the user can access the class.
4. For feature routes, helper checks whether the target feature is enabled.
5. Allowed routes render the requested class screen.
6. Disallowed routes render an error state or a feature-disabled fallback.

Decision points:
- Is the class in the selected organization?
- Can the current role access the class?
- Is the requested feature enabled for the class?

Alternative paths:
- Invalid or inaccessible class routes stop at an error state.
- Disabled features stop at a fallback message instead of loading the tool screen.
- Management actions appear only for users who can manage the class.

Assumptions or partially implemented behavior:
- Class-home progress counters are placeholder values and should not be expanded into a separate analytics workflow diagram.

### WF-10 Class chat and announcements

Diagram title: Activity diagram for class chat and announcements

Actors: `owner`, `teacher`, `student`

Related files inspected: `features/chat/chat-screen.tsx`, `features/chat/use-class-messages.ts`, `app/api/classes/[classId]/messages/route.ts`, `app/api/classes/[classId]/messages/media/route.ts`, `app/api/classes/[classId]/messages/[messageId]/route.ts`, `supabase/migrations/20260502120000_create_class_chat_messages.sql`

Main activity steps:
1. Class member opens chat.
2. Client loads class messages and announcement carousel data.
3. Member sends a text message, or uploads media through the media route.
4. Manager can post a message as an announcement.
5. API validates class access and announcement permissions.
6. Message is inserted into `class_messages`.
7. Announcement posts create a class notification.
8. Manager can hide an announcement from the carousel later.

Decision points:
- Is the sender a class member?
- Is the post a normal message or an announcement?
- Is the sender allowed to create announcements?
- Is the upload file valid?

Alternative paths:
- Students can participate in chat but cannot create announcements.
- Media upload creates a stored class material row and a linked chat message.
- Hidden announcements remain in message history while leaving the announcement carousel.

Assumptions or partially implemented behavior:
- Media authorization is enforced by both route logic and database policies; the user-facing workflow is still fully backed by code.

### WF-11 Class materials management

Diagram title: Activity diagram for class materials management

Actors: `owner`, `teacher`, `student`

Related files inspected: `app/(app)/classes/[classId]/materials/page.tsx`, `features/materials/use-class-materials.ts`, `app/api/classes/[classId]/materials/upload/route.ts`, `app/api/classes/[classId]/materials/[materialId]/route.ts`, `app/api/classes/[classId]/materials/[materialId]/download-url/route.ts`, `app/api/classes/[classId]/materials/[materialId]/content/route.ts`, `supabase/migrations/20260501143000_create_class_materials.sql`

Main activity steps:
1. User opens the materials page.
2. Client loads available class materials.
3. Manager uploads a file with metadata through the upload route.
4. API stores the object, inserts the material row, and creates a class notification.
5. Members search, filter, open, or download materials.
6. Manager can delete a material.

Decision points:
- Is the current user a manager or a read-only class member?
- Is the uploaded file valid?
- Should the material be streamed inline or downloaded through a signed URL?
- Is the material already deleted?

Alternative paths:
- Student path is read-only.
- Image or inline-safe content can be streamed directly.
- Delete performs soft deletion before object cleanup.

Assumptions or partially implemented behavior:
- Some route authorization depends on Supabase row-level security rather than explicit branch logic in every handler.

### WF-12 Assignment lifecycle management

Diagram title: Activity diagram for assignment lifecycle management

Actors: `owner`, `teacher`

Related files inspected: `app/(app)/classes/[classId]/assignments/page.tsx`, `features/assignments/use-class-assignments.ts`, `app/api/classes/[classId]/assignments/route.ts`, `app/api/classes/[classId]/assignments/[assignmentId]/route.ts`, `app/api/classes/[classId]/assignments/[assignmentId]/files/route.ts`, `supabase/migrations/20260502150000_create_class_assignments.sql`, `supabase/migrations/20260502152000_soft_delete_class_assignment_rpc.sql`

Main activity steps:
1. Manager opens the assignments screen.
2. Manager creates a new assignment or edits an existing one.
3. Manager enters instructions, due date, max score, late policy, and allowed submission modes.
4. Manager optionally uploads a prompt file.
5. UI saves the assignment as draft or published.
6. API validates fields and stores the assignment.
7. Publishing creates assignment notifications for students.
8. Manager can later edit, publish, or soft-delete the assignment.

Decision points:
- Is the user allowed to manage the class?
- Is at least one submission mode enabled?
- Is the max score valid?
- Is the assignment saved as draft or published?
- Is the operation create, update, or delete?

Alternative paths:
- Publishing on create or publishing later on update both notify students.
- Draft assignments remain hidden from student submission workflows.
- Delete uses a soft-delete RPC rather than a hard delete.

Assumptions or partially implemented behavior:
- The diagram should treat publishing as the point where the assignment becomes active for student workflows.

### WF-13 Assignment submission and resubmission

Diagram title: Activity diagram for assignment submission

Actors: `student`

Related files inspected: `app/(app)/classes/[classId]/assignments/page.tsx`, `features/assignments/use-class-assignments.ts`, `app/api/classes/[classId]/assignments/[assignmentId]/submission/route.ts`, `supabase/migrations/20260502150000_create_class_assignments.sql`

Main activity steps:
1. Student opens the assignments screen while using the selected student role.
2. Student chooses a published assignment.
3. Student enters text and or uploads a file according to the allowed submission modes.
4. API validates role, class membership, publication state, timing, and submission mode.
5. System upserts the submission.
6. If this is a resubmission, the old file can be replaced and the previous grade is cleared.
7. Teacher receives a submission notification.

Decision points:
- Is the current selected organization role `student`?
- Is the assignment published?
- Is submission still on time, or are late submissions allowed?
- Does the submission match the allowed mode configuration?
- Is there already a prior submission?

Alternative paths:
- Late submission is blocked when the assignment disallows it.
- Invalid submission mode is rejected.
- Resubmission updates the same submission record instead of creating a duplicate.

Assumptions or partially implemented behavior:
- This workflow is explicitly student-only in the implementation, even if the same account may also hold another role in the same organization.

### WF-14 Assignment grading and student notification

Diagram title: Activity diagram for assignment grading

Actors: `owner`, `teacher`

Related files inspected: `app/(app)/classes/[classId]/assignments/page.tsx`, `features/assignments/use-class-assignments.ts`, `app/api/classes/[classId]/assignments/[assignmentId]/submissions/[submissionId]/grade/route.ts`, `supabase/migrations/20260504101000_scope_notifications_to_recipient_role.sql`

Main activity steps:
1. Manager opens assignment submissions for the class roster.
2. Manager chooses a student submission.
3. Manager enters score and feedback.
4. API validates class-management access and score bounds.
5. System saves the grade.
6. Notification is created for the student.
7. Student later sees the graded result in the assignment area and results views.

Decision points:
- Is the submission present?
- Is the user allowed to grade?
- Is the score within the assignment maximum?

Alternative paths:
- Pending submissions stay ungraded.
- Regrading overwrites the previous grade and feedback.

Assumptions or partially implemented behavior:
- No separate grade-publication step was found; saved grading is the student-visible outcome.

### WF-15 Exam lifecycle management

Diagram title: Activity diagram for exam management

Actors: `owner`, `teacher`

Related files inspected: `app/(app)/classes/[classId]/exam/page.tsx`, `features/exam/manager-exam-screen.tsx`, `features/exam/use-class-exam.ts`, `lib/exams/service.ts`, `app/api/classes/[classId]/exams/route.ts`, `app/api/classes/[classId]/exams/[examId]/route.ts`, `supabase/migrations/20260503190000_create_exam_system.sql`

Main activity steps:
1. Manager opens the exam screen.
2. Manager creates a new exam or edits the current exam definition.
3. Manager configures exam metadata, questions, schedule, passcode, attempts, and integrity rules.
4. UI saves the exam draft through the exam routes.
5. Manager publishes the exam when ready.
6. Manager can reopen the screen later to edit or delete the exam.

Decision points:
- Is the exam feature enabled for the class?
- Is the user allowed to manage the class?
- Is the action create, update, publish, or delete?
- Does the exam configuration validate successfully?

Alternative paths:
- Draft exams remain unavailable to students.
- Published exams move into scheduled or active student states based on timing.
- Delete removes the exam from active use.

Assumptions or partially implemented behavior:
- The backend supports full exam entities and history. The inspected manager UI presents a single active management flow for the class screen.

### WF-16 Exam attempt

Diagram title: Activity diagram for exam attempt

Actors: `student`

Related files inspected: `features/exam/exam-screen.tsx`, `features/exam/use-class-exam.ts`, `lib/exams/service.ts`, `app/api/classes/[classId]/exams/[examId]/start/route.ts`, `app/api/classes/[classId]/exams/[examId]/attempts/[attemptId]/answers/route.ts`, `app/api/classes/[classId]/exams/[examId]/attempts/[attemptId]/submit/route.ts`, `supabase/migrations/20260503190000_create_exam_system.sql`

Main activity steps:
1. Student opens the exam page while using the selected student role.
2. Service resolves whether the class has no exam, a scheduled exam, or an active exam.
3. Student enters the passcode when required and starts the attempt.
4. System reuses an eligible in-progress attempt or creates a new attempt.
5. If exam mode is enabled, the student enters fullscreen mode.
6. Student answers questions and saves answers while navigating the exam.
7. System autosaves answers and monitors expiry.
8. Student submits the attempt, or the system auto-submits when time expires.

Decision points:
- Is the selected role `student` and does the user have student membership in the class?
- Is the exam published and currently active?
- Is the passcode correct, or has cooldown been triggered after repeated failures?
- Is there a reusable in-progress attempt already?
- Has the attempt expired?
- Is a retake available?

Alternative paths:
- Existing in-progress attempts resume instead of starting from zero.
- Expired attempts are auto-submitted.
- Fullscreen requirement can pause progress until fullscreen is restored.
- No active exam leaves the student in a waiting or empty state.

Assumptions or partially implemented behavior:
- Integrity tracking is implemented and attached to the attempt workflow. It should be shown conservatively as monitoring behavior, not as a separate student-owned business process unless the report needs that extra detail.

### WF-17 Exam grading, result release, integrity handling, and retake

Diagram title: Activity diagram for exam grading and integrity handling

Actors: `owner`, `teacher`

Related files inspected: `features/exam/manager-exam-screen.tsx`, `features/exam/use-class-exam.ts`, `lib/exams/service.ts`, `app/api/classes/[classId]/exams/[examId]/attempts/[attemptId]/grade/route.ts`, `app/api/classes/[classId]/exams/[examId]/attempts/[attemptId]/release/route.ts`, `app/api/classes/[classId]/exams/[examId]/attempts/[attemptId]/integrity/route.ts`, `app/api/classes/[classId]/exams/[examId]/retakes/route.ts`

Main activity steps:
1. Manager opens the exam detail or monitoring view.
2. Manager reviews attempt status and answers.
3. Manager scores any answers that need manual review.
4. Manager finalizes grading.
5. System computes totals and releases results for the attempt.
6. Manager can flag, clear, or void an attempt for integrity reasons.
7. Manager can grant a retake when the attempt state and history allow it.

Decision points:
- Is the attempt still in progress?
- Are all manual-review answers graded?
- Has the attempt already been released?
- Is an integrity action needed?
- Is a retake still allowed, and is there already an unused retake?

Alternative paths:
- Fully auto-gradable attempts can reach graded state at submission time.
- Manually reviewed attempts stay in submitted state until grading is completed.
- Voided attempts stop following the normal successful-result path.
- Retake grant creates a new future attempt opportunity rather than editing the completed attempt.

Assumptions or partially implemented behavior:
- A dedicated release route exists, but the current grading implementation releases results immediately when grading is finalized. Diagrams should reflect the implemented one-step grading-plus-release outcome.

### WF-18 Live session lifecycle

Diagram title: Activity diagram for live session lifecycle

Actors: `owner`, `teacher`, `student`

Related files inspected: `app/(app)/classes/[classId]/session/page.tsx`, `features/session/session-screen.tsx`, `features/session/live-session-provider.tsx`, `features/session/use-live-session.ts`, `app/api/livekit/token/route.ts`, `app/api/classes/[classId]/live-session/route.ts`, `supabase/migrations/20260504105000_create_class_live_sessions.sql`, `supabase/migrations/20260505124000_fix_claim_live_session_return.sql`

Main activity steps:
1. Manager opens the session screen and starts or reconnects a class live session.
2. Backend claims or refreshes the live session row and issues a LiveKit token.
3. Manager marks the session as live.
4. Students open the session screen and join only when an active live session exists.
5. Participants use media, chat, and whiteboard features during the session.
6. Teacher heartbeat keeps the live session fresh.
7. Manager ends the session, or the owned session can be ended on page exit.

Decision points:
- Is the current user a class manager or a student participant?
- Is there already a pending or live session row to reuse?
- Is the session currently active for student join?
- Has the live session timed out or been ended?

Alternative paths:
- Teacher can start a session even before a live row exists.
- Student join is blocked when the session is not live.
- Session end can happen explicitly from the UI or automatically through the page-exit beacon path.
- Students are disconnected when the live session disappears and the recheck confirms it has ended.

Assumptions or partially implemented behavior:
- Students have view-only whiteboard permissions in the inspected implementation.

### WF-19 Results review

Diagram title: Activity diagram for results review

Actors: `teacher`, `student`

Related files inspected: `features/results/class-results-screen.tsx`, `features/classes/use-class-route.tsx`, `lib/features/feature-registry.ts`, `lib/exams/service.ts`, `features/assignments/use-class-assignments.ts`

Main activity steps:
1. User opens the Results route.
2. Route helper verifies class access and feature availability.
3. Teacher sees aggregated assignment and exam performance views for the class.
4. Student sees graded assignments and released exam results only.
5. User opens result details from the page as needed.

Decision points:
- Is the results feature enabled for the class?
- Is the viewer a teacher or a student?
- Has an exam result been released yet?

Alternative paths:
- Disabled feature routes stop at the feature-disabled fallback.
- Students do not see unreleased exam attempts.
- Teacher view summarizes class performance rather than exposing teacher management controls directly from this screen.

Assumptions or partially implemented behavior:
- The user-facing route label is `Results`, while the internal feature key uses a different name. Diagrams should use the user-facing label.

### WF-20 Notifications handling

Diagram title: Activity diagram for notifications handling

Actors: `owner`, `teacher`, `student`

Related files inspected: `components/top-bar/notifications-menu.tsx`, `app/api/notifications/route.ts`, `app/api/notifications/[notificationId]/route.ts`, `supabase/migrations/20260504100000_create_notifications.sql`, `supabase/migrations/20260504101000_scope_notifications_to_recipient_role.sql`

Main activity steps:
1. User opens the notifications menu.
2. Client loads notifications and unread count for the current organization and selected role.
3. Realtime changes trigger reloads.
4. User opens a notification link, marks one notification read, marks all read, or deletes a notification.
5. The notifications list refreshes to reflect the new state.

Decision points:
- Does the user have unread notifications?
- Is the action open, mark one read, mark all read, or delete?
- Does the notification include a target `href`?

Alternative paths:
- Empty state is shown when no notifications exist.
- Opening a linked notification routes the user to the related class resource.

Assumptions or partially implemented behavior:
- Notification generation is distributed across other workflows such as assignments, chat announcements, materials, and sessions rather than coming from a standalone authoring screen.

## Analyzed But Excluded From Diagram Generation

These items were inspected or encountered during analysis, but they should not be treated as implemented activity-diagram workflows for the report.

### Ex-01 Pending access requests

Reason for exclusion: `features/admin/pending-requests-tab.tsx` is backed by mock data rather than a real backend approval flow.

### Ex-02 Class history

Reason for exclusion: `features/admin/class-history-tab.tsx` is backed by mock data rather than implemented historical workflow logic.

### Ex-03 Activity feed

Reason for exclusion: `features/admin/activity-tab.tsx` is backed by mock data rather than a live activity pipeline.

### Ex-04 Password change

Reason for exclusion: `app/(app)/profile/password/page.tsx` is a placeholder page with no implemented password-change flow.

### Ex-05 IDE coding tool

Reason for exclusion: `app/(app)/classes/[classId]/ide/page.tsx` presents a simulated editor/output experience and does not back a real persisted code-execution workflow.

### Ex-06 Dashboard historical panels

Reason for exclusion: portions of the teacher and student dashboard history displays use mock data, so they should not be promoted into standalone workflow diagrams.

### Ex-07 Class-home progress analytics

Reason for exclusion: the class-home progress cards are placeholder values and do not represent a real calculated workflow.
