# Technical Limitations Analysis

## Overview
This document identifies technical limitations and gaps between the technical overview and user story requirements.

---

## 1. Content Management System Conflict ✅ RESOLVED

### Issue
**Technical Overview states:** "Content of the website will be managed using django admin."

**User Stories Require:**
- **07-create-article-high**: Authors need a frontend form to create articles
- **08-edit-article-medium**: Authors need a frontend form to edit articles
- **09-delete-article-medium**: Authors need frontend delete functionality

### Resolution
✅ **RESOLVED** - User stories have been updated to reflect that admins will use Django admin interface for article management. No sophisticated frontend UI is required for content authors.

**Updated User Stories:**
- **07-create-article-high**: Now specifies Django admin interface
- **08-edit-article-medium**: Now specifies Django admin interface
- **09-delete-article-medium**: Now specifies Django admin interface

---

## 2. Rich Text Editor Not Specified ⚠️ LOW PRIORITY

### Issue
**User Story 07-create-article-high** requires: "content (rich text editor)"

**Technical Overview:** No mention of rich text editor library

### Status
⚠️ **LOW PRIORITY** - Rich text editor is now marked as low priority and not required for initial release. Articles can use plain text or basic HTML textarea initially.

### Limitation (For Future Implementation)
- Need to select and integrate a rich text editor for Django admin (e.g., TinyMCE, CKEditor, django-ckeditor, django-tinymce)
- Editor must be compatible with Django admin interface
- **Resolution Needed:** Specify which rich text editor will be integrated with Django admin (when implementing rich text editing feature)

---

## 3. Search Implementation Not Defined ⚠️

### Issue
**User Story 10-search-articles-medium** requires:
- Search by keywords
- Search works on title and content
- Real-time search results

**Technical Overview:** No mention of search implementation

### Limitation
- Django ORM `.filter()` is basic and may not scale well for full-text search
- No mention of:
  - PostgreSQL full-text search
  - Elasticsearch/Solr
  - Django Haystack
  - Simple LIKE queries (performance concerns with large datasets)
- **Resolution Needed:** Define search strategy:
  - For small sites: Django ORM with `icontains` or `search` (PostgreSQL)
  - For larger sites: Consider Elasticsearch or PostgreSQL full-text search

---

## 4. Nested Comment Structure Not Detailed ⚠️ LOW PRIORITY

### Issue
**User Stories 13, 14** require:
- Multiple levels of nested replies
- Visual hierarchy with indentation
- Threaded discussions

**Technical Overview:** No mention of data model for nested comments

### Status
⚠️ **LOW PRIORITY** - Comments and replies are now marked as low priority and not required for initial release. Focus is on article posting and reading.

### Limitation (For Future Implementation)
- Need to decide on comment model structure:
  - **Adjacency List** (parent_id): Simple but requires recursive queries
  - **Materialized Path**: Better for display but more complex
  - **Nested Set Model**: Complex but efficient for queries
- HTMX integration for nested updates needs careful planning
- **Resolution Needed:** Specify comment model structure and query strategy (when implementing comments feature)

---

## 5. Authentication System Not Specified ⚠️

### Issue
**User Stories 01, 02, 03** require:
- User registration
- User login
- User logout
- Optional authentication (viewing without login)

**Technical Overview:** No mention of authentication approach

### Limitation
- Django has built-in authentication, but need to clarify:
  - Will use Django's default `django.contrib.auth`?
  - Custom user model needed?
  - Social authentication (OAuth) required?
  - Email verification required?
- **Resolution Needed:** Specify authentication approach

---

## 6. Social Media Sharing Implementation Missing ⚠️

### Issue
**User Stories 17, 18, 19, 20** require:
- Facebook sharing
- Twitter/X sharing
- LinkedIn sharing
- Copy link functionality

**Technical Overview:** No mention of social sharing implementation

### Limitation
- Need Open Graph meta tags for proper social media previews
- Need Twitter Card meta tags
- Need LinkedIn meta tags
- Share button implementation (native vs. third-party libraries)
- **Resolution Needed:** Specify:
  - Meta tag management (django-meta, django-seo, or custom)
  - Share button library (if any)
  - Social media API integration (if tracking shares)

---

## 7. HTMX Integration Details Missing ⚠️

### Issue
**Multiple User Stories** require HTMX for:
- Immediate comment posting (Story 11 - LOW PRIORITY)
- Immediate reply posting (Stories 13, 14 - LOW PRIORITY)
- Inline comment editing (Story 15 - LOW PRIORITY)
- Dynamic updates without page refresh

**Technical Overview:** Mentions "Django with htmx" but no implementation details

### Limitation
- Need to define HTMX patterns:
  - Partial template rendering strategy
  - HTMX endpoints structure
  - Error handling with HTMX
  - CSRF token handling with HTMX
  - Loading states and user feedback
- **Resolution Needed:** Document HTMX integration patterns

---

## 8. BaseModel Requirements Not Specified ⚠️

### Issue
**Technical Overview states:** "Every Django Models should inherit from the BaseModel"

**User Stories:** Don't specify what BaseModel should contain

### Limitation
- Need to define BaseModel fields:
  - `created_at`, `updated_at` timestamps?
  - `is_active`, `is_deleted` soft delete?
  - `created_by`, `updated_by` user tracking?
- **Resolution Needed:** Define BaseModel structure

---

## 9. Draft/Published State Management ⚠️

### Issue
**User Story 07-create-article-high** requires:
- Save article as draft
- Publish article immediately

**Technical Overview:** No mention of article state management

### Limitation
- Need to implement:
  - Article status field (draft, published, archived)
  - Draft preview functionality
  - Publishing workflow
- **Resolution Needed:** Define article state model

---

## 10. Mobile Responsiveness Implementation ⚠️

### Issue
**Technical Overview states:** "Every page should be mobile responsive"
**Multiple User Stories:** Require mobile responsive forms and UI

**Technical Overview mentions:** Flowbite for styling

### Limitation
- Flowbite is Tailwind CSS-based, need to ensure:
  - Proper Tailwind CSS integration with Django
  - Mobile-first approach for article pages
  - Touch-friendly interactions for comments/replies (LOW PRIORITY - Comments deferred)
- **Resolution Needed:** Confirm Tailwind CSS + Flowbite setup strategy for article viewing

---

## 11. Real-time Updates Not Addressed ⚠️ LOW PRIORITY

### Issue
**User Stories 11, 13, 14** require:
- "Immediately" displayed comments/replies using HTMX

**Technical Overview:** No mention of real-time capabilities

### Status
⚠️ **LOW PRIORITY** - Comments are now marked as low priority and not required for initial release.

### Limitation (For Future Implementation)
- HTMX provides partial page updates but not true real-time
- If multiple users comment simultaneously, others won't see updates without refresh
- **Resolution Needed:** Clarify if (when implementing comments feature):
  - HTMX polling is acceptable, OR
  - WebSockets/Server-Sent Events needed for true real-time

---

## 12. Comment Edit/Delete Permissions ⚠️ LOW PRIORITY

### Issue
**User Stories 15, 16** require:
- Users can edit/delete their own comments
- Edit button visible only on user's own comments

**Technical Overview:** No mention of permission system

### Status
⚠️ **LOW PRIORITY** - Comments are now marked as low priority and not required for initial release.

### Limitation (For Future Implementation)
- Need to implement:
  - Permission checks in views
  - Frontend conditional rendering based on ownership
  - Time limits for editing? (e.g., can only edit within 5 minutes)
- **Resolution Needed:** Define comment ownership and permission rules (when implementing comments feature)

---

## Summary of Critical Gaps

### High Priority (Must Resolve)
1. ✅ **RESOLVED** - Content management approach (Django admin confirmed)
2. ⚠️ Search implementation strategy
3. ⚠️ Authentication system specification (for admin access only - login optional for visitors)

### Medium Priority (Should Resolve)
5. ⚠️ Social media meta tags and sharing implementation
6. ⚠️ HTMX integration patterns (for article features, not comments)
7. ⚠️ BaseModel structure definition
8. ⚠️ Article draft/published state management

### Low Priority (Nice to Have - Not Required for Initial Release)
9. ⚠️ **Rich text editor selection** (Rich text editing deferred - plain textarea acceptable for initial release)
10. ⚠️ Mobile responsiveness confirmation
11. ⚠️ Real-time update strategy clarification
12. ⚠️ **Nested comment data model** (Comments feature deferred)
13. ⚠️ **Comment permission rules** (Comments feature deferred)

---

## Recommendations

1. ✅ **RESOLVED** - Content Management: Authors use Django admin (no custom frontend needed)
2. **Select Rich Text Editor:** Recommend django-ckeditor or django-tinymce (Django admin compatible) - **LOW PRIORITY** (deferred for initial release)
3. **Define Search Strategy:** Start with PostgreSQL full-text search, upgrade if needed
4. **Choose Comment Model:** Recommend Adjacency List (parent_id) for simplicity (LOW PRIORITY - Comments deferred)
5. **Use Django Auth:** Leverage `django.contrib.auth` with custom user model if needed
6. **Add Meta Tags:** Use `django-meta` or similar for social sharing
7. **Document HTMX Patterns:** Create HTMX endpoint conventions
8. **Define BaseModel:** Include `created_at`, `updated_at`, `is_active` at minimum

