# Building a Course Platform

- [Building a Course Platform](#building-a-course-platform)
  - [Tech Stack](#tech-stack)
  - [Overview](#overview)
  - [Static Vs Media vs Local-CDN](#static-vs-media-vs-local-cdn)
    - [Media Files:](#media-files)
    - [Static Files:](#static-files)
    - [Local CDN (e.g., Whitenoise):](#local-cdn-eg-whitenoise)
    - [Key Differences:](#key-differences)


## Tech Stack

Tech Stack:

- [Django](https://djangoproject.com) v5.1
- [Python](https://python.org) v3.12
- [HTMX](https://htmx.org)
- [django-htmx](https://github.com/adamchainz/django-htmx)
- [tailwind](https://tailwindcss.com)
- [django-tailwind](https://django-tailwind.readthedocs.io/en/latest/installation.html)
- [Flowbite](https://flowbite.com)
- [Cloudinary](https://cloudinary.com)

## Overview

What we are building

- Courses:

  - Title
  - Description
  - Thumbnail/Image
  - Access:
    - Anyone
    - Email required
      - Purchase required
    - User required (n/a)
  - Status:
    - Published
    - Coming Soon
    - Draft
  - Lessons
    - Title
    - Description
    - Video
    - Status: Published, Coming Soon, Draft

- Email verification for short-lived access
  - Views:
    - Collect user email
    - Verify user email
      - Activate session
  - Models:
    - Email
    - EmailVerificationToken

## Static Vs Media vs Local-CDN

### Media Files:

These are user-uploaded files (like images, documents, etc.).
Managed using Django's MEDIA_URL and MEDIA_ROOT settings.
Handled by Django's file handling system and typically served through a web server (e.g., Nginx, Apache) in production.

### Static Files:

These are files like CSS, JavaScript, and images that are part of the application but aren't user-uploaded.
Managed using STATIC_URL and STATIC_ROOT settings.
In production, static files are collected using python manage.py collectstatic and served by a web server or a CDN.

### Local CDN (e.g., Whitenoise):

Whitenoise is a Python library used to serve static files directly from Django, without needing an external server like Nginx or Apache.
It can serve compressed, cached, and versioned static files efficiently in production.
Works as a "local CDN" by serving static files in a way that reduces the need for external hosting, improving performance and reducing complexity.

### Key Differences:

Media files are user uploads; static files are part of the app.
Whitenoise helps serve static files in Django directly, while traditional CDNs host these files externally to improve delivery speed. **In simple terms**, media = user content, static = app content (CSS/JS), and Whitenoise helps serve static content efficiently from within Django.
