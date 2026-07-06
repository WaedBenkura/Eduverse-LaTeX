# Eduverse Database Analysis

## Method And Source Of Truth

This report was regenerated from the current checked-out codebase on branch `main`, using the latest available project sources in this order:

1. `supabase/migrations/*.sql`
2. Current SQL RPC definitions and later `ALTER TABLE` migrations
3. TypeScript/Supabase query usage in `app/`, `lib/`, and `features/`
4. RLS policies embedded in migrations
5. Storage-related backend code

Important caveat:

- The repository does **not** include the original `CREATE TABLE` DDL for several core tables: `organizations`, `profiles`, `organization_memberships`, `organization_invites`, `classes`, `class_memberships`, and `audit_logs`.
- For those tables, the columns below are the columns that are **directly confirmed** by current migrations, RPCs, and active query usage.
- When a relationship is enforced by a visible foreign key in the checked-in SQL, it is marked **FK relationship**.
- When a relationship is only implied by later code/RPC usage because the original base DDL is missing, it is marked **logical relationship**.

Current schema removals relevant to older ERD assumptions:

- `public.student_previous_grades` is **not** part of the current schema; it was created and later dropped.
- `public.classes.subject` has been removed.
- `public.classes.schedule_text` has been removed.

External dependency:

- Multiple tables reference Supabase `auth.users(id)`. That is a real external system table, not an Eduverse-owned public-schema table.

## Core Multi-Organization And Membership Model

### `public.organizations`

Purpose:
- Top-level tenant/organization record.

Key columns:
- `id`
- `slug`
- `name`

Primary key:
- `id` (referenced by many visible downstream FKs; original base `CREATE TABLE` is not present in the repo)

Foreign keys:
- No outgoing FK is visible in the checked-in base DDL slice.

Main relationships:
- `organizations.id -> organization_feature_settings.organization_id` (**FK relationship**)
- `organizations.id -> organization_extensions.organization_id` (**FK relationship**)
- `organizations.id -> organization_settings.organization_id` (**FK relationship**)
- `organizations.id -> organization_join_links.organization_id` (**FK relationship**)
- `organizations.id -> organization_join_requests.organization_id` (**FK relationship**)
- `organizations.id -> class_feature_settings.organization_id` (**FK relationship**)
- `organizations.id -> class_extension_settings.organization_id` (**FK relationship**)
- `organizations.id -> class_invites.organization_id` (**FK relationship**)
- `organizations.id -> class_visibility_preferences.organization_id` (**FK relationship**)
- `organizations.id -> class_materials.organization_id` (**FK relationship**)
- `organizations.id -> class_messages.organization_id` (**FK relationship**)
- `organizations.id -> class_assignments.organization_id` (**FK relationship**)
- `organizations.id -> class_assignment_files.organization_id` (**FK relationship**)
- `organizations.id -> class_assignment_submissions.organization_id` (**FK relationship**)
- `organizations.id -> class_live_sessions.organization_id` (**FK relationship**)
- `organizations.id -> exams.organization_id` (**FK relationship**)
- `organizations.id -> exam_questions.organization_id` (**FK relationship**)
- `organizations.id -> exam_attempts.organization_id` (**FK relationship**)
- `organizations.id -> exam_answers.organization_id` (**FK relationship**)
- `organizations.id -> notifications.organization_id` (**FK relationship**)
- `organizations.id -> organization_memberships.organization_id` (**logical relationship**)
- `organizations.id -> organization_invites.organization_id` (**logical relationship**)
- `organizations.id -> classes.organization_id` (**logical relationship**)
- `organizations.id -> audit_logs.organization_id` (**logical relationship**)

System feature usage:
- Organization switching, public join access, feature presets, settings, membership, class ownership, notifications, archived history.

RLS/access:
- Base-table RLS is not restated in the current migration set.

Notes:
- Current create-organization RPCs insert `slug` and `name`, and later seed feature/settings state immediately.

### `public.profiles`

Purpose:
- Application profile record for authenticated users.

Key columns:
- `id`
- `email`
- `display_name`
- `default_organization_id`
- `updated_at`

Primary key:
- `id` (used everywhere as the canonical profile/user key; original base DDL not present in repo)

Foreign keys:
- `default_organization_id -> organizations.id` is only visible through current updates/query usage, not through visible base DDL.

Main relationships:
- `profiles.id -> class_materials.uploaded_by_user_id` (**FK relationship**)
- `profiles.id -> class_messages.sender_user_id` (**FK relationship**)
- `profiles.id -> class_assignments.created_by_user_id` (**FK relationship**)
- `profiles.id -> class_assignment_files.uploaded_by_user_id` (**FK relationship**)
- `profiles.id -> class_assignment_submissions.student_user_id` (**FK relationship**)
- `profiles.id -> class_assignment_submissions.graded_by_user_id` (**FK relationship**)
- `profiles.id -> class_live_sessions.started_by_user_id` (**FK relationship**)
- `profiles.id -> notifications.recipient_user_id` (**FK relationship**)
- `profiles.id -> notifications.actor_user_id` (**FK relationship**)
- `profiles.id -> organization_teacher_class_permissions.teacher_user_id` (**FK relationship**)
- `profiles.id <-> auth.users.id` (**logical relationship**, strongly implied by auth flows)
- `profiles.default_organization_id -> organizations.id` (**logical relationship**)
- `profiles.id <- classes.teacher_user_id` (**logical relationship**)
- `profiles.id <- class_memberships.user_id` (**logical relationship**)
- `profiles.id <- organization_memberships.user_id` (**logical relationship**)

System feature usage:
- Auth context, organization switching, class hydration, roster displays, materials, assignments, notifications, teacher permission overrides.

RLS/access:
- Base-table RLS is not restated in the current migration set.

Notes:
- The app always loads a profile using `id = auth.uid()`, so profile identity is tightly coupled to Supabase auth identity even though the base FK/trigger is not visible here.

### `public.organization_memberships`

Purpose:
- Core organization-membership row for a user within one organization.
- Also acts as the compatibility record for the newer multi-role model.

Key columns:
- `id`
- `organization_id`
- `user_id`
- `role`
- `status`
- `selected_role_id`
- `created_at`
- `updated_at`

Primary key:
- `id` (used throughout the current app and referenced by `organization_membership_roles`)

Foreign keys:
- `selected_role_id -> organization_membership_roles.id` (**FK relationship**)
- Original FK definitions for `organization_id`/`user_id` are not visible in the current repo slice.

Enum/status fields:
- `role` uses `public.app_role`
- `status` uses `public.membership_status`

Main relationships:
- `organization_memberships.id -> organization_membership_roles.organization_membership_id` (**FK relationship**)
- `organization_memberships.organization_id -> organizations.id` (**logical relationship**)
- `organization_memberships.user_id -> profiles/auth identity` (**logical relationship**)

System feature usage:
- Organization access, selected-role switching, membership status, invite acceptance, admin/teacher/student authorization.

RLS/access:
- Base-table RLS is not restated in the current migration set.

Notes:
- The newer authorization model uses `organization_membership_roles` for active roles while `organization_memberships.role` is kept as a compatibility/effective role field.

### `public.organization_membership_roles`

Purpose:
- Per-membership role records that let one organization member hold multiple active roles.

Key columns:
- `id`
- `organization_membership_id`
- `role`
- `status`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_membership_id -> organization_memberships.id`

Enum/status fields:
- `role` uses `public.app_role`
- `status` uses `public.membership_status`

Main relationships:
- `organization_memberships.id -> organization_membership_roles.organization_membership_id` (**FK relationship**)
- `organization_memberships.selected_role_id -> organization_membership_roles.id` (**FK relationship**)

System feature usage:
- Selected-role switching, RLS checks for notifications, organization role grants, teacher/admin/student multi-role state.

RLS/access:
- RLS enabled.
- Select policy: org members can read membership roles.
- No direct end-user manage policy is exposed; writes happen through security-definer functions such as `grant_organization_role` and `set_selected_organization_role`.

Notes:
- This is the real role model used by `is_org_member`, `has_org_role`, and role-scoped notifications.

### `public.organization_invites`

Purpose:
- Pending or processed organization-wide invite records.

Key columns:
- `id`
- `organization_id`
- `email`
- `role`
- `invited_by_user_id`
- `token`
- `status`
- `expires_at`
- `created_at`
- `updated_at`

Primary key:
- `id` (used throughout invite flows; base DDL is not present in repo)

Foreign keys:
- Direct base-table FK definitions are not visible in the checked-in base DDL slice.
- `class_invites.organization_invite_id -> organization_invites.id` is visible downstream.

Enum/status fields:
- `role` uses `public.app_role`
- `status` behaves like membership status and is currently used with `invited`, `active`, and `suspended`

Main relationships:
- `organization_invites.id <- class_invites.organization_invite_id` (**FK relationship**)
- `organization_invites.organization_id -> organizations.id` (**logical relationship**)
- `organization_invites.invited_by_user_id -> auth.users.id` (**logical relationship**)

System feature usage:
- Organization invitations, registration flows, class invite linkage, prior-term registration fallback.

RLS/access:
- Current visible invite-management logic is implemented through security-definer RPCs; base table RLS is not directly visible here.

Notes:
- Pending student invites can carry later class-level and past-term registration workflows.

### `public.organization_settings`

Purpose:
- Per-organization settings for public access and teacher class-management permissions.

Key columns:
- `organization_id`
- `public_features_enabled`
- `public_features_locked_disabled`
- `all_teachers_can_create_classes`
- `all_teachers_can_manage_own_classes`
- `created_at`
- `updated_at`

Primary key:
- `organization_id`

Foreign keys:
- `organization_id -> organizations.id`

Enum/status fields:
- Boolean control flags only.

Main relationships:
- `organizations.id -> organization_settings.organization_id` (**FK relationship**)
- `organization_settings.organization_id -> organization_teacher_class_permissions.organization_id` (**logical parent-child relationship by organization**)

System feature usage:
- Public join-link/org-visibility enablement, preset-level public-access lock, teacher class creation/edit permissions.

RLS/access:
- RLS enabled.
- Select policy: org members can read.
- Write policy: org admins can manage.
- Anonymous/public access is not granted directly to the table, but `is_public_org_features_enabled(uuid)` is executable by `anon`.

Notes:
- `public_features_locked_disabled` is enforced by trigger logic; once an organization is created with public access locked off, later enablement is rejected.

### `public.organization_teacher_class_permissions`

Purpose:
- Per-teacher permission overrides inside one organization.

Key columns:
- `organization_id`
- `teacher_user_id`
- `can_create_classes`
- `can_manage_own_classes`
- `created_at`
- `updated_at`

Primary key:
- Composite primary key: (`organization_id`, `teacher_user_id`)

Foreign keys:
- `organization_id -> organizations.id`
- `teacher_user_id -> profiles.id`

Main relationships:
- `organizations.id -> organization_teacher_class_permissions.organization_id` (**FK relationship**)
- `profiles.id -> organization_teacher_class_permissions.teacher_user_id` (**FK relationship**)

System feature usage:
- Teacher-specific overrides for class creation and class self-management.

RLS/access:
- RLS enabled.
- Select policy: org members can read.
- Write policy: org admins can manage.

Notes:
- Writes are normalized through `update_organization_settings(...)`, which only keeps rows for users who currently hold an active teacher role in the organization.

## Feature Flags, Presets, And Extension Model

### `public.feature_definitions`

Purpose:
- Master catalog of built-in feature flags/tool definitions.

Key columns:
- `key`
- `label`
- `description`
- `parent_key`
- `kind`
- `route_segment`
- `default_enabled`
- `is_system`
- `sort_order`
- `metadata`
- `created_at`
- `updated_at`

Primary key:
- `key`

Foreign keys:
- `parent_key -> feature_definitions.key`

Enum/status fields:
- `kind` uses enum `public.feature_kind` with values `core`, `extension`

Main relationships:
- `feature_definitions.key -> feature_definitions.parent_key` (**FK relationship**, self-reference)
- `feature_definitions.key -> feature_preset_items.feature_key` (**FK relationship**)
- `feature_definitions.key -> organization_feature_settings.feature_key` (**FK relationship**)
- `feature_definitions.key -> class_feature_settings.feature_key` (**FK relationship**)

System feature usage:
- Navigation/tool gating for `home`, `chat`, `materials`, `assignments`, `sessions`, `exam`, `leaderboard`, `extensions`, `extensions.ide`, and `ai` (current label: AI Agent).

RLS/access:
- RLS enabled.
- Authenticated users can read.
- Direct writes are intentionally blocked by a `using (false)` / `with check (false)` policy.

Notes:
- The actual database key remains `ai`; the visible label was renamed to “AI Agent”.

### `public.feature_presets`

Purpose:
- Named preset bundles for organization creation defaults.

Key columns:
- `key`
- `name`
- `description`
- `created_at`
- `updated_at`

Primary key:
- `key`

Foreign keys:
- None.

Main relationships:
- `feature_presets.key -> feature_preset_items.preset_key` (**FK relationship**)

System feature usage:
- Organization creation presets such as `kindergarten`, `primary_school`, `university`, and `open_learning`.

RLS/access:
- RLS enabled.
- Authenticated users can read.

### `public.feature_preset_items`

Purpose:
- Junction table mapping presets to specific feature enablement/config values.

Key columns:
- `preset_key`
- `feature_key`
- `enabled`
- `config`
- `created_at`
- `updated_at`

Primary key:
- Composite primary key: (`preset_key`, `feature_key`)

Foreign keys:
- `preset_key -> feature_presets.key`
- `feature_key -> feature_definitions.key`

Main relationships:
- `feature_presets.key -> feature_preset_items.preset_key` (**FK relationship**)
- `feature_definitions.key -> feature_preset_items.feature_key` (**FK relationship**)

System feature usage:
- Seeds per-preset org feature state during organization creation.

RLS/access:
- RLS enabled.
- Authenticated users can read.

### `public.organization_feature_settings`

Purpose:
- Per-organization feature enablement/config state.

Key columns:
- `organization_id`
- `feature_key`
- `enabled`
- `config`
- `created_at`
- `updated_at`

Primary key:
- Composite primary key: (`organization_id`, `feature_key`)

Foreign keys:
- `organization_id -> organizations.id`
- `feature_key -> feature_definitions.key`

Enum/status fields:
- No enum columns; `config` can store lock metadata such as `locked_disabled`.

Main relationships:
- `organizations.id -> organization_feature_settings.organization_id` (**FK relationship**)
- `feature_definitions.key -> organization_feature_settings.feature_key` (**FK relationship**)
- `organization_feature_settings` seeds `class_feature_settings` rows at class creation (**logical workflow relationship**)

System feature usage:
- Organization-level gating for all built-in tools and extensions.

RLS/access:
- RLS enabled.
- Select policy: org members can read.
- Write policy: org admins can manage.
- Trigger `prevent_locked_disabled_feature_enable` blocks later enablement of preset-disabled features that were locked off at organization creation.

### `public.class_feature_settings`

Purpose:
- Per-class feature enablement/config state.

Key columns:
- `organization_id`
- `class_id`
- `feature_key`
- `enabled`
- `config`
- `created_at`
- `updated_at`

Primary key:
- Composite primary key: (`class_id`, `feature_key`)

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `feature_key -> feature_definitions.key`

Main relationships:
- `organizations.id -> class_feature_settings.organization_id` (**FK relationship**)
- `classes.id -> class_feature_settings.class_id` (**FK relationship**)
- `feature_definitions.key -> class_feature_settings.feature_key` (**FK relationship**)

System feature usage:
- Per-class enablement of navigation/tools such as AI, exams, sessions, leaderboard, IDE, and custom extension visibility.

RLS/access:
- RLS enabled.
- Select policy: org members can read.
- Current write policy: org admins can manage.

Notes:
- Earlier class-manager control was replaced by admin-only management in `20260621120000_restrict_class_settings_to_admins.sql`.

### `public.organization_extensions`

Purpose:
- Organization-scoped custom extension definitions.

Key columns:
- `id`
- `organization_id`
- `name`
- `slug`
- `description`
- `launch_url`
- `enabled`
- `sort_order`
- `config`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`

Main relationships:
- `organizations.id -> organization_extensions.organization_id` (**FK relationship**)
- `organization_extensions.id -> class_extension_settings.extension_id` (**FK relationship**)

System feature usage:
- Custom extension registration and launch URLs for organization-specific tools.

RLS/access:
- RLS enabled.
- Select policy: org members can read.
- Write policy: org admins can manage.

### `public.class_extension_settings`

Purpose:
- Per-class enable/disable/config rows for organization-scoped extensions.

Key columns:
- `organization_id`
- `class_id`
- `extension_id`
- `enabled`
- `config`
- `created_at`
- `updated_at`

Primary key:
- Composite primary key: (`class_id`, `extension_id`)

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `extension_id -> organization_extensions.id`

Main relationships:
- `organizations.id -> class_extension_settings.organization_id` (**FK relationship**)
- `classes.id -> class_extension_settings.class_id` (**FK relationship**)
- `organization_extensions.id -> class_extension_settings.extension_id` (**FK relationship**)

System feature usage:
- Per-class custom-extension visibility/availability.

RLS/access:
- RLS enabled.
- Select policy: org members can read.
- Current write policy: org admins can manage.

Notes:
- Like `class_feature_settings`, this became admin-managed rather than manager-managed in later migrations.

## Classes, Rosters, Public Visibility, And Archived History

### `public.classes`

Purpose:
- Core class/course record owned by an organization.

Key columns:
- `id`
- `organization_id`
- `name`
- `code`
- `teacher_user_id`
- `color`
- `description`
- `room`
- `semester`
- `stage`
- `organization_visible`
- `results_visible_to_students`
- `teacher_can_toggle_results_visibility`
- `is_archived`
- `ended_at`
- `ended_by_user_id`
- `archived_edited_at`
- `archived_edited_by_user_id`
- `created_at`
- `updated_at`

Primary key:
- `id` (canonical class key used by all downstream FK tables; base class DDL itself is not present in repo)

Foreign keys:
- Visible later FKs:
  - `ended_by_user_id -> auth.users.id`
  - `archived_edited_by_user_id -> auth.users.id`
- Original FK visibility for `organization_id` and `teacher_user_id` is missing from the base DDL slice.

Enum/status fields:
- `is_archived` is the active/archive lifecycle flag.
- `semester` and `stage` are now required non-blank text fields.

Main relationships:
- `classes.id -> class_feature_settings.class_id` (**FK relationship**)
- `classes.id -> class_extension_settings.class_id` (**FK relationship**)
- `classes.id -> class_invites.class_id` (**FK relationship**)
- `classes.id -> class_visibility_preferences.class_id` (**FK relationship**)
- `classes.id -> class_materials.class_id` (**FK relationship**)
- `classes.id -> class_messages.class_id` (**FK relationship**)
- `classes.id -> class_assignments.class_id` (**FK relationship**)
- `classes.id -> class_assignment_files.class_id` (**FK relationship**)
- `classes.id -> class_assignment_submissions.class_id` (**FK relationship**)
- `classes.id -> class_live_sessions.class_id` (**FK relationship**)
- `classes.id -> exams.class_id` (**FK relationship**)
- `classes.id -> exam_attempts.class_id` (**FK relationship**)
- `classes.id -> notifications.class_id` (**FK relationship**)
- `classes.organization_id -> organizations.id` (**logical relationship**)
- `classes.teacher_user_id -> profiles.id` (**logical relationship**)
- `classes.id <- class_memberships.class_id` (**logical relationship**)

System feature usage:
- Class creation/update, roster assignment, organization-visible classes, archived past terms, results visibility, live sessions, content, exams.

RLS/access:
- Base class-table RLS is not directly visible because the original class DDL is not in repo.
- Access is enforced heavily by RPC guards such as `can_manage_class`, `can_teacher_create_class`, `can_teacher_manage_own_classes`, `end_class`, `end_classes`, and `set_class_results_visibility`.

Notes:
- `subject` and `schedule_text` were removed from the schema.
- Past-term history uses archived classes instead of a separate history table.

### `public.class_memberships`

Purpose:
- Class-level membership/roster rows.

Key columns:
- `id`
- `organization_id`
- `class_id`
- `user_id`
- `role`
- `created_at`
- `updated_at`

Primary key:
- `id` is used as the canonical row identifier in current code; original base DDL is not present in repo.

Foreign keys:
- Direct base-table FK declarations are not visible in the checked-in base DDL slice.

Enum/status fields:
- `role` is a class-level role field.
- Current code and permission checks confirm `teacher`, `student`, and `ta` usage.

Main relationships:
- `class_memberships.organization_id -> organizations.id` (**logical relationship**)
- `class_memberships.class_id -> classes.id` (**logical relationship**)
- `class_memberships.user_id -> profiles/auth identity` (**logical relationship**)

System feature usage:
- Class rosters, teacher assignment checks, manager checks, student visibility, results summaries, live session membership gating.

RLS/access:
- Original base table RLS is not visible in the checked-in base DDL slice.

Notes:
- Later migrations enforce one active teacher row per class through a partial unique index on `class_id where role = 'teacher'`.
- Current admin routes restrict roster management workflows to org admins, but some general manager checks still treat `teacher`/`ta` as class managers.

### `public.class_invites`

Purpose:
- Pending or activated class-level invite rows, optionally linked to an organization invite.

Key columns:
- `id`
- `organization_id`
- `class_id`
- `email`
- `role`
- `organization_invite_id`
- `invited_by_user_id`
- `status`
- `previous_grade_payload`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `organization_invite_id -> organization_invites.id`
- `invited_by_user_id -> auth.users.id`

Enum/status fields:
- `role` uses `public.class_membership_role`
- `status` uses `public.membership_status`

Main relationships:
- `organizations.id -> class_invites.organization_id` (**FK relationship**)
- `classes.id -> class_invites.class_id` (**FK relationship**)
- `organization_invites.id -> class_invites.organization_invite_id` (**FK relationship**)
- `auth.users.id -> class_invites.invited_by_user_id` (**FK relationship**)

System feature usage:
- Class invitations, pending teacher/student assignment, student registration with imported past-term grades.

RLS/access:
- RLS enabled.
- Policy: class managers can manage class invites.

Notes:
- `previous_grade_payload` is the current pending-storage mechanism for importing previous-term student grades during invite acceptance.

### `public.class_visibility_preferences`

Purpose:
- Per-student hide/show preferences for organization-visible classes.

Key columns:
- `id`
- `organization_id`
- `class_id`
- `user_id`
- `hidden`
- `hidden_at`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `user_id -> auth.users.id`

Main relationships:
- `organizations.id -> class_visibility_preferences.organization_id` (**FK relationship**)
- `classes.id -> class_visibility_preferences.class_id` (**FK relationship**)
- `auth.users.id -> class_visibility_preferences.user_id` (**FK relationship**)

System feature usage:
- Organization-visible class hiding for students.

RLS/access:
- RLS enabled.
- Select: users can read their own preferences.
- Insert/update: only student-role users, only for organization-visible classes.
- Delete: student users can delete their own preferences.

Notes:
- This is a user-preference table, not a roster/history table.

### `public.organization_join_links`

Purpose:
- Public or semi-public organization join URLs/tokens.

Key columns:
- `id`
- `organization_id`
- `purpose`
- `token`
- `default_role`
- `enabled`
- `approval_required`
- `max_uses`
- `use_count`
- `expires_at`
- `created_by_user_id`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `created_by_user_id -> auth.users.id`

Enum/status fields:
- `default_role` uses `public.app_role`, constrained to teacher/student

Main relationships:
- `organizations.id -> organization_join_links.organization_id` (**FK relationship**)
- `auth.users.id -> organization_join_links.created_by_user_id` (**FK relationship**)
- `organization_join_links.id -> organization_join_requests.join_link_id` (**FK relationship**)

System feature usage:
- Public access, self-service join links, approval-required flows, invite-free student/teacher onboarding.

RLS/access:
- RLS enabled.
- Select/manage: org admins only.

Notes:
- Older one-link-per-organization behavior was removed; multiple links are now supported, and `purpose` is part of the model.

### `public.organization_join_requests`

Purpose:
- Pending/approved/rejected approval workflow for public join links.

Key columns:
- `id`
- `organization_id`
- `join_link_id`
- `user_id`
- `requested_role`
- `status`
- `reviewed_by_user_id`
- `reviewed_at`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `join_link_id -> organization_join_links.id`
- `user_id -> auth.users.id`
- `reviewed_by_user_id -> auth.users.id`

Enum/status fields:
- `requested_role` uses `public.app_role`, constrained to teacher/student
- `status` is checked to `pending`, `approved`, `rejected`

Main relationships:
- `organizations.id -> organization_join_requests.organization_id` (**FK relationship**)
- `organization_join_links.id -> organization_join_requests.join_link_id` (**FK relationship**)
- `auth.users.id -> organization_join_requests.user_id` (**FK relationship**)
- `auth.users.id -> organization_join_requests.reviewed_by_user_id` (**FK relationship**)

System feature usage:
- Public join approval queue for admins.

RLS/access:
- RLS enabled.
- Org admins can read/manage all requests.
- Users can read their own requests.

## Learning Materials, Chat, Assignments, And Notifications

### `public.class_materials`

Purpose:
- Persisted learning materials and chat-linked media files for a class.

Key columns:
- `id`
- `organization_id`
- `class_id`
- `uploaded_by_user_id`
- `title`
- `description`
- `type`
- `source`
- `chat_message_id`
- `storage_bucket`
- `storage_key`
- `original_filename`
- `mime_type`
- `size_bytes`
- `ai_summary`
- `ai_summary_used_file_text`
- `ai_summary_generated_at`
- `ai_extracted_content`
- `ai_extracted_content_used_file_content`
- `ai_extracted_content_generated_at`
- `deleted_at`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `uploaded_by_user_id -> profiles.id`
- `chat_message_id -> class_messages.id`

Enum/status fields:
- `type` uses enum `public.class_material_type`: `image`, `pdf`, `video`, `slide`
- `source` uses enum `public.class_material_source`: `manual`, `chat`

Main relationships:
- `organizations.id -> class_materials.organization_id` (**FK relationship**)
- `classes.id -> class_materials.class_id` (**FK relationship**)
- `profiles.id -> class_materials.uploaded_by_user_id` (**FK relationship**)
- `class_messages.id -> class_materials.chat_message_id` (**FK relationship**)
- `class_messages.material_id -> class_materials.id` (**FK relationship**, reverse optional link)

System feature usage:
- Class materials library, chat media uploads, AI summary/extraction cache, material downloads.

RLS/access:
- RLS enabled.
- Read: class members/managers, excluding soft-deleted rows.
- Create/update/delete: class managers.
- Additional insert policy: class members can create `source = 'chat'` materials.

Notes:
- File storage is backed by AWS S3 (`AWS_S3_BUCKET`, signed URLs), not by a dedicated database storage table and not by Supabase Storage metadata in this repo.

### `public.class_messages`

Purpose:
- Class chat, announcements, and chat-media message records.

Key columns:
- `id`
- `organization_id`
- `class_id`
- `sender_user_id`
- `sender_role`
- `content`
- `kind`
- `material_id`
- `media_title`
- `original_filename`
- `mime_type`
- `size_bytes`
- `material_type`
- `show_in_announcement_carousel`
- `created_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `sender_user_id -> profiles.id`
- `material_id -> class_materials.id`

Enum/status fields:
- `kind` uses enum `public.class_message_kind`: `text`, `announcement`, `media`
- `sender_role` is checked to `student`, `teacher`, `admin`

Main relationships:
- `organizations.id -> class_messages.organization_id` (**FK relationship**)
- `classes.id -> class_messages.class_id` (**FK relationship**)
- `profiles.id -> class_messages.sender_user_id` (**FK relationship**)
- `class_materials.id -> class_messages.material_id` (**FK relationship**)

System feature usage:
- Chat timeline, announcements, chat media snapshots, announcement carousel.

RLS/access:
- RLS enabled.
- Read: class members/managers.
- Insert: class members; announcements require class-manager rights.
- Delete: class managers can delete announcement rows.
- Update: class managers can update `show_in_announcement_carousel` for announcement rows.

Notes:
- There is no separate announcements table.

### `public.class_assignments`

Purpose:
- Assignment definitions for a class.

Key columns:
- `id`
- `organization_id`
- `class_id`
- `created_by_user_id`
- `title`
- `description`
- `due_at`
- `max_score`
- `status`
- `allow_late_submissions`
- `allow_text_submission`
- `allow_file_submission`
- `created_at`
- `updated_at`
- `deleted_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `created_by_user_id -> profiles.id`

Enum/status fields:
- `status` is checked to `draft`, `published`

Main relationships:
- `organizations.id -> class_assignments.organization_id` (**FK relationship**)
- `classes.id -> class_assignments.class_id` (**FK relationship**)
- `profiles.id -> class_assignments.created_by_user_id` (**FK relationship**)
- `class_assignments.id -> class_assignment_files.assignment_id` (**FK relationship**)
- `class_assignments.id -> class_assignment_submissions.assignment_id` (**FK relationship**)

System feature usage:
- Assignment authoring, publish/draft lifecycle, AI drafting support, roster result summaries.

RLS/access:
- RLS enabled.
- Read: published assignments for class members; all non-deleted assignments for managers.
- Create/update: class managers only.

Notes:
- Soft delete is modeled via `deleted_at`; there is no separate archive table.

### `public.class_assignment_files`

Purpose:
- Prompt/supporting files attached to assignments.

Key columns:
- `id`
- `organization_id`
- `class_id`
- `assignment_id`
- `uploaded_by_user_id`
- `storage_bucket`
- `storage_key`
- `original_filename`
- `mime_type`
- `size_bytes`
- `created_at`
- `deleted_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `assignment_id -> class_assignments.id`
- `uploaded_by_user_id -> profiles.id`

Main relationships:
- `organizations.id -> class_assignment_files.organization_id` (**FK relationship**)
- `classes.id -> class_assignment_files.class_id` (**FK relationship**)
- `class_assignments.id -> class_assignment_files.assignment_id` (**FK relationship**)
- `profiles.id -> class_assignment_files.uploaded_by_user_id` (**FK relationship**)

System feature usage:
- Assignment attachments and downloadable prompt files.

RLS/access:
- RLS enabled.
- Read: class members if the parent assignment is published, or managers.
- Create/update: class managers only.

Notes:
- Files are stored in AWS S3; the table stores object references only.

### `public.class_assignment_submissions`

Purpose:
- Student submissions and assignment grading records.

Key columns:
- `id`
- `organization_id`
- `class_id`
- `assignment_id`
- `student_user_id`
- `text_response`
- `file_storage_bucket`
- `file_storage_key`
- `file_original_filename`
- `file_mime_type`
- `file_size_bytes`
- `submitted_at`
- `is_late`
- `score`
- `feedback`
- `graded_at`
- `graded_by_user_id`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `assignment_id -> class_assignments.id`
- `student_user_id -> profiles.id`
- `graded_by_user_id -> profiles.id`

Main relationships:
- `organizations.id -> class_assignment_submissions.organization_id` (**FK relationship**)
- `classes.id -> class_assignment_submissions.class_id` (**FK relationship**)
- `class_assignments.id -> class_assignment_submissions.assignment_id` (**FK relationship**)
- `profiles.id -> class_assignment_submissions.student_user_id` (**FK relationship**)
- `profiles.id -> class_assignment_submissions.graded_by_user_id` (**FK relationship**)

System feature usage:
- Student work submission, grading, results display, imported past-term grades.

RLS/access:
- RLS enabled.
- Read: managers or the owning student.
- Insert: student can create own submission if class member.
- Update: owning student or manager.
- Validation trigger also enforces assignment status/submission-mode rules.

Notes:
- This table stores assignment grades directly; there is no separate assignment-results table.
- Imported previous-term grades are currently materialized here via helper RPCs.

### `public.notifications`

Purpose:
- User notification inbox records.

Key columns:
- `id`
- `organization_id`
- `class_id`
- `recipient_user_id`
- `recipient_role`
- `actor_user_id`
- `type`
- `title`
- `body`
- `href`
- `metadata`
- `event_key`
- `read_at`
- `created_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `recipient_user_id -> profiles.id`
- `actor_user_id -> profiles.id`

Enum/status fields:
- `type` uses enum `public.notification_type` with current values:
  - `chat_announcement`
  - `session_started`
  - `material_added`
  - `assignment_published`
  - `assignment_submitted`
  - `assignment_graded`
  - `exam_published`
  - `exam_submitted`
  - `exam_results_released`
- `recipient_role` uses `public.app_role`

Main relationships:
- `organizations.id -> notifications.organization_id` (**FK relationship**)
- `classes.id -> notifications.class_id` (**FK relationship**)
- `profiles.id -> notifications.recipient_user_id` (**FK relationship**)
- `profiles.id -> notifications.actor_user_id` (**FK relationship**)

System feature usage:
- Announcement, session, materials, assignments, and exam inbox notifications.

RLS/access:
- RLS enabled.
- Direct table grants:
  - `select`
  - `update (read_at)`
  - `delete`
- Policies require:
  - `recipient_user_id = auth.uid()`
  - and the current membership’s selected active organization role must equal `recipient_role`
- Inserts are not granted directly to end users; server code uses security-definer helper functions.

Notes:
- Role-scoped notifications are a major current-schema change versus earlier simpler inbox logic.

## Exams, Attempts, Answers, And Result Release

### `public.exams`

Purpose:
- Exam header/definition rows for a class.

Key columns:
- `id`
- `organization_id`
- `class_id`
- `title`
- `duration_minutes`
- `total_points`
- `start_at`
- `end_at`
- `status`
- `created_by_user_id`
- `published_at`
- `passcode_hash`
- `rules_override_json`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `created_by_user_id -> auth.users.id`

Enum/status fields:
- `status` uses enum `public.exam_status`: `upcoming`, `live`, `ended`

Main relationships:
- `organizations.id -> exams.organization_id` (**FK relationship**)
- `classes.id -> exams.class_id` (**FK relationship**)
- `auth.users.id -> exams.created_by_user_id` (**FK relationship**)
- `exams.id -> exam_questions.exam_id` (**FK relationship**)
- `exams.id -> exam_attempts.exam_id` (**FK relationship**)

System feature usage:
- Exam authoring, publish schedule, passcode-protected starts, exam-mode access.

RLS/access:
- RLS enabled.
- Read: class managers, or class members when `published_at` is not null.
- Manage: class managers only.

Notes:
- Even though class members can read published exam headers directly, student attempt/question workflows are primarily mediated through server-side service code.

### `public.exam_questions`

Purpose:
- Question rows belonging to one exam.

Key columns:
- `id`
- `organization_id`
- `exam_id`
- `position`
- `question_type`
- `prompt`
- `options_json`
- `correct_answer_json`
- `points`
- `language`
- `starter_code`
- `visible_tests_json`
- `hidden_tests_json`
- `evaluator_key`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `exam_id -> exams.id`

Enum/status fields:
- `question_type` uses enum `public.exam_question_kind`: `mcq`, `short`, `code`

Main relationships:
- `organizations.id -> exam_questions.organization_id` (**FK relationship**)
- `exams.id -> exam_questions.exam_id` (**FK relationship**)
- `exam_questions.id -> exam_answers.exam_question_id` (**FK relationship**)

System feature usage:
- Exam content, question ordering, optional coding-question evaluator metadata/tests.

RLS/access:
- RLS enabled.
- Read/manage: class managers only through policies.

Notes:
- The current TypeScript student-facing types only expose `mcq` and `short`, but the database schema still includes `code` as a real question kind.

### `public.exam_attempts`

Purpose:
- Per-student exam attempt records and exam result-release state.

Key columns:
- `id`
- `organization_id`
- `class_id`
- `exam_id`
- `student_user_id`
- `status`
- `started_at`
- `submitted_at`
- `total_score`
- `attempt_number`
- `deadline_at`
- `rules_snapshot_json`
- `needs_manual_review`
- `auto_submitted_at`
- `integrity_status`
- `flagged_at`
- `flagged_by_user_id`
- `flag_reason`
- `voided_at`
- `voided_by_user_id`
- `void_reason`
- `graded_at`
- `graded_by_user_id`
- `results_released_at`
- `results_released_by_user_id`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `exam_id -> exams.id`
- `student_user_id -> auth.users.id`
- `flagged_by_user_id -> auth.users.id`
- `voided_by_user_id -> auth.users.id`
- `graded_by_user_id -> auth.users.id`
- `results_released_by_user_id -> auth.users.id`

Enum/status fields:
- `status` uses enum `public.exam_attempt_status`: `in_progress`, `submitted`, `graded`, `voided`
- `integrity_status` is text checked to `clear`, `reported`, `flagged`, `voided`

Main relationships:
- `organizations.id -> exam_attempts.organization_id` (**FK relationship**)
- `classes.id -> exam_attempts.class_id` (**FK relationship**)
- `exams.id -> exam_attempts.exam_id` (**FK relationship**)
- `auth.users.id -> exam_attempts.student_user_id` (**FK relationship**)
- `exam_attempts.id -> exam_answers.exam_attempt_id` (**FK relationship**)

System feature usage:
- Starting/submitting attempts, grading, retakes, integrity handling, released exam results.

RLS/access:
- RLS enabled.
- Direct policy read/manage access is manager-only.
- Student access in the app is handled through server-side routes plus privileged server queries after custom class-context checks.

Notes:
- This table stores exam-level grade aggregates directly.
- Retake history and integrity event streams are not stored here as separate child tables; they are recorded in `audit_logs`.

### `public.exam_answers`

Purpose:
- Per-question answer rows within an attempt.

Key columns:
- `id`
- `organization_id`
- `exam_attempt_id`
- `exam_question_id`
- `answer_json`
- `auto_score`
- `teacher_score`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `exam_attempt_id -> exam_attempts.id`
- `exam_question_id -> exam_questions.id`

Main relationships:
- `organizations.id -> exam_answers.organization_id` (**FK relationship**)
- `exam_attempts.id -> exam_answers.exam_attempt_id` (**FK relationship**)
- `exam_questions.id -> exam_answers.exam_question_id` (**FK relationship**)

System feature usage:
- Stored student answers, auto-grading, teacher overrides, released question-level results.

RLS/access:
- RLS enabled.
- Direct policy read/manage access is manager-only.
- Student answer save/load is mediated through server-side exam services.

Notes:
- There is no separate answer-review table; teacher scoring lives directly here.

## Live Sessions, Audit, And External Auth

### `public.class_live_sessions`

Purpose:
- Session state/header table for one live class session per class.

Key columns:
- `id`
- `organization_id`
- `class_id`
- `room_name`
- `live_session_id`
- `started_by_user_id`
- `status`
- `started_at`
- `last_seen_at`
- `ended_at`
- `created_at`
- `updated_at`

Primary key:
- `id`

Foreign keys:
- `organization_id -> organizations.id`
- `class_id -> classes.id`
- `started_by_user_id -> profiles.id`

Enum/status fields:
- `status` is text currently checked to `pending`, `live`, `ended`

Main relationships:
- `organizations.id -> class_live_sessions.organization_id` (**FK relationship**)
- `classes.id -> class_live_sessions.class_id` (**FK relationship**)
- `profiles.id -> class_live_sessions.started_by_user_id` (**FK relationship**)

System feature usage:
- LiveKit session claiming, manager/session-start notifications, session presence heartbeat, end-class shutdown.

RLS/access:
- RLS enabled.
- Read: org admins, class members, or class managers.
- Insert: class managers.
- Update: class managers and the session starter.
- Table is published to Supabase realtime.

Notes:
- The database only tracks session lifecycle metadata.
- Whiteboard operations and participant media state are not stored in dedicated database tables.

### `public.audit_logs`

Purpose:
- Cross-cutting audit/event log table used across organizations, invites, classes, join flows, and exams.

Key columns confirmed from current code:
- `organization_id`
- `actor_user_id`
- `action`
- `entity_type`
- `entity_id`
- `payload`
- `created_at`

Primary key:
- Not directly verifiable from the checked-in repo slice.

Foreign keys:
- No visible base-table DDL in the repo slice.

Main relationships:
- `audit_logs.organization_id -> organizations.id` (**logical relationship**)
- `audit_logs.actor_user_id -> auth.users.id` (**logical relationship**)
- `audit_logs.entity_id` is a **polymorphic logical relationship** to many different entities, including organization memberships, invites, classes, join requests/links, exams, and exam attempts.

System feature usage:
- Audit trail for organization creation, invites, joins, class lifecycle, results visibility, exam events, retake grants, integrity events.

RLS/access:
- Base audit-log DDL/RLS is not present in the current repo slice.

Notes:
- Exam integrity events and retake grant history are currently implemented through this table instead of dedicated child tables.

### External table: `auth.users`

Purpose:
- Supabase authentication user table referenced by many Eduverse tables.

Confirmed referenced column:
- `id`

Direct relationships visible in Eduverse migrations:
- `class_invites.invited_by_user_id -> auth.users.id` (**FK relationship**)
- `organization_join_links.created_by_user_id -> auth.users.id` (**FK relationship**)
- `organization_join_requests.user_id -> auth.users.id` (**FK relationship**)
- `organization_join_requests.reviewed_by_user_id -> auth.users.id` (**FK relationship**)
- `class_visibility_preferences.user_id -> auth.users.id` (**FK relationship**)
- `exams.created_by_user_id -> auth.users.id` (**FK relationship**)
- `exam_attempts.student_user_id -> auth.users.id` (**FK relationship**)
- `exam_attempts.flagged_by_user_id -> auth.users.id` (**FK relationship**)
- `exam_attempts.voided_by_user_id -> auth.users.id` (**FK relationship**)
- `exam_attempts.graded_by_user_id -> auth.users.id` (**FK relationship**)
- `exam_attempts.results_released_by_user_id -> auth.users.id` (**FK relationship**)
- `classes.ended_by_user_id -> auth.users.id` (**FK relationship**)
- `classes.archived_edited_by_user_id -> auth.users.id` (**FK relationship**)

Notes:
- `profiles.id` behaves as the app-facing identity mirror of `auth.users.id`, but that base relationship is only code-visible in this repository snapshot.

## Feature-Level Summary

- Multi-organization structure:
  - Real and current, centered on `organizations`, `organization_memberships`, `organization_membership_roles`, `organization_invites`, `organization_settings`, `organization_join_links`, and `organization_join_requests`.
- Organization/class permission model:
  - Real and current, using selected org roles plus `organization_teacher_class_permissions`.
- Class membership model:
  - Real and current, using `classes`, `class_memberships`, and `class_invites`.
- Public join or approval flows:
  - Real and current, using `organization_join_links` and `organization_join_requests`.
- Materials:
  - Real and current, using `class_materials`.
- Assignments:
  - Real and current, using `class_assignments`, `class_assignment_files`, and `class_assignment_submissions`.
- Exams/questions/attempts/answers:
  - Real and current, using `exams`, `exam_questions`, `exam_attempts`, and `exam_answers`.
- Results/grades:
  - Real and current, but stored directly on assignment submissions and exam attempt/answer tables rather than a dedicated results table.
- Chat/messages/media:
  - Real and current, using `class_messages` plus `class_materials` for chat-linked files.
- Announcements:
  - Real and current, represented by `class_messages.kind = 'announcement'`.
- Notifications:
  - Real and current, using `notifications`.
- Live sessions:
  - Real and current, using `class_live_sessions`.
- AI-related persistence:
  - Real and current only as feature flags plus cached fields on `class_materials`; there is no separate AI history table.
- IDE/extensions-related persistence:
  - Real and current for extension metadata/settings (`organization_extensions`, `class_extension_settings`, feature flags).
  - No dedicated IDE workspace database table.
- Archived/past-term history:
  - Real and current, using archived `classes`, imported assignment rows, submission rows, and `class_invites.previous_grade_payload`.


