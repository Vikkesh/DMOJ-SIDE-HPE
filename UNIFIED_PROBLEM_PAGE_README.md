# Unified Problem Page (LeetCode-Style Interface)

## Overview
This implementation combines the problem description, code editor, and submission status into a single unified interface similar to LeetCode.

## Files Modified/Created

### 1. New Template
- **File**: `site/templates/problem/problem_unified.html`
- **Purpose**: LeetCode-style unified interface with split-pane layout

### 2. Views Added
- **File**: `site/judge/views/problem.py`
- **New Classes**:
  - `ProblemUnified`: Main view for unified problem page
  - `LanguageTemplateAjax`: AJAX endpoint to fetch language templates
  - `SubmissionStatusAjax`: AJAX endpoint to poll submission results
  - `ProblemEditorialAjax`: AJAX endpoint to fetch problem editorial
  - `ProblemSubmissionsAjax`: AJAX endpoint to fetch user's submissions

### 3. URL Routes
- **File**: `site/dmoj/urls.py`
- **New Routes**:
  - `/problem/<problem>/unified` - Main unified page
  - `/ajax/language_template/` - Get language template
  - `/ajax/submission_status/` - Get submission status
  - `/problem/<problem>/editorial/ajax` - Get editorial content
  - `/problem/<problem>/submissions/ajax` - Get user submissions

## Features

### Layout
- **Left Panel (50%)**: Problem description with tabs
  - Description tab
  - Editorial tab (if available)
  - My Submissions tab
- **Right Panel (50%)**: Code editor with controls
  - Language selector
  - ACE code editor
  - Submit and Reset buttons
- **Bottom Panel (Slides up)**: Test results
  - Auto-opens after submission
  - Real-time status polling
  - Test case breakdown

### Interactive Features
1. **Resizable Panels**: Drag the center handle to adjust split (30-70% range)
2. **Tabbed Interface**: Switch between description/editorial/submissions
3. **Real-time Feedback**: Live polling of submission status
4. **AJAX Submissions**: No page reload required
5. **Language Templates**: Auto-load template code when switching languages

## How to Use

### Accessing the Unified Page
Visit: `/problem/<problem_code>/unified`

Example: `/problem/aplusb/unified`

### For Users
1. **Read the problem** on the left panel
2. **Select your language** from the dropdown
3. **Write your code** in the editor
4. **Click Submit** to test your solution
5. **View results** in the bottom panel that slides up

### For Developers

#### Adding to Navigation
To make this the default problem view, update the problem detail link in your templates:

```html
<!-- Old -->
<a href="{{ url('problem_detail', problem.code) }}">{{ problem.name }}</a>

<!-- New Unified -->
<a href="{{ url('problem_unified', problem.code) }}">{{ problem.name }}</a>
```

#### Customizing the Layout
Edit `problem_unified.html`:
- Adjust panel widths in CSS (`.problem-description-panel`, `.code-editor-panel`)
- Change colors in difficulty badges
- Modify editor theme/settings

## API Endpoints

### 1. Language Template
**URL**: `/ajax/language_template/?id=<language_id>`  
**Method**: GET  
**Response**:
```json
{
  "template": "# Your code here\n",
  "ace_mode": "python",
  "name": "Python 3"
}
```

### 2. Submission Status
**URL**: `/ajax/submission_status/?id=<submission_id>`  
**Method**: GET  
**Response**:
```json
{
  "id": 12345,
  "status": "AC",
  "status_display": "Accepted",
  "is_graded": true,
  "time": "0.05s",
  "memory": "15.2 MB",
  "points": 100.0,
  "language": "Python 3",
  "test_cases": [
    {"status": "AC", "time": "0.01s", "memory": "15.0 MB"}
  ]
}
```

### 3. Problem Editorial
**URL**: `/problem/<problem>/editorial/ajax`  
**Method**: GET  
**Response**:
```json
{
  "content": "<h1>Solution</h1><p>...</p>",
  "publish_on": "2025-10-31T12:00:00Z"
}
```

### 4. User Submissions
**URL**: `/problem/<problem>/submissions/ajax`  
**Method**: GET  
**Response**:
```json
{
  "submissions": [
    {
      "id": 12345,
      "date": "2025-10-31T12:00:00Z",
      "status": "AC",
      "status_display": "Accepted",
      "language": "Python 3",
      "time": "0.05s",
      "memory": "15.2 MB",
      "points": 100.0
    }
  ]
}
```

## Technical Details

### AJAX Submission Flow
1. User clicks Submit button
2. Code is sent via AJAX POST to `/problem/<code>/submit`
3. Server responds with submission ID
4. Client polls `/ajax/submission_status/` every second
5. Results are displayed when grading completes

### Security
- CSRF token validation on all POST requests
- User authentication required for submissions
- Permission checks for viewing submissions
- Rate limiting on submission endpoint (429 response)

### Browser Compatibility
- Modern browsers with ES6 support
- Fetch API required
- ACE editor compatibility

## Troubleshooting

### Submission Not Working
1. Check browser console for errors
2. Verify CSRF token is being sent
3. Ensure user is authenticated
4. Check submission limit hasn't been reached

### Results Not Updating
1. Check network tab for polling requests
2. Verify submission ID is correct
3. Check server logs for grading errors

### Editor Not Loading
1. Verify ACE_URL setting in settings.py
2. Check static files are being served
3. Ensure JavaScript files are loaded

## Future Enhancements
- [ ] Add custom test cases
- [ ] Show expected vs actual output
- [ ] Add keyboard shortcuts (Ctrl+Enter to submit)
- [ ] Save code drafts locally
- [ ] Add split view for test cases
- [ ] Theme customization
- [ ] Mobile responsive design
