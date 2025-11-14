# 13-reply-to-comment-low

**As a** logged-in user  
**I want to** reply to an existing comment  
**So that** I can engage in threaded discussions

**Priority:** Low (Not required for initial release)

**Acceptance Criteria:**
- Reply button is available **only** to logged-in users on each comment
- For non-logged-in visitors, reply button shows "Login to reply" prompt
- Clicking reply shows a reply form
- User can enter reply text
- Reply is posted and displayed nested under the parent comment (using HTMX)
- Reply shows author name and timestamp
- Reply is indented to show hierarchy
- **Login is required** to post replies (viewing replies does not require login)

