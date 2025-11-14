### Tech Stack

* Django with htmx (version 2.x)
* PostgreSQL 18 (database)
* Styling is done with Tailwind CSS
* Dependency Management: uv


### Design Decisions

* Every page should be mobile responsive
* Every Django Models should inherit from the BaseModel
* UI should be minimal, modern and elegant
* Content of the website will be managed using django admin

---

## Database Configuration

### PostgreSQL Setup

* **Database:** PostgreSQL 18
* **Local Development:** Use `docker-compose.local.yml` to run PostgreSQL in a Docker container
* **Connection Settings:**
  - Default database name: `asanbay_db`
  - Default user: `asanbay_user`
  - Default port: `5432`
  - Configure via environment variables (see `.env.local.example`)

### Running PostgreSQL Locally

```bash
# Start PostgreSQL service
docker-compose -f docker-compose.local.yml up -d

# Stop PostgreSQL service
docker-compose -f docker-compose.local.yml down

# View logs
docker-compose -f docker-compose.local.yml logs -f postgres
```

### Django Database Configuration

Django settings should connect to PostgreSQL using the credentials from environment variables:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'asanbay_db'),
        'USER': os.getenv('POSTGRES_USER', 'asanbay_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'asanbay_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}
```

---

## Authentication System

* **Framework:** Django's built-in `django.contrib.auth`
* **User Model:** Standard Django User model (no custom user model initially)
* **Authentication Type:** Optional authentication for visitors
  - Articles are viewable without login (public access)
  - User registration and login available for future comment features
  - Admin access restricted to Django admin interface (staff users only)
* **Features:**
  - User registration (email/username + password)
  - User login/logout
  - Optional authentication - visitors can browse articles without account

---

## BaseModel Structure

All Django models must inherit from a `BaseModel` abstract class with the following fields:

```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
```

**Fields:**
- `created_at`: Automatically set when object is created
- `updated_at`: Automatically updated when object is modified
- `is_active`: Boolean flag for soft delete functionality (default: True)

**Usage:**
```python
class Article(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # ... other fields
```

---

## Search Implementation

### Strategy

* **Initial Implementation:** PostgreSQL full-text search using Django ORM
* **Search Fields:** Article title and content
* **Method:** Use PostgreSQL's `search` vector with Django's `SearchVector` and `SearchQuery`
* **Real-time Search:** HTMX-powered search with debounced input (500ms delay)

### Implementation Details

* Use Django's `django.contrib.postgres.search` module
* Create search vectors on title and content fields
* Search results displayed in same format as article list
* Can scale to Elasticsearch or more advanced search solutions if needed later

### Example Query Pattern

```python
from django.contrib.postgres.search import SearchVector, SearchQuery

# Search in title and content
vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
query = SearchQuery(search_term)
articles = Article.objects.annotate(search=vector).filter(search=query)
```

---

## HTMX Integration Patterns

### Core Principles

* **Response Format:** HTMX endpoints return HTML fragments, not JSON
* **Partial Templates:** Create reusable template fragments for dynamic content
* **Target Elements:** Use `hx-target` to specify where content should be swapped

### CSRF Token Handling

* Include CSRF token in forms using `{% csrf_token %}`
* For HTMX requests, include token via `hx-headers`:
  ```html
  <div hx-post="/endpoint" 
       hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
  ```

### Loading States and User Feedback

* Use `htmx-indicator` class for loading indicators
* Elements with `htmx-indicator` class are hidden by default (opacity: 0)
* When request is active, `htmx-request` class is added to requesting element
* Child elements with `htmx-indicator` become visible during request

### Error Handling

* Return error HTML fragments that can be swapped into target elements
* Use HTTP status codes appropriately (400 for validation errors, 500 for server errors)
* Display error messages within the swapped content

### Common HTMX Patterns

1. **Search with Debounce:**
   ```html
   <input hx-get="/search" 
          hx-trigger="keyup changed delay:500ms" 
          hx-target="#results">
   ```

2. **Form Submission:**
   ```html
   <form hx-post="/submit" 
         hx-target="#result-container" 
         hx-swap="innerHTML">
   ```

3. **Polling (for future real-time features):**
   ```html
   <div hx-get="/updates" hx-trigger="every 2s"></div>
   ```

---

## Article State Management

### Status Field

Articles include a `status` field with the following choices:

* **Draft:** Article is being written, not visible to public
* **Published:** Article is live and visible in article list
* **Archived:** Article is no longer active but preserved

### Implementation

```python
class ArticleStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    ARCHIVED = 'archived', 'Archived'

class Article(BaseModel):
    status = models.CharField(
        max_length=20,
        choices=ArticleStatus.choices,
        default=ArticleStatus.DRAFT
    )
    # ... other fields
```

### Visibility Rules

* Only articles with `status='published'` appear in public article list
* Draft articles are only visible to admin users in Django admin
* Archived articles are not shown in public views but remain accessible via direct URL (optional)

---

## Social Media Sharing

### Meta Tags

* **Open Graph Tags:** For Facebook and LinkedIn sharing
  - `og:title`, `og:description`, `og:image`, `og:url`, `og:type`
* **Twitter Card Tags:** For Twitter/X sharing
  - `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`
* **Implementation:** Custom meta tag management (can use `django-meta` package if needed)

### Share Buttons

* Use native sharing URLs (no third-party libraries required):
  - Facebook: `https://www.facebook.com/sharer/sharer.php?u={url}`
  - Twitter: `https://twitter.com/intent/tweet?url={url}&text={title}`
  - LinkedIn: `https://www.linkedin.com/sharing/share-offsite/?url={url}`
* Copy link functionality using JavaScript Clipboard API

### Meta Tag Example Structure

```html
<!-- Open Graph -->
<meta property="og:title" content="{{ article.title }}">
<meta property="og:description" content="{{ article.excerpt }}">
<meta property="og:image" content="{{ article.featured_image.url }}">
<meta property="og:url" content="{{ request.build_absolute_uri }}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ article.title }}">
<meta name="twitter:description" content="{{ article.excerpt }}">
```

---

## Development Environment

### Dependency Management

* **Package Manager:** uv (fast Python package installer and resolver)
* **Installation:**
  ```bash
  # Install uv
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # Or on Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

* **Usage:**
  ```bash
  # Create a new project or sync dependencies
  uv sync
  
  # Add a new dependency
  uv add django
  
  # Add a development dependency
  uv add --dev pytest
  
  # Run commands in the virtual environment
  uv run python manage.py migrate
  uv run python manage.py runserver
  ```

* **Project Setup:**
  - Dependencies are managed in `pyproject.toml`
  - Virtual environment is automatically managed by uv
  - No need to manually activate virtual environment when using `uv run`

### Local Setup

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install Dependencies:**
   ```bash
   uv sync
   ```

3. **Start PostgreSQL:**
   ```bash
   docker-compose -f docker-compose.local.yml up -d
   ```

4. **Configure Environment Variables:**
   - Copy `.env.local.example` to `.env.local` (if created)
   - Set database credentials in environment variables or Django settings

5. **Run Migrations:**
   ```bash
   uv run python manage.py migrate
   ```

6. **Create Superuser:**
   ```bash
   uv run python manage.py createsuperuser
   ```

7. **Start Development Server:**
   ```bash
   uv run python manage.py runserver
   ```

### Environment Variables

Key environment variables for local development:
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_PORT`: Database port (default: 5432)

---

## Additional Technical Specifications

### Rich Text Editor

* **Initial Release:** Plain textarea for article content
* **Future Enhancement:** Rich text editor integration (django-ckeditor or django-tinymce) - LOW PRIORITY

### Comments System (Future - LOW PRIORITY)

* Nested comment structure using adjacency list model (parent_id)
* HTMX for immediate comment posting and replies
* Permission system for edit/delete (users can only edit/delete their own comments)

### Mobile Responsiveness

* Pure Tailwind CSS for responsive design
* Mobile-first approach for all pages
* Touch-friendly interactions for all interactive elements
* Custom components built with Tailwind CSS utility classes