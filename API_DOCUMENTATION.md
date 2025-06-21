# iCAT API Documentation

## Overview

This document describes the POST APIs available in the Django admin dashboard for creating modules, assessments, questions, and answers.

## Authentication

All APIs require JWT authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Base URL

```
/dashboard/
```

## API Endpoints

### 1. Module Management

#### Create Module

**POST** `/modules/`

Creates a new learning module.

**Request Body:**

```json
{
  "name": "Cybersecurity Fundamentals",
  "description": "Introduction to basic cybersecurity concepts and best practices",
  "text": [
    "Section 1: Understanding Cyber Threats",
    "Section 2: Password Security",
    "Section 3: Safe Browsing Practices"
  ]
}
```

**Response (201 Created):**

```json
{
  "id": "uuid-string",
  "name": "Cybersecurity Fundamentals",
  "description": "Introduction to basic cybersecurity concepts and best practices",
  "text": [
    "Section 1: Understanding Cyber Threats",
    "Section 2: Password Security",
    "Section 3: Safe Browsing Practices"
  ],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Validation Rules:**

- `name`: Required, non-empty string
- `description`: Required, non-empty string
- `text`: Required, non-empty array of strings

### 2. Assessment Management

#### Create Assessment

**POST** `/assessments/`

Creates a new assessment (initial or module-based).

**Request Body:**

```json
{
  "name": "Initial Security Assessment",
  "type": "INITIAL",
  "max_questions_at_once": 10,
  "max_retries": 1
}
```

**For Module Assessment:**

```json
{
  "name": "Module 1 Assessment",
  "type": "MODULE",
  "module": "module-uuid",
  "max_questions_at_once": 5,
  "max_retries": 3
}
```

**Response (201 Created):**

```json
{
  "id": "uuid-string",
  "name": "Initial Security Assessment",
  "type": "INITIAL",
  "module": null,
  "max_questions_at_once": 10,
  "max_retries": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Assessment Types:**

- `INITIAL`: Initial assessment (cannot have module)
- `MODULE`: Module-based assessment (must have module)

**Validation Rules:**

- `name`: Required, non-empty string
- `type`: Must be "INITIAL" or "MODULE"
- `module`: Required for MODULE type, forbidden for INITIAL type
- `max_questions_at_once`: Positive integer (default: 5)
- `max_retries`: Positive integer (default: 3, forced to 1 for INITIAL)

### 3. Question Management

#### Create MCQ Question

**POST** `/questions/mcq/`

Creates a new multiple-choice question.

**Request Body for Initial Assessment:**

```json
{
  "assessment": "assessment-uuid",
  "domain": "PHISHING_AND_SOCIAL_ENGINEERING",
  "difficulty": 3,
  "text": "What should you do if you receive a suspicious email?"
}
```

**Request Body for Module Assessment:**

```json
{
  "assessment": "assessment-uuid",
  "difficulty": 2,
  "text": "What is the best practice for password creation?"
}
```

**Response (201 Created):**

```json
{
  "id": "uuid-string",
  "assessment": "assessment-uuid",
  "domain": "PHISHING_AND_SOCIAL_ENGINEERING",
  "difficulty": 3,
  "text": "What should you do if you receive a suspicious email?",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### Create Essay Question

**POST** `/questions/essay/`

Creates a new essay question.

**Request Body for Initial Assessment:**

```json
{
  "assessment": "assessment-uuid",
  "domain": "PASSWORD_HYGIENE",
  "difficulty": 4,
  "text": "Explain why strong passwords are important for cybersecurity."
}
```

**Request Body for Module Assessment:**

```json
{
  "assessment": "assessment-uuid",
  "difficulty": 3,
  "text": "Describe the steps to identify a phishing attempt."
}
```

**Response (201 Created):**

```json
{
  "id": "uuid-string",
  "assessment": "assessment-uuid",
  "domain": "PASSWORD_HYGIENE",
  "difficulty": 4,
  "text": "Explain why strong passwords are important for cybersecurity.",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Question Validation Rules:**

- `assessment`: Required, valid assessment UUID
- `domain`: Required for INITIAL assessments, forbidden for MODULE assessments
- `difficulty`: Integer between 1-5
- `text`: Required, non-empty string

**Available Domains for Initial Assessments:**

- `AUTHENTICATION_AND_DEVICE_SECURITY`
- `DATA_PRIVACY_AND_RESPONSIBLE_SHARING`
- `FINANCIAL_AND_PAYMENT_SECURITY`
- `PASSWORD_HYGIENE`
- `PHISHING_AND_SOCIAL_ENGINEERING`
- `SAFE_BROWSING_AND_PUBLIC_WIFI`

### 4. Answer Management

#### Create MCQ Answer

**POST** `/answers/mcq/`

Creates a new multiple-choice answer option.

**Request Body:**

```json
{
  "question": "question-uuid",
  "text": "Delete the email immediately",
  "is_correct": true
}
```

**Response (201 Created):**

```json
{
  "id": "uuid-string",
  "question": "question-uuid",
  "text": "Delete the email immediately",
  "is_correct": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### Create Essay Answer Rubric

**POST** `/answers/essay-rubric/`

Creates a new rubric criterion for essay questions.

**Request Body:**

```json
{
  "question": "question-uuid",
  "text": "Mentions cybersecurity best practices",
  "weight": 1.0
}
```

**Response (201 Created):**

```json
{
  "id": "uuid-string",
  "question": "question-uuid",
  "text": "Mentions cybersecurity best practices",
  "weight": 1.0,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Answer Validation Rules:**

- `question`: Required, valid question UUID
- `text`: Required, non-empty string
- `is_correct`: Boolean (for MCQ answers)
- `weight`: Positive float (for essay rubrics)

## Error Responses

### 400 Bad Request

```json
{
  "field_name": ["Error message describing the validation issue"]
}
```

### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found

```json
{
  "detail": "Resource not found."
}
```

## Usage Examples

### Complete Workflow Example

1. **Create a Module:**

```bash
curl -X POST /dashboard/modules/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Phishing Awareness",
    "description": "Learn to identify and avoid phishing attacks",
    "text": ["Introduction to Phishing", "Common Phishing Techniques", "How to Stay Safe"]
  }'
```

2. **Create an Assessment for the Module:**

```bash
curl -X POST /dashboard/assessments/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Phishing Assessment",
    "type": "MODULE",
    "module": "module-uuid-from-step-1",
    "max_questions_at_once": 5,
    "max_retries": 3
  }'
```

3. **Create MCQ Questions:**

```bash
curl -X POST /dashboard/questions/mcq/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "assessment": "assessment-uuid-from-step-2",
    "difficulty": 3,
    "text": "What is the first thing you should do when you suspect a phishing email?"
  }'
```

4. **Create MCQ Answers:**

```bash
curl -X POST /dashboard/answers/mcq/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "question-uuid-from-step-3",
    "text": "Delete it immediately",
    "is_correct": true
  }'
```

5. **Create Essay Questions:**

```bash
curl -X POST /dashboard/questions/essay/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "assessment": "assessment-uuid-from-step-2",
    "difficulty": 4,
    "text": "Explain how you would identify a phishing attempt and what steps you would take."
  }'
```

6. **Create Essay Rubrics:**

```bash
curl -X POST /dashboard/answers/essay-rubric/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "essay-question-uuid-from-step-5",
    "text": "Mentions checking sender email address",
    "weight": 1.0
  }'
```

## Notes

- All UUIDs are automatically generated
- Timestamps are automatically managed
- The system enforces business rules (e.g., only one correct answer per MCQ question)
- Initial assessments cannot have modules, and module assessments must have modules
- Initial assessment questions must have domains, while module assessment questions cannot have domains
