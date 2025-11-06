# Contest MCQ Filtering - Complete Implementation

## Problem Solved
Users were seeing ALL MCQs in the site when visiting `/mcq/` while in a contest, instead of only seeing the MCQs assigned to that contest.

## Solution Implemented
Made the MCQ list view work exactly like the Problem list view - when a user is in a contest, filter MCQs to show only those assigned to the contest.

## Changes Made

### 1. Updated `judge/views/mcq.py`

#### Added Contest Detection Properties
```python
@cached_property
def in_contest(self):
    return self.profile is not None and self.profile.current_contest is not None

@cached_property
def contest(self):
    return self.profile.current_contest.contest if self.in_contest else None
```

#### Split get_queryset into Two Methods
- **`get_contest_queryset()`**: Returns only ContestMCQ objects for the current contest
- **`get_normal_queryset()`**: Returns all MCQs the user can access (normal browsing)
- **`get_queryset()`**: Checks `in_contest` and calls appropriate method

#### Updated Submission Tracking
- **`get_completed_mcqs()`**: Now filters by participation when in contest
- **`get_attempted_mcqs()`**: Now filters by participation when in contest

### 2. Updated `templates/mcq/list.html`

#### Template Logic
```django
{% if in_contest %}
    {# item is a ContestMCQ object #}
    {% set mcq = item.mcq_question %}
    {% set contest_points = item.points %}
{% else %}
    {# item is an MCQQuestion object #}
    {% set mcq = item %}
{% endif %}
```

#### Dynamic Links
- In contest: Links to `/contest/<key>/mcq/<code>/`
- Normal: Links to `/mcq/<code>/`

#### Dynamic Columns
- **In Contest**: Shows only essential columns (Status, Name, Type, Difficulty, Category, Points)
- **Normal**: Shows all columns including AC%, Users, Tags

## How It Works

### Scenario 1: User NOT in Contest
1. User visits `/mcq/`
2. `in_contest` = False
3. `get_normal_queryset()` is called
4. Shows ALL public MCQs in the site
5. Template displays full table with sorting, filtering, stats

### Scenario 2: User IN Contest
1. User joins contest "testmcc"
2. Profile.current_contest is set
3. User visits `/mcq/`
4. `in_contest` = True
5. `get_contest_queryset()` is called
6. Shows ONLY MCQs assigned to contest "testmcc"
7. Template displays simplified table with contest-specific points
8. Links point to contest MCQ detail pages

### Scenario 3: Contest-Specific URL
1. User visits `/contest/testmcc/mcqs/`
2. Uses `ContestMCQListView` (different view entirely)
3. Always shows only contest MCQs
4. Works whether user is in contest or not

## URLs Explained

| URL | View | Shows | When |
|-----|------|-------|------|
| `/mcq/` | `MCQList` | All MCQs (normal) | Not in contest |
| `/mcq/` | `MCQList` | Contest MCQs only | In contest |
| `/contest/<key>/mcqs/` | `ContestMCQListView` | Contest MCQs only | Always |

## Testing

```bash
# 1. Create MCQs
#    - test1 (not in contest)
#    - test2 (in contest "testmcc")

# 2. Without joining contest
#    Visit: http://localhost:8000/mcq/
#    Result: See both test1 AND test2

# 3. Join contest
#    Click "Join contest" on /contest/testmcc/

# 4. While in contest
#    Visit: http://localhost:8000/mcq/
#    Result: See ONLY test2 (the one in contest)

# 5. Leave contest
#    Click "Leave contest"
#    Visit: http://localhost:8000/mcq/
#    Result: See both test1 AND test2 again
```

## Key Benefits

✅ **Consistent UX**: MCQs work exactly like Problems in contests  
✅ **Auto-filtering**: Users automatically see only contest MCQs when in a contest  
✅ **Contest points**: Shows contest-specific point values  
✅ **Proper tracking**: Submissions tracked per contest participation  
✅ **No confusion**: Users can't accidentally browse all site MCQs during contest  

## Files Modified

1. **`judge/views/mcq.py`**
   - Added `in_contest` and `contest` properties
   - Split `get_queryset()` into contest and normal versions
   - Updated submission tracking to filter by participation

2. **`templates/mcq/list.html`**
   - Added conditional logic for contest/normal mode
   - Dynamic link generation
   - Dynamic column display
   - Contest points vs default points

## Summary

The MCQ system now perfectly mirrors the Problem system's contest behavior:
- When you're in a contest, you see only that contest's MCQs
- When you're not in a contest, you see all MCQs you have access to
- Contest-specific URLs always show only contest content
- Submissions are properly tracked per contest participation

**This is exactly how the problem list works, and now MCQs work the same way!** 🎉
