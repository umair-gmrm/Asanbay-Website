# 09-delete-article-medium

**As an** admin  
**I want to** delete an article using Django admin  
**So that** I can remove outdated or inappropriate content

**Acceptance Criteria:**
- Admin can access delete option for articles in Django admin interface
- Django admin asks for confirmation before deletion
- Deleted article is removed from public view immediately
- Associated comments are handled appropriately (deleted or archived based on model configuration)

