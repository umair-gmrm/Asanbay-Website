# 07-create-article-high

**As an** admin  
**I want to** create a new article using Django admin  
**So that** I can publish content for the society

**Acceptance Criteria:**
- Admin can access article creation form in Django admin interface
- Form includes title, content (textarea - rich text editor optional for future), category, tags, and publish/draft status options
- Admin can select one category per article (required field)
- Admin can add multiple tags to an article (tags can be created on-the-fly or selected from existing tags)
- Admin can save article as draft
- Admin can publish article immediately by changing status
- System validates required fields (title, content, category)
- Published articles appear in public article list with category and tags
- Django admin interface is accessible to authorized admin users only
- **Note:** Rich text editor is low priority - plain textarea is acceptable for initial release

