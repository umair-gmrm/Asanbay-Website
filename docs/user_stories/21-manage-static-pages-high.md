# 21-manage-static-pages-high

**As an** admin  
**I want to** manage About Us and Content Policies pages using Django admin  
**So that** I can update page content through database changes without code modifications

**Acceptance Criteria:**
- Admin can access static pages management in Django admin interface
- Admin can create/edit "About Us" page with:
  - Page title (e.g., "About Us")
  - Page content (textarea - rich text editor optional for future)
  - Page slug/URL (e.g., "about-us")
  - Active/inactive status (to show/hide page)
  - Last updated timestamp (auto-tracked)
- Admin can create/edit "Content Policies" page with:
  - Page title (e.g., "Content Policies")
  - Page content (textarea - rich text editor optional for future)
  - Page slug/URL (e.g., "content-policies")
  - Active/inactive status (to show/hide page)
  - Last updated timestamp (auto-tracked)
- Content is stored in database (not hardcoded in templates)
- Admin can update page content at any time through Django admin
- Changes are reflected immediately on the public website
- Pages can be activated/deactivated without deleting content
- Django admin interface is accessible to authorized admin users only
- **Note:** Rich text editor is low priority - plain textarea is acceptable for initial release

