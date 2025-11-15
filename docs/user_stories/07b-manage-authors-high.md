# 07b-manage-authors-high

**As an** admin  
**I want to** create and manage authors using Django admin  
**So that** I can assign articles to authors and maintain author profiles

**Acceptance Criteria:**
- Admin can access author management in Django admin interface
- Admin can create new authors with:
  - Author name (required)
  - Author bio/description (optional)
  - Author photo/avatar (optional)
  - Contact information (optional)
- Admin can edit existing author information
- Admin can view list of all authors
- Admin can see which articles belong to each author
- Authors are independent entities (not linked to user accounts)
- **Authors do NOT need to login** - they are managed entirely by admin
- Django admin interface is accessible to authorized admin users only

