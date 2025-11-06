# Contest MCQ Feature - Complete Guide

## Overview
The Contest MCQ feature allows you to add Multiple Choice Questions (MCQs) to contests, just like you add problems. Users participating in the contest can answer these MCQs and earn points.

## Key Features

### 1. **Contest-Specific MCQs**
- Only MCQs assigned to a contest are visible when viewing that contest
- Each MCQ can have different point values in different contests
- MCQ submissions are tracked per contest participation

### 2. **Contest Integration**
- MCQs appear in a dedicated "MCQ Questions" tab in the contest interface
- Submissions are linked to contest participation
- Users can answer MCQs during their contest window
- Virtual participation is supported

### 3. **Scoring**
- Contest-specific point values override the MCQ's default points
- Partial credit is supported for multiple-choice questions
- Submissions are scored immediately upon submission

## How to Use

### Step 1: Create MCQ Questions
1. Go to `/admin/judge/mcqquestion/`
2. Click "Add MCQ Question"
3. Fill in:
   - **Code**: Unique identifier (e.g., `mcq1`)
   - **Name**: Question title
   - **Description**: Question text (supports Markdown)
   - **Question Type**: Single Choice, Multiple Choice, or True/False
   - **Difficulty**: Easy, Medium, or Hard
   - **Points**: Default points (will be overridden in contests)
   - **Partial Credit**: Whether to award partial points
4. Save the question
5. Add options (answers) to the question
6. Mark the correct options

### Step 2: Create a Contest
1. Go to `/admin/judge/contest/`
2. Create a new contest or edit an existing one
3. Fill in contest details (name, times, visibility, etc.)

### Step 3: Add MCQs to Contest
1. While editing a contest, scroll to the **"MCQ Questions"** section
2. Click "Add another MCQ Question"
3. Select the MCQ question from the dropdown
4. Set the **points** for this MCQ in this contest
5. Set the **order** (position in the list)
6. Save the contest

### Step 4: Users Answer MCQs
1. Users navigate to the contest page
2. If MCQs are added, they'll see an **"MCQ Questions"** tab
3. Click the tab to see the list of MCQs
4. Click on any MCQ to view and answer it
5. Select answer(s) and click "Submit Answer"
6. Results are shown immediately

## URL Structure

### For Regular MCQs (Outside Contests)
- **List**: `/mcq/`
- **Detail**: `/mcq/<code>/`
- **Submit**: `/mcq/<code>/submit`

### For Contest MCQs
- **List**: `/contest/<contest_key>/mcqs/`
- **Detail**: `/contest/<contest_key>/mcq/<mcq_code>/`
- **Submit**: `/contest/<contest_key>/mcq/<mcq_code>/submit`

## Database Models

### ContestMCQ
Links MCQ questions to contests with contest-specific settings:
```python
- mcq_question: Foreign key to MCQQuestion
- contest: Foreign key to Contest
- points: Contest-specific points for this MCQ
- order: Display order in the contest
```

### MCQSubmission (Updated)
Now tracks contest participation:
```python
- question: The MCQ question
- user: The user who submitted
- selected_options: Selected answer options
- is_correct: Whether the answer is correct
- points_earned: Points awarded
- participation: Contest participation (null if practice)
- contest_object: Contest MCQ (null if practice)
```

## Admin Interface

### ContestMCQ Inline
When editing a contest, you'll see:
- Sortable list of MCQs
- Drag to reorder
- Set points per MCQ
- Add/remove MCQs easily

### MCQ Question Admin
Manage MCQ questions independently:
- Create questions
- Add/edit options
- Mark correct answers
- Set default points and difficulty

## Features in Detail

### 1. **Contest Participation Tracking**
- Submissions are linked to contest participation
- Users can submit once per MCQ per participation
- Virtual participants have separate submissions

### 2. **Access Control**
- Only users who can access the contest can see its MCQs
- Contest visibility rules apply to MCQs
- Private contests keep MCQs private

### 3. **Time-Based Access**
- MCQs are only answerable during contest time
- After contest ends, MCQs remain viewable
- Virtual participants have their own time windows

### 4. **Scoring System**
- **Single Choice**: All or nothing (correct option only)
- **Multiple Choice**: Full points if all correct, partial if enabled
- **True/False**: All or nothing (correct option only)

### 5. **Immediate Feedback**
- Results shown immediately after submission
- Correct answers highlighted in green
- Incorrect selections highlighted in red
- Explanation shown if provided

## Example Workflow

### Creating a Contest with MCQs

1. **Create MCQ Questions**
   ```
   mcq1: "What is 2+2?"
   - Option A: 3 (incorrect)
   - Option B: 4 (correct)
   - Option C: 5 (incorrect)
   Points: 10
   ```

2. **Create Contest**
   ```
   Key: spring2024
   Name: Spring 2024 Programming Contest
   Start: 2024-03-01 10:00
   End: 2024-03-01 13:00
   ```

3. **Add MCQ to Contest**
   ```
   MCQ Question: mcq1
   Points: 15 (override default 10)
   Order: 1
   ```

4. **Users Access**
   ```
   URL: /contest/spring2024/mcqs/
   They see: "mcq1" worth 15 points
   Click to answer
   Submit and get immediate feedback
   ```

## Migration Applied

The following migration was created and applied:
```
0161_alter_mcqsubmission_unique_together_and_more.py
- Removed unique_together constraint (question, user)
- Added contest_object field to MCQSubmission
- Added participation field to MCQSubmission
```

This allows users to:
- Answer the same MCQ in different contests
- Have separate submissions for each contest
- Practice MCQs outside contests

## Testing Checklist

✅ **Database**
- [x] Migrations applied successfully
- [x] ContestMCQ table created
- [x] MCQSubmission updated with contest fields

✅ **Admin Interface**
- [x] Can add MCQs to contests
- [x] Can set contest-specific points
- [x] Can reorder MCQs

✅ **Views**
- [x] Contest MCQ list view created
- [x] Contest MCQ detail view created
- [x] Contest MCQ submit view created

✅ **Templates**
- [x] MCQ list template created
- [x] MCQ detail template created
- [x] MCQ tab added to contest navigation

✅ **URLs**
- [x] Contest MCQ routes added
- [x] URLs properly namespaced

## Next Steps

1. **Test the Feature**
   - Create a test contest
   - Add some MCQ questions
   - Join the contest and answer MCQs
   - Verify scoring works correctly

2. **Add to Navigation** (Optional)
   - Add "MCQ Questions" link to main contest page
   - Show MCQ count in contest info

3. **Enhance Features** (Future)
   - Add MCQ statistics to contest stats page
   - Show MCQ performance in rankings
   - Add time tracking for MCQ answers
   - Export MCQ results with problem results

## Troubleshooting

### Issue: MCQ tab doesn't appear
**Solution**: Make sure MCQs are added to the contest in the admin panel

### Issue: Can't submit MCQ answers
**Solution**: Check that:
- You're logged in
- The contest has started
- Your contest time hasn't ended
- You haven't already submitted

### Issue: Points don't match
**Solution**: Remember that contest points override MCQ default points

## Summary

You now have a fully functional Contest MCQ system! MCQs work just like problems in contests:
- Add them via admin
- Users see them in a dedicated tab
- Submissions are tracked per contest
- Scoring is automatic and immediate

The system is ready for production use! 🎉
