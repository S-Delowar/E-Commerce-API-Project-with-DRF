# Ecommerce API Project

A comprehensive **Ecommerce API** built using **Django** and **Django Rest Framework** (DRF). This project provides a robust backend for managing an ecommerce platform, supporting features such as authentication, product and cart management, order processing, and payment integration with Stripe.

The project is containerized with **Docker** and designed for scalability, maintainability, and production deployment.

---

## Features

### Authentication & Authorization:
- User registration, login, and password management using **dj-rest-auth** and **django-allauth**.
- Token-based authentication with **Simple JWT** for secure API access.
- Social account authentication using `django-allauth[socialaccount]`.

### Product and Shop Management:
- API endpoints for managing products and shops.
- Supports image uploads for products using **Pillow**.

### Cart and Order:
- Add, update, or remove items in the cart.
- Place orders based on the cart items.

### Payment Integration:
- Stripe integration for handling payments.
- Webhooks for real-time Stripe event handling.

### Testing
- Comprehensive unit tests for the models as well as api endpoints.
- 
### API Documentation:
- Auto-generated API documentation using **drf-spectacular**.

### CORS Support:
- Cross-origin requests enabled using **django-cors-headers**.

### Production-Ready Setup:
- Configured with **PostgreSQL** for database management.
- Dockerized for development and production environments.
- Environment management with **django-environ**.

---

## Technologies Used

- **Django**: Web framework.
- **Django Rest Framework (DRF)**: For building RESTful APIs.
- **PostgreSQL**: Production database.
- **Docker**: For containerized environments.
- **Stripe**: Payment gateway integration.
- **JWT**: Token-based authentication.
- **drf-spectacular**: For API schema generation and documentation.

---
