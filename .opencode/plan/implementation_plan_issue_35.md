# Implementation Plan: Issue #35 - Default Profile

**Issue:** #35 - Default profile  
**Date:** January 14, 2026  
**Implementation Agent:** Build Agent  

---

## Executive Summary

Implement default profile functionality that allows users to:
- Set a specific profile as their default
- Have the default profile automatically selected on app load
- See which profile is currently set as default
- Ensure only one default profile exists per user

This is a low-complexity feature that significantly improves user experience by eliminating the need to manually select their preferred profile each session.

---

## Current State Analysis

### Database Model (No Default Support)
**File:** `backend/app/models.py` - Profile Model (Lines 26-34)
- **Current fields**: `id`, `name`, `user_id`, `journals` relationship
- **Missing**: `is_default` boolean field
- **No constraint**: Multiple profiles could theoretically be default

### Backend API (No Default Logic)
**File:** `backend/app/routers/profiles.py`
- **List profiles**: Returns all profiles with no default indication
- **Create profile**: No option to set as default during creation
- **Update profile**: No default setting capability
- **Missing**: GET/PUT endpoints for default profile management

### Frontend State Management (Basic First-Profile Logic)
**File:** `frontend/src/stores/dashboard.js` (Lines 39-61)
- **Current "default"**: `selectedProfileId.value = profiles.value[0].id` (first profile)
- **No persistence**: Selected profile resets to first on app reload
- **Missing**: Default profile detection and persistence

### Frontend UI (No Default Indication)
**File:** `frontend/src/views/Profiles.vue`
- **Profile cards**: No visual indication of default profile
- **No controls**: No buttons to set/unset default profile
- **Management**: Users cannot control default behavior

---

## Implementation Plan

### Phase 1: Database Schema Update

#### Step 1: Add `is_default` Field to Profile Model
**File:** `backend/app/models.py` - Profile Class
**Add field:**
```python
is_default = Column(Boolean, default=False, nullable=False)
```

#### Step 2: Create Database Migration
**New File:** `backend/alembic/versions/add_profile_default_field.py`
**Migration content:**
```python
"""add is_default field to profiles

Revision ID: add_profile_default_field
Revises: 15b0d85587dc
Create Date: 2026-01-14 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'add_profile_default_field'
down_revision = '15b0d85587dc'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('profiles', sa.Column('is_default', sa.Boolean(), nullable=False, server_default=sa.text('false')))

def downgrade():
    op.drop_column('profiles', 'is_default')
```

#### Step 3: Update Pydantic Models
**File:** `backend/app/routers/profiles.py` - Add `is_default` field
```python
class ProfileOut(BaseModel):
    id: int
    name: str
    journal_ids: List[int]
    is_default: bool = False
```

---

### Phase 2: Backend API Implementation

#### Step 1: Add Default Profile Validation
**New Function:** in `backend/app/routers/profiles.py`
```python
async def ensure_single_default(user_id: int, db: AsyncSession, exclude_profile_id: int = None):
    """Ensure only one default profile per user."""
    result = await db.execute(
        select(Profile)
        .where(Profile.user_id == user_id)
        .where(Profile.is_default == True)
        .where(Profile.id != exclude_profile_id if exclude_profile_id else True)
    )
    other_defaults = result.scalars().all()
    
    # Set other profiles as non-default
    for profile in other_defaults:
        profile.is_default = False
    await db.commit()
```

#### Step 2: Update Profile Creation Endpoint
**File:** `backend/app/routers/profiles.py` - POST /api/profiles/
**Add default setting logic:**
```python
@router.post("/", response_model=ProfileOut)
async def create_profile(
    profile: ProfileCreate,
    is_default: bool = False,  # New parameter
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # First profile automatically becomes default
    if is_default or await count_user_profiles(current_user.id, db) == 0:
        is_default = True
    
    # Clear other defaults if setting this one as default
    if is_default:
        await ensure_single_default(current_user.id, db)
    
    # Create profile with default flag
    new_profile = Profile(
        name=profile.name,
        user_id=current_user.id,
        is_default=is_default
    )
    # ... rest of existing logic
```

#### Step 3: Update Profile Update Endpoint
**File:** `backend/app/routers/profiles.py` - PUT /api/profiles/{profile_id}
**Add default management:**
```python
@router.put("/{profile_id}", response_model=ProfileOut)
async def update_profile(
    profile_id: int,
    profile_update: ProfileCreate,  # Reuse same structure
    is_default: bool = False,  # New parameter
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Clear other defaults if setting this one as default
    if is_default:
        await ensure_single_default(current_user.id, db, exclude_profile_id=profile_id)
    
    # Update profile including default flag
    # ... existing update logic with is_default field
```

#### Step 4: Add Default Profile Endpoint
**File:** `backend/app/routers/profiles.py` - New endpoint
```python
@router.get("/default", response_model=Optional[ProfileOut])
async def get_default_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Profile)
        .options(selectinload(Profile.journals))
        .where(Profile.user_id == current_user.id)
        .where(Profile.is_default == True)
    )
    profile = result.scalars().first()
    if not profile:
        # Fallback: return first profile if no default exists
        result = await db.execute(
            select(Profile)
            .options(selectinload(Profile.journals))
            .where(Profile.user_id == current_user.id)
            .order_by(Profile.id)
        )
        profile = result.scalars().first()
    
    return ProfileOut(
        id=profile.id, 
        name=profile.name, 
        journal_ids=[j.id for j in profile.journals],
        is_default=profile.is_default
    ) if profile else None
```

#### Step 5: Add Set Default Profile Endpoint
**File:** `backend/app/routers/profiles.py` - New endpoint
```python
@router.put("/{profile_id}/set-default", response_model=ProfileOut)
async def set_default_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Verify user owns profile
    result = await db.execute(
        select(Profile).where(Profile.id == profile_id).where(Profile.user_id == current_user.id)
    )
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Clear other defaults and set this one as default
    await ensure_single_default(current_user.id, db, exclude_profile_id=profile_id)
    profile.is_default = True
    await db.commit()
    await db.refresh(profile)
    
    return ProfileOut(
        id=profile.id, 
        name=profile.name, 
        journal_ids=[j.id for j in profile.journals],
        is_default=True
    )
```

---

### Phase 3: Frontend State Management

#### Step 1: Update API Service
**File:** `frontend/src/services/api.js` - Add default profile functions
```javascript
// Add to existing functions:
export async function getDefaultProfile() {
  const response = await apiGet('/api/profiles/default')
  return response.data
}

export async function setDefaultProfile(profileId) {
  const response = await apiPut(`/api/profiles/${profileId}/set-default`)
  return response.data
}

// Update existing functions to include is_default:
export async function getProfiles() {
  const response = await apiGet('/api/profiles/')
  return response.data  // Will include is_default field now
}
```

#### Step 2: Update Dashboard Store
**File:** `frontend/src/stores/dashboard.js` - Add default profile logic
**Add new reactive state:**
```javascript
const defaultProfileId = ref(null)
```

**Update profile loading logic (around lines 39-61):**
```javascript
async function loadProfiles(force = false) {
  if (!force && hasLoadedProfiles.value) return
  
  loadingProfiles.value = true
  try {
    profiles.value = await getProfiles()
    hasLoadedProfiles.value = true
    
    // NEW: Load default profile
    const defaultProf = await getDefaultProfile()
    if (defaultProf) {
      defaultProfileId.value = defaultProf.id
      selectedProfileId.value = defaultProf.id
    } else if (profiles.value.length > 0) {
      // Fallback: select first profile
      selectedProfileId.value = profiles.value[0].id
    }
  } catch (error) {
    console.error('Failed to load profiles:', error)
  } finally {
    loadingProfiles.value = false
  }
}
```

**Add set default profile function:**
```javascript
async function setProfileDefault(profileId) {
  try {
    await setDefaultProfile(profileId)
    defaultProfileId.value = profileId
    
    // Force profiles reload to get updated default status
    await loadProfiles(true)
  } catch (error) {
    console.error('Failed to set default profile:', error)
  }
}
```

**Update currentProfile computed:**
```javascript
const currentProfile = computed(() => {
  return profiles.value.find(p => p.id === selectedProfileId.value)
})
```

**Export new function:**
```javascript
return {
  // ... existing exports
  defaultProfileId,
  setProfileDefault
}
```

---

### Phase 4: Frontend UI Implementation

#### Step 1: Update Profiles.vue UI
**File:** `frontend/src/views/Profiles.vue`

**Add default profile indicators in profile cards (around line 40):**
```vue
<div class="card-header d-flex justify-content-between align-items-center">
  <div v-if="editingId !== profile.id" class="d-flex align-items-center gap-2">
    <div class="profile-name-section">
      <h5 class="mb-0 text-warm-dark">{{ profile.name }}</h5>
      <span v-if="profile.is_default" class="badge badge-default ms-2">Default</span>
    </div>
  </div>
  <!-- ... rest of existing header code ... -->
</div>
```

**Add "Set as Default" button (around line 55):**
```vue
<button 
  v-if="editingId !== profile.id && !profile.is_default"
  class="btn btn-sm btn-outline-terracotta d-flex align-items-center gap-1" 
  @click.stop="setDefault(profile.id)"
  :disabled="settingDefault === profile.id"
>
  <Star :size="14" /> Set as Default
</button>
```

**Add new reactive state variables:**
```javascript
const settingDefault = ref(null)
```

**Add set default function:**
```javascript
async function setDefault(profileId) {
  if (settingDefault.value === profileId) return
  
  settingDefault.value = profileId
  try {
    await setDefaultProfile(profileId)
    successMessage.value = `"${getProfileName(profileId)}" set as default profile!`
    // Reload profiles to update UI
    await loadProfiles()
    setTimeout(() => { successMessage.value = '' }, 3000)
  } catch (e) {
    console.error('Failed to set default profile:', e)
    alert('Failed to set default profile: ' + e.message)
  } finally {
    settingDefault.value = null
  }
}
```

#### Step 2: Add CSS Styles for Default Indicators
**Add to Profiles.vue style section:**
```css
.badge-default {
  background-color: var(--terracotta-500);
  color: white;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 0.3rem;
}

.profile-name-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.btn-outline-terracotta {
  border-color: var(--terracotta-500);
  color: var(--terracotta-500);
}

.btn-outline-terracotta:hover {
  background-color: var(--terracotta-500);
  color: white;
}
```

#### Step 3: Update Dashboard Profile Indicator
**File:** `frontend/src/views/Dashboard.vue` - Profile dropdown (around line 35)
**Add default indicator:**
```vue
<button 
  class="btn btn-link text-decoration-none p-0 fw-bold text-warm-dark dropdown-toggle d-flex align-items-center gap-2" 
  type="button" 
  data-bs-toggle="dropdown" 
  aria-expanded="false"
>
  {{ store.currentProfile?.name }}
  <span v-if="store.currentProfile?.is_default" class="badge badge-default ms-2">Default</span>
</button>
```

---

## Testing & Verification Plan

### Backend Testing
1. **Migration Testing**: Verify database schema updates correctly
2. **Default Constraint**: Ensure only one default per user
3. **API Endpoints**: Test new default profile endpoints
4. **Profile Creation**: Verify first profile auto-default behavior
5. **Profile Update**: Test default setting/unsetting

### Frontend Testing
1. **UI Indicators**: Verify default badges appear correctly
2. **Default Setting**: Test "Set as Default" functionality
3. **Persistence**: Confirm default profile remembered across sessions
4. **Fallback Behavior**: Test first profile selection when no default exists
5. **Edge Cases**: Handle profile deletion when it's the default

### Integration Testing
1. **End-to-End**: Create profile → Set as default → Reload app → Verify selected
2. **Multi-Profile**: Multiple profiles with different defaults → Verify switching
3. **Profile Deletion**: Delete default profile → Verify new default selection

---

## File Impact Summary

### Database Changes
1. **New Migration**: `backend/alembic/versions/add_profile_default_field.py`
2. **Model Update**: `backend/app/models.py` - Add `is_default` field

### Backend API Changes
1. **Modified**: `backend/app/routers/profiles.py` - Add default profile logic
2. **New Endpoints**: GET /default, PUT /{id}/set-default

### Frontend Changes
1. **New Functions**: `frontend/src/services/api.js` - Default profile API calls
2. **State Management**: `frontend/src/stores/dashboard.js` - Default profile logic
3. **UI Updates**: `frontend/src/views/Profiles.vue` - Default profile indicators and controls
4. **UI Updates**: `frontend/src/views/Dashboard.vue` - Default profile indicator in dropdown

---

## Implementation Priority & Dependencies

### Phase 1: Database & Backend (Foundation)
- **Estimated Time**: 45-60 minutes
- **Dependencies**: None
- **Risk Level**: Medium (database changes)

### Phase 2: Frontend State & UI (Implementation)
- **Estimated Time**: 60-75 minutes  
- **Dependencies**: Backend completion
- **Risk Level**: Low

### Phase 3: Testing & Integration (Verification)
- **Estimated Time**: 30 minutes
- **Dependencies**: All components complete
- **Risk Level**: Low

### Total Estimated Implementation Time: 2.5-3 hours

---

## Rollback Plan

### Database Rollback
1. **Revert Migration**: Apply downgrade migration to remove `is_default` field
2. **Restore Models**: Remove `is_default` from Profile model

### Backend Rollback
1. **Remove Endpoints**: Delete new default profile endpoints
2. **Revert Changes**: Remove default logic from existing endpoints

### Frontend Rollback
1. **Remove Imports**: Delete default profile API imports
2. **Revert State**: Remove default profile logic from store
3. **Remove UI**: Delete default profile indicators and controls

All changes are additive and can be safely rolled back without affecting core functionality.

---

## Success Criteria

### Backend Success
- ✅ Database migration runs successfully
- ✅ Only one default profile allowed per user
- ✅ First profile automatically becomes default
- ✅ Default profile endpoints work correctly
- ✅ Profile creation/update support default setting

### Frontend Success  
- ✅ Default profiles visually indicated with badges
- ✅ "Set as Default" buttons function correctly
- ✅ Default profile persists across app sessions
- ✅ Fallback to first profile when no default exists
- ✅ Profile deletion handles default gracefully

### User Experience Success
- ✅ Users can easily identify and set default profiles
- ✅ Default profile automatically selected on app load
- ✅ Clear visual feedback for default status
- ✅ No disruption to existing profile management workflows

---

## Notes for Build Agent

1. **Database First**: Run migration before implementing backend changes
2. **Test Migration**: Verify database update locally before deployment
3. **API Consistency**: Follow existing error handling patterns
4. **UI Consistency**: Use existing design tokens and Bootstrap classes
5. **State Management**: Follow Pinia patterns used in dashboard store
6. **Error Handling**: Maintain consistent error messaging
7. **Loading States**: Add appropriate loading indicators for async operations
8. **Accessibility**: Ensure buttons and badges are screen-reader friendly