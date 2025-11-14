# 16-delete-comment-low

**As a** logged-in user  
**I want to** delete my own comments  
**So that** I can remove comments I no longer want to keep

**Priority:** Low (Not required for initial release)

**Acceptance Criteria:**
- Delete button is visible only on user's own comments
- System asks for confirmation before deletion
- Deleted comment is removed from view (using HTMX)
- Replies to deleted comment are handled (deleted or preserved with "deleted" indicator)

