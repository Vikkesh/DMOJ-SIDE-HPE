# MCQ Implementation - Backend & Admin Setup

## What Was Created

### 1. **Models** (`/site/judge/models/mcq.py`)

Three new database models were created:

#### **MCQQuestion Model**
- **Purpose**: Stores MCQ questions
- **Key Fields**:
  - `code`: Unique identifier (like problem code)
  - `name`: Question title
  - `description`: Question text (supports markdown)
  - `question_type`: SINGLE, MULTIPLE, or TRUE_FALSE
  - `difficulty`: Easy, Medium, or Hard
  - `points`: Points awarded for correct answer
  - `partial_credit`: Allow partial points for multiple choice
  - `explanation`: Answer explanation shown after submission
  - `randomize_options`: Randomize option order per user
  - Access control fields (authors, curators, organizations, is_public)
  - Statistics (user_count, ac_rate)

#### **MCQOption Model**
- **Purpose**: Stores answer options for each MCQ question
- **Key Fields**:
  - `question`: Foreign key to MCQQuestion
  - `option_text`: The option text (supports markdown)
  - `is_correct`: Boolean indicating if this is a correct answer
  - `order`: Display order (0-based)

#### **MCQSubmission Model**
- **Purpose**: Tracks user submissions/answers
- **Key Fields**:
  - `question`: Foreign key to MCQQuestion
  - `user`: Foreign key to Profile
  - `selected_options`: Many-to-Many with MCQOption
  - `is_correct`: Whether the answer is correct
  - `points_earned`: Points awarded
  - `time_taken`: Time taken to answer in seconds
  - `submitted_at`: Timestamp

### 2. **Admin Interface** (`/site/judge/admin/mcq.py`)

Three admin classes were created:

#### **MCQQuestionAdmin**
- Full admin interface for creating/editing MCQ questions
- **Features**:
  - Inline option editor (add 2-10 options directly)
  - Validation for correct answers based on question type
  - List display with code, name, type, difficulty, authors, points
  - Filters by: is_public, question_type, difficulty, creator
  - Search by: code, name, author username
  - Bulk actions: Make public/private
  - Permission checks: only authors/curators can edit
  - Markdown support for question and explanation text

#### **MCQOptionInline**
- Inline form for adding options within MCQQuestion admin
- Automatically limits True/False questions to exactly 2 options
- Shows: option_text, is_correct checkbox, order field

#### **MCQSubmissionAdmin**
- View-only admin for monitoring submissions
- Shows: user, question, correctness, points earned, time taken
- Filters by: is_correct, submission date, difficulty
- Cannot add/edit submissions (read-only)

### 3. **Database Migrations**
- Migration file created: `judge/migrations/0157_alter_profile_timezone_mcqquestion_mcqoption_and_more.py`
- Tables created:
  - `judge_mcqquestion`
  - `judge_mcqoption`
  - `judge_mcqsubmission`
  - Related junction tables for ManyToMany fields

### 4. **Updated Files**
- `/site/judge/models/__init__.py` - Added MCQ imports
- `/site/judge/admin/__init__.py` - Registered MCQ admin classes

## How to Use (Admin Panel)

### Access the Admin Panel
1. Go to your site's admin URL: `http://localhost:8000/admin/`
2. Login with superuser credentials
3. You'll see new sections:
   - **MCQ questions** (under Judge section)
   - **MCQ submissions** (under Judge section)

### Creating an MCQ Question

1. **Click "MCQ questions" → "Add MCQ question"**

2. **Fill in Basic Information**:
   - Code: `mcq001` (unique, lowercase alphanumeric)
   - Name: "What is Python?"
   - Question Type: Choose from Single Choice, Multiple Choice, or True/False
   - Difficulty: Easy/Medium/Hard
   - Is Public: Check if you want it visible to all
   - Authors: Select yourself or other users
   - Description: Write the question text (markdown supported)

3. **Configure Settings**:
   - Points: How many points for correct answer (default: 1.0)
   - Partial Credit: Check for multiple choice if you want partial points
   - Randomize Options: Check to randomize option order
   - Explanation: Optional explanation shown after answering

4. **Select Taxonomy**:
   - Types: Select question categories (uses same types as Problems)
   - Group: Select question group (uses same groups as Problems)

5. **Add Options** (in the inline section at bottom):
   - **For Single Choice / True-False**: 
     - Add 2-10 options
     - Check "Is correct" for EXACTLY ONE option
   - **For Multiple Choice**:
     - Add 2-10 options  
     - Check "Is correct" for ONE OR MORE options
   - Set order (0, 1, 2, etc.) if not randomizing

6. **Save**

### Validation Rules
- **Single Choice**: Must have exactly 1 correct answer
- **True/False**: Must have exactly 2 options, 1 correct
- **Multiple Choice**: Must have at least 1 correct answer
- Minimum 2 options, maximum 10 options

## Scoring Logic (Built-in)

The `MCQSubmission.calculate_score()` method handles automatic scoring:

### Single Choice & True/False
- **100% points** if selected option matches the one correct answer
- **0 points** otherwise

### Multiple Choice
- **100% points** if selected options exactly match all correct answers
- **Partial points** (if enabled):
  - Formula: `(correct_selected - incorrect_selected) / total_correct * points`
  - Example: 4 options, 2 are correct, user selects 1 correct + 1 incorrect
    - Score: (1 - 1) / 2 = 0 points
  - Example: 4 options, 2 are correct, user selects both correct + 0 incorrect
    - Score: (2 - 0) / 2 = 100% points
- **0 points** if partial credit disabled and answer not perfect

## Permissions

New permissions created:
- `judge.edit_own_mcq` - Can create and edit own MCQ questions
- `judge.edit_all_mcq` - Can edit all MCQ questions

Assign these permissions to user groups as needed.

## What's NOT Included (Frontend)

This implementation only covers the backend and admin panel. Still needed:

1. **Frontend Views**: Display MCQ questions to users
2. **Submission Forms**: Allow users to select answers
3. **Results Page**: Show user's score and correct answers
4. **Contest Integration**: Include MCQs in contests
5. **MCQ List Page**: Browse available MCQs
6. **User Statistics**: Track user's MCQ performance
7. **URLs**: Route configuration for MCQ pages

## Next Steps (For Frontend Implementation)

1. Create views in `judge/views/` for MCQ display
2. Create templates in `judge/templates/` for MCQ UI
3. Add URL patterns in `judge/urls.py`
4. Integrate with existing contest system (optional)
5. Add MCQ statistics to user profiles
6. Create MCQ practice mode vs contest mode

## Testing the Admin

1. Start server: `python manage.py runserver`
2. Access admin: `http://localhost:8000/admin/`
3. Navigate to "MCQ questions"
4. Click "Add MCQ question"
5. Fill in all required fields and add options
6. Save and verify it appears in the list

The admin panel is now fully functional for creating and managing MCQ questions!
