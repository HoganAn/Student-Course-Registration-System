# Course Management System

A comprehensive Django-based web application for academic course management, designed to streamline the course selection process, facilitate teaching resource sharing, and manage student performance.

## Features

### For Students
- **Course Selection**: Browse available courses, view course details, and register for courses
- **Course Prerequisites**: System automatically checks if students have completed required prerequisite courses
- **Learning Resources**: Access and download course materials uploaded by instructors
- **Performance Tracking**: View grades for all enrolled courses

### For Teachers
- **Course Management**: Create and manage course information, capacity, and prerequisites
- **Resource Sharing**: Upload and organize teaching materials for students
- **Student Management**: View enrolled students and manage their course participation
- **Grade Management**: Record and update student grades

### System Features
- **Multi-role Authentication**: Separate models and interfaces for students and teachers with role-specific permissions
- **Session-based Security**: Secure login system with role identification stored in session
- **Data Validation**: Comprehensive validation for all user inputs
- **Security**: Password encryption using MD5 hashing and secure session management
