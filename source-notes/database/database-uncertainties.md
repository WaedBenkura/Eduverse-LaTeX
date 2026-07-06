# Database Reconstruction Notes And Relationship Summary

## 1. Core tables whose original `CREATE TABLE` DDL is not present in the available migration history

The current repository does not expose the original base-table DDL for these tables, so their current columns were reconstructed from later migrations, RPCs, and active query usage:

- `public.organizations`
- `public.profiles`
- `public.organization_memberships`
- `public.organization_invites`
- `public.classes`
- `public.class_memberships`
- `public.audit_logs`

Because of that gap, the following details are summarized from later migrations, RPCs, and active query usage rather than from a single original `CREATE TABLE` statement:

- The exact original column list for each base table.
- The exact original PK/unique/foreign-key declarations for some base-table columns.
- The exact RLS policies on those base tables, unless later migrations explicitly replaced them.

## 2. Relationships that are visible in code or later SQL, but not directly verifiable as enforced FKs from the available base-table DDL

- `profiles.id` to `auth.users.id`
  - Strong logical 1:1 relationship.
  - Current implementation pattern: auth flows read `profiles` with `id = auth.uid()`.
- `profiles.default_organization_id` to `organizations.id`
  - Logical relationship from create/join/invite acceptance flows.
- `organization_memberships.organization_id` to `organizations.id`
  - Logical relationship in all current membership RPCs and queries.
- `organization_memberships.user_id` to the current user profile/auth identity
  - Logical relationship from auth-context loading and membership management flows.
- `organization_invites.organization_id` to `organizations.id`
  - Logical relationship in invite management RPCs and routes.
- `organization_invites.invited_by_user_id` to `auth.users.id`
  - Logical relationship from current invite flows; direct FK not visible in base DDL.
- `classes.organization_id` to `organizations.id`
  - Logical relationship from every class RPC and from all downstream FK tables.
- `classes.teacher_user_id` to `profiles.id` / current user identity
  - Logical relationship in the visible repo slice; direct FK not present in visible base DDL.
- `class_memberships.organization_id` to `organizations.id`
  - Logical relationship from class roster RPCs and queries.
- `class_memberships.class_id` to `classes.id`
  - Logical relationship from roster management and all class-member checks.
- `class_memberships.user_id` to the current user profile/auth identity
  - Logical relationship from roster queries and membership checks.
- `audit_logs.organization_id` to `organizations.id`
  - Logical relationship from all audit insertions.
- `audit_logs.actor_user_id` to `auth.users.id`
  - Logical relationship from all audit insertions.
- `audit_logs.entity_id` to many different domain tables
  - Polymorphic logical relationship only; not FK-enforced.

## 3. Features implemented without a dedicated table

- Announcements
  - Implemented as `public.class_messages.kind = 'announcement'`.
  - No separate announcements table.
- Chat media
  - Implemented through `public.class_messages` plus `public.class_materials`.
  - No separate message-media table.
- Assignment grades / overall results
  - Stored directly on `public.class_assignment_submissions`.
  - No separate assignment-results table.
- Exam results
  - Stored on `public.exam_attempts` and `public.exam_answers`.
  - No separate exam-results table.
- Exam integrity event stream
  - Stored in `public.audit_logs` with `entity_type = 'exam_attempt'` and `action = 'exam.attempt_event'`.
  - No dedicated integrity-events table.
- Exam retake grants/consumption history
  - Stored in `public.audit_logs`.
  - No dedicated retakes table.
- AI conversation/session history
  - No dedicated AI chat table.
  - Current persistence is limited to `class_materials.ai_summary*` and `class_materials.ai_extracted_content*`.
- IDE workspace/project files
  - No database table.
  - The built-in IDE is enabled by feature flags (`feature_definitions`, `organization_feature_settings`, `class_feature_settings`), while workspace state is client-side.
- Live-session whiteboard state / participant timeline
  - No dedicated database table.
  - The database only stores session header/state in `public.class_live_sessions`.

## 4. Current schema mismatches versus older schema snapshots / older ERD assumptions

These are the important mismatches the new documentation intentionally removes or updates:

- `public.student_previous_grades` is not part of the current schema.
  - It was created in `20260620120000_create_student_previous_grades.sql`.
  - It was dropped in `20260620121000_drop_student_previous_grades.sql`.
  - Current past-term import uses archived classes, imported assignment rows, submission rows, and `class_invites.previous_grade_payload`.
- `public.classes.subject` no longer exists in the current schema.
  - Removed by `20260609130000_remove_class_subject.sql`.
- `public.classes.schedule_text` no longer exists in the current schema.
  - Removed by `20260609120000_remove_class_schedule_text.sql`.
- `public.organization_settings` and `public.organization_teacher_class_permissions` are real current tables.
  - Added in `20260624120000_create_organization_settings.sql`.
- `public.classes.stage` is a real current field and is now required.
  - Added in `20260626130000_add_class_stage.sql`.
  - Required/non-blank in `20260627123000_require_class_term_stage.sql`.
- `public.classes` now has explicit end/archive lifecycle fields.
  - `ended_at`
  - `ended_by_user_id`
  - `archived_edited_at`
  - `archived_edited_by_user_id`
- `public.classes` now has results-visibility controls.
  - `results_visible_to_students`
  - `teacher_can_toggle_results_visibility`
- `public.organization_join_links` now supports multiple links per organization and stores `purpose`.
  - Changed by `20260616121000_support_multiple_public_join_links.sql`.
- `public.class_live_sessions.status` now includes `pending`, and sessions carry `live_session_id`.
  - Added/hardened in `20260505120000_add_live_session_generation.sql`, `20260505122000_harden_live_session_claim.sql`, and `20260505124000_fix_claim_live_session_return.sql`.
- `public.notifications` now includes `recipient_role` and exam notification types.
- Organization owner terminology was migrated to `org_admin` in active application data and policy logic.

## 5. Prior ERD artifacts available for direct comparison

- No current ERD source set was present under `docs/` in the local worktree before regeneration.
- `git log -- docs/...` did not return an earlier tracked ERD source set in the local repository history used for this note.
- Accordingly, the mismatch notes above are based on the current schema state rather than a line-by-line diff against an older checked-in ERD document.







