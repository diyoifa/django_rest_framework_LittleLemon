# Little Lemon Restaurant API Project

## Introduction

This README provides an overview of the Little Lemon Restaurant API project developed using Django REST Framework. The project aims to create a fully functioning API for managing restaurant operations, including menu items, orders, user management, and authentication.

## Scope

The project involves creating an API that allows client application developers to interact with the Little Lemon restaurant system. Users with different roles, including customers, managers, and delivery crew, can perform various actions such as browsing menu items, placing orders, and managing user groups.

## Project Structure and API Routes

The project follows a specific structure and defines several API routes for different functionalities. Below are the key aspects of the project:

### Structure

- Implemented as a single Django app named `LittleLemonAPI`.
- Dependencies managed using `pipenv` within a virtual environment.

### Views

- Utilizes both function-based and class-based views.
- Maintains proper API naming conventions.

### User Groups

- Defines two user groups: Manager and Delivery crew.
- Users not assigned to a group are considered customers.

### Error Handling

- Provides appropriate HTTP status codes and error messages for different scenarios, including authorization failures, validation errors, and resource not found.

```markdown
# API Endpoints

## User Registration and Token Generation Endpoints

These endpoints handle user registration and token generation functionalities.

| Endpoint            | Role               | Method | Purpose                                                      |
|---------------------|--------------------|--------|--------------------------------------------------------------|
| /api/users          | No role required   | POST   | Creates a new user with name, email, and password           |
| /api/users/me/      | Anyone with a valid user token | GET | Displays only the current user                               |
| /token/login/       | Anyone with a valid username and password | POST | Generates access tokens for API calls                        |

## Menu Items Endpoints

These endpoints manage menu items, allowing users to list, create, update, and delete them.

| Endpoint            | Role               | Method | Purpose                                                      |
|---------------------|--------------------|--------|--------------------------------------------------------------|
| /api/menu-items     | Customer, delivery crew | GET | Lists all menu items                                         |
| /api/menu-items     | Customer, delivery crew | POST, PUT, PATCH, DELETE | Denies access and returns 403 - Unauthorized          |
| /api/menu-items/{menuItem} | Customer, delivery crew | GET | Lists a single menu item                                     |
| /api/menu-items/{menuItem} | Customer, delivery crew | POST, PUT, PATCH, DELETE | Returns 403 - Unauthorized                                    |
| /api/menu-items     | Manager            | GET    | Lists all menu items                                         |
| /api/menu-items     | Manager            | POST   | Creates a new menu item and returns 201 - Created            |
| /api/menu-items/{menuItem} | Manager       | GET    | Lists a single menu item                                     |
| /api/menu-items/{menuItem} | Manager       | PUT, PATCH | Updates a single menu item                                   |
| /api/menu-items/{menuItem} | Manager       | DELETE | Deletes a menu item                                          |

## User Group Management Endpoints

These endpoints handle user group management, allowing managers to assign and remove users from groups.

| Endpoint                     | Role    | Method | Purpose                                                      |
|------------------------------|---------|--------|--------------------------------------------------------------|
| /api/groups/manager/users    | Manager | GET    | Returns all managers                                         |
| /api/groups/manager/users    | Manager | POST   | Assigns a user to the manager group and returns 201 - Created|
| /api/groups/manager/users/{userId} | Manager | DELETE | Removes a user from the manager group and returns 200 - Success or 404 - Not found |
| /api/groups/delivery-crew/users | Manager | GET | Returns all delivery crew                                   |
| /api/groups/delivery-crew/users | Manager | POST | Assigns a user to the delivery crew group and returns 201 - Created |
| /api/groups/delivery-crew/users/{userId} | Manager | DELETE | Removes a user from the delivery crew group and returns 200 - Success or 404 - Not found |

## Cart Management Endpoints

These endpoints handle cart management functionalities, allowing customers to view, add, and delete items from their carts.

| Endpoint                  | Role     | Method | Purpose                                                      |
|---------------------------|----------|--------|--------------------------------------------------------------|
| /api/cart/menu-items      | Customer | GET    | Returns current items in the cart for the current user token |
| /api/cart/menu-items      | Customer | POST   | Adds a menu item to the cart                                  |
| /api/cart/menu-items      | Customer | DELETE | Deletes all menu items created by the current user token      |

## Order Management Endpoints

These endpoints handle order management functionalities, allowing customers, managers, and delivery crew to view, create, update, and delete orders.

| Endpoint                  | Role     | Method | Purpose                                                      |
|---------------------------|----------|--------|--------------------------------------------------------------|
| /api/orders               | Customer | GET    | Returns all orders with order items created by the user      |
| /api/orders               | Customer | POST   | Creates a new order item for the user                        |
| /api/orders/{orderId}     | Customer | GET    | Returns all items for the given order ID                     |
| /api/orders               | Manager  | GET    | Returns all orders with order items for all users            |
| /api/orders/{orderId}     | Manager  | PUT, PATCH | Updates the order status and assigns a delivery crew        |
| /api/orders/{orderId}     | Manager  | DELETE | Deletes the order                                            |
| /api/orders               | Delivery crew | GET | Returns all orders with order items assigned to the delivery crew |
| /api/orders/{orderId}     | Delivery crew | PATCH | Updates the order status                                     |

```


## Additional Features

In addition to the core functionalities, the project includes the following features:

- Implementation of filtering, pagination, and sorting capabilities for menu items and orders endpoints.
- Application of throttling mechanisms for authenticated and anonymous users.

