```
1. Mobile Technology Stack
The mobile repository is an Expo + React Native application built in TypeScript.
The root shell is [App.tsx](DEduverse-mobile-appApp.tsx), datastate is
centralized in [srcprovidersEduverseProvider.tsx](DEduverse-mobile-
appsrcprovidersEduverseProvider.tsx), and backend access is wrapped in
[srcserviceseduverseApi.ts](DEduverse-mobile-appsrcserviceseduverseApi.ts).
Framework Expo SDK 54 with React Native 0.81 and React 19.
Programming language TypeScript.
Main libraries @supabasesupabase-js, @react-native-async-storageasync-storage,
nativewind, expo-notifications, expo-file-system, expo-sharing, @livekitreact-
native, livekit-client, lucide-react-native.
Styling NativeWind + Tailwind config.
Navigationstate style simple state-based screen switching in App.tsx; no React
Navigation setup is present.
Project structure srccomponents for reusable UI, srcscreens for major screens,
srcproviders for app state, srcservices for APIdevice services, srclib for
Supabase client setup, srcconfig for environment handling.
2. Current Implemented ScreensFeatures
ScreenWhat it appears to doData sourcestatus
AuthScreenLogin, signup, forgot passwordReal Supabase auth
DashboardScreenShows current class, summary metrics, next assignment summary,
recent notifications, entry to chatmaterialsliveupdatesReal providerAPI
data; assignment use is summary-only
CoursesScreenLists classes, live sessions, and materials; opens class
materials subview with search and downloadshare Real API data for
classesmaterialslive sessions; search is local UI
ChatScreenLists class threads, opens a class conversation, sends text
messages, shows announcementsReal API-backed messages; announcements come from
notification records
UpdatesScreenNotification inbox, unread count, mark singleall as read
Real API-backed notifications
MoreScreenProfile summary, org switching, theme toggle, push notification
toggle, sign outMixed org switchingsign out are real; theme and push
preference are mostly local device state
LiveSessionScreenJoinstartend LiveKit session, miccamera toggles, participant
tilesReal integration, but requires a dev build
```

```
Key reusable components already implemented include BottomTabs, AppHeader,
CourseCard, MetricCard, NotificationRow, SettingRow, FormInput, ActionButton,
Badge, and ProgressBar.
```

```
Important limitation I did not find a dedicated assignments screen or an
assignment submission form in the current code. Assignments are loaded and used
for countsprogress, but not exposed as a full workflow. I also did not find
mock-data files; most content is either real API-backed state or local UI state.
3. BackendAPI Integration
The mobile app uses Supabase mainly for authenticationsession management through
[srclibsupabase.ts](DEduverse-mobile-appsrclibsupabase.ts), with AsyncStorage
session persistence. Domain data is then fetched from the Eduverse backend
through [srcserviceseduverseApi.ts](DEduverse-mobile-
appsrcserviceseduverseApi.ts), using the Supabase access token as a bearer
token.
```

```
Integrated pieces already visible in code
Authentication sign in, sign up, reset password, sign out, auth state listener.
Environment config [srcconfigenv.ts](DEduverse-mobile-appsrcconfigenv.ts) and
[app.config.js](DEduverse-mobile-appapp.config.js) read EXPO_PUBLIC_ or
NEXT_PUBLIC_ values.
```

```
Backend endpoints used apime, apiorganizationsidclasses, apinotifications,
apiorganizationsidlive-sessions, apilivekittoken, apiclassesidlive-session,
apiclassesidassignments, apiclassesidmaterials, apiclassesidmessages, and
material download-url routes.
Materials downloaded via signed URLs, then openedshared locally.
Notifications polled from API, then shown as local device notifications while
the app is running.
```

```
Live sessions token creation and session lifecycle are API-backed; media room is
```

```
LiveKit-backed.
Clearly not fully integrated yet
No direct evidence of remote Expo push token registration or server-side push
delivery.
```

```
No direct business-table access from mobile beyond Supabase auth; classroom data
intentionally goes through the Eduverse web API.
No visible assignment submission API call in the current mobile code.
No chat media upload flow.
No offline data synccache layer beyond auth session persistence and a stored
push-notification preference.
Note .env.example defines the needed variables, but the repository
snapshot’s .env is empty, so active runtime credentials are not included in the
repo.
4. User Roles and Mobile Workflows
The app recognizes student, teacher, and admin behavior. In the role mapping,
org_owner and org_admin are treated as admin; teacher stays teacher; all others
default to student.
Visible workflow from code
User authenticates with Supabase.
The app loads apime and determines the activedefault organization.
It then loads classes, notifications, assignments, materials, live sessions, and
initial messages.
The main bottom-tab flow is Today, Classes, Chat, and More.
From there, the user can open updates, switch organizations, view materials,
chat in a class, or join a live session.
Role differences are currently limited. Teachersadmins can start live sessions;
students can only join an existing one. I did not find separate teacher
dashboards or admin management screens.
5. Completeness Status
Fully implemented features emailpassword auth flow, session persistence,
organization switching, dashboard summaries, class listing, materials
browsingdownloading, notifications inbox with read actions, basic class chat
sendload, and basic LiveKit room participationstartend.
Partially implemented features assignments are loaded but only used for
metricsprogress; chat thread countspreviews are limited because messages are
loaded for one active class at a time; push notifications are foregroundlocal
rather than full remote push; settings are partly local-only; live sessions do
not include whiteboard or in-session chat.
Planned or placeholder features richer preferences, remote push token
registrationdelivery, offline caching, chat media upload, LiveKit whiteboard,
in-session chat, and fuller assignment handling are described in the README as
next steps, but are not fully present in code.
Missing features compared with the web application organization management,
class creationarchive management, analytics, exam authoring, rich content
editing, feature configuration, and broader administrative workflows remain web-
side rather than mobile-side.
```

```
One more caution the README describes some capabilities more broadly than the
current code supports. For example, it mentions assignment submission, but the
current mobile UIcodebase shows assignment readingsummary only, not a complete
submission workflow.
```

```
6. Relationship to the Main Eduverse Platform
This mobile app is best described as a companion application to the main
Eduverse platform, not a full standalone replacement. It reuses the same
Supabase authentication context, depends on the Eduverse web API for classroom
data, and focuses on lighter daily workflows such as checking classes, reading
updates, opening materials, chatting, and joining live sessions.
Because the implementation is still incomplete, it should be documented as an
extension of the main web platform rather than as a feature-complete mobile
version of Eduverse.
```

```
7. Academic Documentation Notes
Safe wording for the graduation report
“Eduverse Mobile is an ExpoReact Native companion application under active
development.”
```

```
“The current mobile version supports authenticated access, class overviews,
```

```
notifications, materials, class chat, organization switching, and basic live-
session participation.”
“The mobile client uses Supabase for authentication and consumes Eduverse
backend API routes for domain data.”
“Administrative workflows and several advanced learning features remain web-only
or under development.”
What can be confidently documented
The technology stack.
The providerservice-based architecture.
Supabase authentication integration.
API-backed loading of classes, notifications, materials, messages, and live
sessions.
The current screen set and mobile companion role.
What should be described as future work or ongoing development
Full assignment workflow and submission UI.
Remote push notifications.
Offline cachingsync.
Media upload in chat.
Live-session whiteboardin-session chat.
Feature parity with the main web platform.
A final caution for academic writing avoid claiming full mobile parity with the
web app, and avoid presenting assignment handling or advanced notifications as
finished. Also, automated verification in this repo is still light; I found only
environmentconfig tests.
Mobile Documentation Summary
Eduverse Mobile is a companion application for the main Eduverse platform built
with Expo, React Native, and TypeScript. In its current repository state, it
already provides real Supabase-based authentication and API-backed access to
class summaries, notifications, materials, class chat, organization switching,
and basic LiveKit live sessions. However, the mobile implementation is still
under development and should not be described as feature-complete, since
assignment workflows, remote push notifications, offline support, and
administrative features remain partial, web-only, or planned for future work.
```

