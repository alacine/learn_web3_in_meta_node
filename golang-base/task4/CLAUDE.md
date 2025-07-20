# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Run the application**: `go run main.go` (runs on port 8000)
- **Build**: `go build`
- **Test**: No specific test command found - use `go test ./...` for standard Go testing
- **Database setup**: `docker-compose up -d` (starts MySQL container)
- **Simple API test**: `./test.sh` (tests GET /api/v1/user/1)

## Architecture Overview

This is a Go REST API built with the Gin framework and GORM ORM for database operations. It follows a clean architecture pattern with clear separation of concerns:

### Core Structure
- **main.go**: Application entry point, database connection, and route setup
- **model/**: Data models (User, Post, Comment) with GORM annotations
- **service/**: Business logic layer with database operations
- **api/**: HTTP handlers and request/response processing
- **middleware/**: Request validation and processing middleware

### Database Layer
- Uses GORM with MySQL driver
- Database connection: `practice_user:practice_password@tcp(localhost:3306)/practice_db`
- Auto-migration for User, Post, Comment models
- Models use embedded `gorm.Model` for ID, CreatedAt, UpdatedAt, DeletedAt fields

### API Layer
- RESTful API with `/api/v1` prefix
- Consistent response format using generic `Resp[T]` struct
- JSON request/response binding
- URI parameter validation middleware for ID fields

### Service Pattern
- Service layer abstracts database operations
- Global DB instance managed through `service.GetDB()`
- Each entity (User, Post, Comment) has its own service struct

### Key Features
- User registration and authentication (basic password comparison)
- CRUD operations for Users, Posts, and Comments
- MySQL database with Docker containerization
- Structured error handling with consistent response codes