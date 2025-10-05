# ✅ Blog API

## 🔐 Authenticaiton

- [x] **User Registration** - create new users, hash passwords before saving.
- [x] **User login** - check credentials, issude JWT token.
- [x] **JWT Verification** - middleware/utility to decode and verify tokens.
- [x] **Protected Routes** - require a valid JWT for creating, updating or deleting blog posts.

---

## 📝 Blog Posts (Core Features)

- [x] **Create Post** - authenticated users can create blog posts.
- [x] **List Posts** - anyone can view all blog posts (public route).
- [x] **Retrieve Post** - anyone can view a single blog post by ID.
- [x] **Update Post** - only the post's author can update their post.
- [x] **Delete Post** - only the post's author can delete their post.

---

## 👤 User ↔ Post Relationship

- [x] Each `Post` must have an `author` (ForiegnKey to `User`).
- [x] When querying posts, include the author's username in the reposnse.

---

## ⚙ Optional Nice-to-Haves (if time allows)

- [x] **TImestamps** - auto-add `created_at` and `updated_at` to posts.
- [x] **Pagination** - limit number of posts returned per page.
- [x] **Search/Filter** - allow filtering posts by title/author.
- [ ] **Comments** - users can comment on posts (optional stretch feature).

---

## 🔎 Visual Flow Recap

```
    [ User registers ] → [ User logs in → gets JWT ]
       ↓
    [ User creates post (JWT required) ]
       ↓
    [ Other users can read posts (no JWT required) ]
       ↓
    [ Only author can edit/delete their posts ]



```

---

## 👉 By the end of Friday, your Blog API should be:

- **Secure** (JWT-based auth).
- **Functional** (CRUD posts).
- **Owner-aware** (only authors edit/delete).

---

# Keep Simple

- One app: `blog`
  - Models: `User` (if custom), `Post`, maybe `Comment`.
  - Views: registration, login, post CRUD.
  - Serializers: user + post serializers.

---

# App Structure

## Project name: `blog_api`

### Apps:

- `accounts` ➡ registration, login, JWT
- `blog` ➡ posts, comments

```
blog_api/
│
├── blog_api/        # project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/        # user auth app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── blog/            # posts + comments app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
└── manage.py



```
