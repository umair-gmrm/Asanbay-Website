# 07-create-article-high

**As an** admin  
**I want to** create a new article using Django admin  
**So that** I can publish content for the society

**Acceptance Criteria:**
- Admin can access article creation form in Django admin interface
- Form includes title, content (textarea - rich text editor optional for future), **author (required)**, category, tags, and publish/draft status options
- Admin can **select an author from existing authors** or create a new author before creating article
- Admin can select one category per article (required field)
- Admin can add multiple tags to an article (tags can be created on-the-fly or selected from existing tags)
- Admin can save article as draft
- Admin can publish article immediately by changing status
- System validates required fields (title, content, author, category)
- Published articles appear in public article list with author, category and tags
- **Authors are independent of users** - they don't need to login
- Django admin interface is accessible to authorized admin users only
- **Note:** Rich text editor is low priority - plain textarea is acceptable for initial release

